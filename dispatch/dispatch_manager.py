"""
Dispatch Manager
Handles ambulance assignment, routing, and resource allocation
"""

import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.models import Ambulance, DispatchAssignment, TriageCase
import config


class DispatchManager:
    """
    Manages ambulance dispatch operations
    - Find nearest available ambulance
    - Calculate ETA
    - Assign resources
    - Track dispatch status
    """
    
    def __init__(self):
        self.assignment_counter = 0
    
    def calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def estimate_travel_time(
        self,
        distance_km: float,
        is_emergency: bool = True,
        traffic_multiplier: float = 1.0
    ) -> int:
        """
        Estimate travel time in minutes
        
        Args:
            distance_km: Distance in kilometers
            is_emergency: Whether using lights/sirens (affects average speed)
            traffic_multiplier: Adjust for traffic conditions (1.0 = normal)
        
        Returns:
            Estimated time in minutes
        """
        # Average speeds (km/h)
        if is_emergency:
            avg_speed = 60  # Emergency response with lights/sirens
        else:
            avg_speed = 45  # Normal driving
        
        # Calculate base time
        time_hours = distance_km / avg_speed
        time_minutes = time_hours * 60
        
        # Apply traffic adjustment
        time_minutes *= traffic_multiplier
        
        # Add base response time (crew prep, startup)
        time_minutes += 2
        
        return int(math.ceil(time_minutes))
    
    def find_nearest_ambulance(
        self,
        patient_lat: float,
        patient_lon: float,
        db_session,
        required_equipment: Optional[List[str]] = None,
        min_crew_size: int = 2
    ) -> Optional[Tuple[Ambulance, float, int]]:
        """
        Find the nearest available ambulance
        
        Returns:
            (ambulance, distance_km, eta_minutes) or None if no ambulance available
        """
        # Query available ambulances
        available = db_session.query(Ambulance).filter(
            Ambulance.status == 'available',
            Ambulance.in_service == True
        ).all()
        
        if not available:
            return None
        
        # Filter by requirements
        candidates = []
        for ambulance in available:
            # Check crew size
            if ambulance.crew_size < min_crew_size:
                continue
            
            # Check equipment if specified
            if required_equipment:
                amb_equipment = ambulance.special_equipment or []
                if not all(eq in amb_equipment for eq in required_equipment):
                    continue
            
            # Calculate distance
            if ambulance.current_latitude and ambulance.current_longitude:
                distance = self.calculate_distance(
                    ambulance.current_latitude,
                    ambulance.current_longitude,
                    patient_lat,
                    patient_lon
                )
            else:
                # Use station location if current position unknown
                if ambulance.station_latitude and ambulance.station_longitude:
                    distance = self.calculate_distance(
                        ambulance.station_latitude,
                        ambulance.station_longitude,
                        patient_lat,
                        patient_lon
                    )
                else:
                    continue
            
            eta = self.estimate_travel_time(distance, is_emergency=True)
            candidates.append((ambulance, distance, eta))
        
        if not candidates:
            return None
        
        # Sort by distance and return nearest
        candidates.sort(key=lambda x: x[1])
        return candidates[0]
    
    def assign_ambulance(
        self,
        case: TriageCase,
        ambulance: Ambulance,
        db_session,
        dispatcher_id: str,
        priority: str = 'high',
        notes: str = ''
    ) -> DispatchAssignment:
        """
        Create a dispatch assignment
        """
        # Calculate routing info
        distance = self.calculate_distance(
            ambulance.current_latitude or ambulance.station_latitude,
            ambulance.current_longitude or ambulance.station_longitude,
            case.patient_latitude,
            case.patient_longitude
        )
        
        eta = self.estimate_travel_time(distance, is_emergency=True)
        
        # Create assignment
        self.assignment_counter += 1
        assignment = DispatchAssignment(
            assignment_id=f"DISP_{datetime.now().strftime('%Y%m%d')}_{self.assignment_counter:04d}",
            case_id=case.case_id,
            ambulance_id=ambulance.ambulance_id,
            assigned_at=datetime.now(),
            status='pending',
            pickup_latitude=case.patient_latitude,
            pickup_longitude=case.patient_longitude,
            pickup_address=case.patient_address or "Address not provided",
            estimated_distance_km=round(distance, 2),
            estimated_time_minutes=eta,
            priority=priority,
            assigned_by=dispatcher_id,
            assignment_notes=notes
        )
        
        # Update ambulance status
        ambulance.status = 'dispatched'
        ambulance.updated_at = datetime.now()
        
        # Save to database
        db_session.add(assignment)
        db_session.commit()
        
        return assignment
    
    def update_dispatch_status(
        self,
        assignment_id: str,
        new_status: str,
        db_session,
        notes: Optional[str] = None
    ):
        """
        Update the status of a dispatch assignment
        """
        assignment = db_session.query(DispatchAssignment).filter_by(
            assignment_id=assignment_id
        ).first()
        
        if not assignment:
            raise ValueError(f"Assignment {assignment_id} not found")
        
        # Update status
        assignment.status = new_status
        
        # Update timestamps based on status
        now = datetime.now()
        if new_status == 'dispatched':
            assignment.dispatched_at = now
        elif new_status == 'en_route':
            assignment.en_route_at = now
        elif new_status == 'on_scene':
            assignment.arrived_at = now
            # Calculate actual response time
            if assignment.dispatched_at:
                delta = now - assignment.dispatched_at
                assignment.actual_response_time_minutes = int(delta.total_seconds() / 60)
        elif new_status == 'transporting':
            assignment.transported_at = now
        elif new_status in ['completed', 'cancelled']:
            assignment.completed_at = now
            
            # Update ambulance status back to available
            ambulance = db_session.query(Ambulance).filter_by(
                ambulance_id=assignment.ambulance_id
            ).first()
            if ambulance:
                ambulance.status = 'available'
        
        if notes:
            assignment.outcome_notes = notes
        
        db_session.commit()
    
    def get_active_dispatches(self, db_session) -> List[DispatchAssignment]:
        """
        Get all active dispatch assignments
        """
        return db_session.query(DispatchAssignment).filter(
            DispatchAssignment.status.in_(['pending', 'dispatched', 'en_route', 'on_scene', 'transporting'])
        ).all()
    
    def get_dispatch_summary(self, db_session) -> Dict:
        """
        Get summary of dispatch operations
        """
        total_ambulances = db_session.query(Ambulance).filter(
            Ambulance.in_service == True
        ).count()
        
        available = db_session.query(Ambulance).filter(
            Ambulance.status == 'available',
            Ambulance.in_service == True
        ).count()
        
        dispatched = db_session.query(Ambulance).filter(
            Ambulance.status.in_(['dispatched', 'en_route', 'on_scene', 'transporting'])
        ).count()
        
        active_assignments = len(self.get_active_dispatches(db_session))
        
        return {
            'total_ambulances': total_ambulances,
            'available': available,
            'dispatched': dispatched,
            'utilization_rate': round((dispatched / total_ambulances * 100) if total_ambulances > 0 else 0, 1),
            'active_assignments': active_assignments
        }


def initialize_sample_ambulances(db_session):
    """
    Create sample ambulance fleet for testing
    """
    # City center coordinates (example: Seattle, WA)
    base_lat = 47.6062
    base_lon = -122.3321
    
    ambulances = [
        {
            'ambulance_id': 'AMB_001',
            'unit_name': 'Medic 1',
            'vehicle_type': 'ALS',
            'station_id': 'STATION_1',
            'status': 'available',
            'current_latitude': base_lat + 0.01,
            'current_longitude': base_lon - 0.01,
            'current_address': '123 Hospital Way, Seattle, WA',
            'station_latitude': base_lat + 0.01,
            'station_longitude': base_lon - 0.01,
            'station_address': 'Station 1, Seattle, WA',
            'crew_size': 2,
            'paramedic_on_board': True,
            'equipment_level': 'advanced',
            'special_equipment': ['defibrillator', 'ventilator', 'cardiac_monitor'],
            'in_service': True,
            'fuel_level': 85,
        },
        {
            'ambulance_id': 'AMB_002',
            'unit_name': 'Medic 2',
            'vehicle_type': 'ALS',
            'station_id': 'STATION_2',
            'status': 'available',
            'current_latitude': base_lat - 0.02,
            'current_longitude': base_lon + 0.02,
            'current_address': '456 Emergency Ln, Seattle, WA',
            'station_latitude': base_lat - 0.02,
            'station_longitude': base_lon + 0.02,
            'station_address': 'Station 2, Seattle, WA',
            'crew_size': 2,
            'paramedic_on_board': True,
            'equipment_level': 'advanced',
            'special_equipment': ['defibrillator', 'cardiac_monitor'],
            'in_service': True,
            'fuel_level': 92,
        },
        {
            'ambulance_id': 'AMB_003',
            'unit_name': 'Basic 3',
            'vehicle_type': 'BLS',
            'station_id': 'STATION_3',
            'status': 'available',
            'current_latitude': base_lat + 0.03,
            'current_longitude': base_lon + 0.01,
            'current_address': '789 Rescue Rd, Seattle, WA',
            'station_latitude': base_lat + 0.03,
            'station_longitude': base_lon + 0.01,
            'station_address': 'Station 3, Seattle, WA',
            'crew_size': 2,
            'paramedic_on_board': False,
            'equipment_level': 'basic',
            'special_equipment': ['defibrillator'],
            'in_service': True,
            'fuel_level': 78,
        },
    ]
    
    for amb_data in ambulances:
        # Check if already exists
        existing = db_session.query(Ambulance).filter_by(
            ambulance_id=amb_data['ambulance_id']
        ).first()
        
        if not existing:
            ambulance = Ambulance(**amb_data)
            db_session.add(ambulance)
    
    db_session.commit()
    print(f"[OK] Initialized {len(ambulances)} ambulances")


# Example usage
if __name__ == '__main__':
    from database.models import DatabaseManager
    
    # Initialize database
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    
    # Create sample ambulances
    initialize_sample_ambulances(session)
    
    # Test dispatch manager
    dispatch_mgr = DispatchManager()
    
    # Example: Find nearest ambulance to a location
    patient_lat = 47.6162
    patient_lon = -122.3421
    
    result = dispatch_mgr.find_nearest_ambulance(patient_lat, patient_lon, session)
    
    if result:
        ambulance, distance, eta = result
        print(f"\nNearest ambulance: {ambulance.unit_name}")
        print(f"Distance: {distance:.2f} km")
        print(f"ETA: {eta} minutes")
    else:
        print("\nNo ambulances available")
    
    # Get summary
    summary = dispatch_mgr.get_dispatch_summary(session)
    print(f"\nDispatch Summary:")
    print(f"  Total Ambulances: {summary['total_ambulances']}")
    print(f"  Available: {summary['available']}")
    print(f"  Dispatched: {summary['dispatched']}")
    print(f"  Utilization: {summary['utilization_rate']}%")
    
    session.close()
