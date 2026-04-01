"""
Database Models for Emergency Triage System
SQLite database schema and ORM models
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config

Base = declarative_base()


class TriageCase(Base):
    """
    Main triage case record
    Stores complete information about each patient interaction
    """
    __tablename__ = 'triage_cases'
    
    # Primary key
    case_id = Column(String(50), primary_key=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    
    # Patient information (anonymized in production)
    patient_age = Column(Integer)
    chief_complaint = Column(Text)
    symptoms = Column(JSON)  # List of symptoms
    transcript = Column(Text)  # Full conversation transcript
    
    # Patient Location
    patient_latitude = Column(Float)
    patient_longitude = Column(Float)
    patient_address = Column(String(500))
    patient_city = Column(String(100))
    patient_state = Column(String(50))
    patient_zipcode = Column(String(20))
    location_accuracy = Column(String(20))  # 'gps', 'address', 'approximate'
    
    # Contact Information
    callback_phone = Column(String(20))
    caller_name = Column(String(200))
    
    # Clinical data
    pain_level = Column(Integer)  # 1-10 scale
    duration_hours = Column(Float)
    conscious_status = Column(Boolean)
    medical_history = Column(Text)
    medications = Column(Text)
    
    # Vital Signs (NEW: Advanced Assessment)
    heart_rate = Column(Integer)  # bpm
    blood_pressure = Column(String(20))  # "120/80"
    respiratory_rate = Column(Integer)  # breaths/min
    spo2 = Column(Integer)  # % oxygen saturation
    temperature = Column(Float)  # Fahrenheit
    consciousness_level = Column(String(50))  # 'Alert', 'Verbal', 'Pain', 'Unresponsive'
    symptom_duration = Column(String(100))  # Duration description
    patient_gender = Column(String(20))  # Male, Female, Other
    
    # ML Prediction
    ml_risk_score = Column(Float)  # 0-1
    ml_confidence = Column(Float)  # 0-1
    ml_recommendation = Column(String(50))  # 'emergency' or 'non_emergency'
    ml_reasoning = Column(Text)
    
    # Safety
    safety_override_applied = Column(Boolean, default=False)
    safety_override_reasons = Column(JSON)
    critical_symptoms_detected = Column(JSON)
    
    # Routing
    routed_to = Column(String(50))  # 'dispatcher' or 'nurse'
    queue_priority = Column(String(20))  # 'HIGH', 'MEDIUM', 'LOW'
    
    # Human Decision
    human_decision = Column(String(50), nullable=True)  # Final outcome
    human_decision_by = Column(String(100), nullable=True)  # Operator ID
    human_decision_at = Column(DateTime, nullable=True)
    human_override = Column(Boolean, default=False)
    human_override_reason = Column(Text, nullable=True)
    
    # Final disposition
    final_disposition = Column(String(100), nullable=True)
    # Examples: 'ambulance_dispatched', 'nurse_callback', 'self_care_advised', 'clinic_referral'
    
    # Feedback & Quality
    outcome_verified = Column(Boolean, default=False)
    actual_emergency = Column(Boolean, nullable=True)  # Ground truth after the fact
    feedback_notes = Column(Text, nullable=True)
    
    # Metadata
    intake_duration_seconds = Column(Integer)
    total_handling_time_seconds = Column(Integer)
    conversation_turns = Column(Integer)
    assessment_language = Column(String(10), default='en')  # 'en' or 'mr' for language tracking
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'case_id': self.case_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'patient_age': self.patient_age,
            'chief_complaint': self.chief_complaint,
            'pain_level': self.pain_level,
            'ml_risk_score': self.ml_risk_score,
            'ml_recommendation': self.ml_recommendation,
            'routed_to': self.routed_to,
            'human_decision': self.human_decision,
            'final_disposition': self.final_disposition,
        }


class AuditLog(Base):
    """
    Comprehensive audit trail
    Every action is logged for compliance and feedback
    """
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    # Reference
    case_id = Column(String(50), nullable=False)
    
    # Action details
    action_type = Column(String(50), nullable=False)
    # Examples: 'case_created', 'ml_prediction', 'safety_override', 
    #           'human_decision', 'queue_assignment', 'disposition_set'
    
    actor = Column(String(100))  # Who performed the action (system/user ID)
    action_details = Column(JSON)  # Full details
    
    # Context
    previous_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'case_id': self.case_id,
            'action_type': self.action_type,
            'actor': self.actor,
            'action_details': self.action_details,
        }


class KPIMetric(Base):
    """
    KPI tracking table
    Stores daily/hourly metrics for dashboard
    """
    __tablename__ = 'kpi_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    metric_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    
    # Volume metrics
    total_cases = Column(Integer, default=0)
    emergency_cases = Column(Integer, default=0)
    non_emergency_cases = Column(Integer, default=0)
    
    # Accuracy metrics
    correct_predictions = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)  # Predicted emergency, was not
    false_negatives = Column(Integer, default=0)  # Predicted non-emergency, was emergency (CRITICAL)
    
    # Performance metrics
    avg_handling_time_seconds = Column(Float)
    avg_risk_score = Column(Float)
    human_override_count = Column(Integer, default=0)
    
    # Safety metrics
    safety_overrides_applied = Column(Integer, default=0)
    critical_symptoms_detected = Column(Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'metric_date': self.metric_date,
            'total_cases': self.total_cases,
            'emergency_cases': self.emergency_cases,
            'non_emergency_cases': self.non_emergency_cases,
            'false_negatives': self.false_negatives,
            'avg_handling_time_seconds': self.avg_handling_time_seconds,
        }


class SystemHealth(Base):
    """
    System health monitoring
    Tracks uptime, errors, and performance
    """
    __tablename__ = 'system_health'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    # Health status
    status = Column(String(20), nullable=False)  # 'healthy', 'degraded', 'down'
    
    # Performance
    avg_response_time_ms = Column(Float)
    active_sessions = Column(Integer)
    queue_lengths = Column(JSON)  # {'dispatcher': 3, 'nurse': 5}
    
    # Errors
    error_count_last_hour = Column(Integer, default=0)
    last_error_message = Column(Text, nullable=True)


class Ambulance(Base):
    """
    Ambulance/Resource Management
    Tracks all available emergency response units
    """
    __tablename__ = 'ambulances'
    
    # Primary key
    ambulance_id = Column(String(50), primary_key=True)
    
    # Basic Info
    unit_name = Column(String(100), nullable=False)  # "Unit-12", "Ambulance A"
    vehicle_type = Column(String(50))  # 'ALS' (Advanced Life Support), 'BLS' (Basic), 'Fire', 'Police'
    station_id = Column(String(50))  # Home station
    
    # Status
    status = Column(String(20), nullable=False, default='available')
    # 'available', 'dispatched', 'en_route', 'on_scene', 'transporting', 'hospital', 'unavailable'
    
    # Location (current position)
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    current_address = Column(String(500))
    last_location_update = Column(DateTime, default=datetime.now)
    
    # Station Location (home base)
    station_latitude = Column(Float)
    station_longitude = Column(Float)
    station_address = Column(String(500))
    
    # Crew
    crew_size = Column(Integer, default=2)
    paramedic_on_board = Column(Boolean, default=True)
    
    # Capabilities
    equipment_level = Column(String(50))  # 'basic', 'advanced', 'critical_care'
    special_equipment = Column(JSON)  # ['defibrillator', 'ventilator', 'cardiac_monitor']
    
    # Operational
    in_service = Column(Boolean, default=True)
    last_maintenance = Column(DateTime)
    fuel_level = Column(Integer)  # Percentage
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'ambulance_id': self.ambulance_id,
            'unit_name': self.unit_name,
            'vehicle_type': self.vehicle_type,
            'status': self.status,
            'current_latitude': self.current_latitude,
            'current_longitude': self.current_longitude,
            'current_address': self.current_address,
            'station_address': self.station_address,
            'paramedic_on_board': self.paramedic_on_board,
            'equipment_level': self.equipment_level,
            'in_service': self.in_service,
        }


class DispatchAssignment(Base):
    """
    Dispatch Assignment Tracking
    Links cases to ambulances and tracks the dispatch lifecycle
    """
    __tablename__ = 'dispatch_assignments'
    
    # Primary key
    assignment_id = Column(String(50), primary_key=True)
    
    # References
    case_id = Column(String(50), nullable=False)
    ambulance_id = Column(String(50), nullable=False)
    
    # Timing
    assigned_at = Column(DateTime, default=datetime.now, nullable=False)
    dispatched_at = Column(DateTime)
    en_route_at = Column(DateTime)
    arrived_at = Column(DateTime)
    transported_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Status
    status = Column(String(20), nullable=False, default='pending')
    # 'pending', 'dispatched', 'en_route', 'on_scene', 'transporting', 'completed', 'cancelled'
    
    # Location Details
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    pickup_address = Column(String(500), nullable=False)
    
    destination_latitude = Column(Float)
    destination_longitude = Column(Float)
    destination_address = Column(String(500))  # Hospital
    destination_hospital = Column(String(200))
    
    # Routing
    estimated_distance_km = Column(Float)
    estimated_time_minutes = Column(Integer)
    actual_response_time_minutes = Column(Integer)
    estimated_arrival_time = Column(DateTime)  # ETA datetime
    
    # Assignment Details
    priority = Column(String(20))  # 'critical', 'high', 'medium', 'low'
    assigned_by = Column(String(100))  # Dispatcher ID
    assignment_notes = Column(Text)
    
    # Ambulance & Instructions
    ambulance_type = Column(String(50))  # 'ALS' or 'BLS'
    prerarrival_instructions = Column(JSON)  # Chief complaint-wise instructions
    
    # Outcome
    patient_transported = Column(Boolean)
    outcome_notes = Column(Text)
    cancellation_reason = Column(Text)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'assignment_id': self.assignment_id,
            'case_id': self.case_id,
            'ambulance_id': self.ambulance_id,
            'status': self.status,
            'pickup_address': self.pickup_address,
            'destination_address': self.destination_address,
            'estimated_time_minutes': self.estimated_time_minutes,
            'actual_response_time_minutes': self.actual_response_time_minutes,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    # Resources
    database_size_mb = Column(Float)
    model_load_time_ms = Column(Float)


# Database initialization and session management
class DatabaseManager:
    """
    Manages database connections and operations
    """
    
    def __init__(self, db_uri=None):
        self.db_uri = db_uri or config.DATABASE_URI
        self.engine = create_engine(self.db_uri, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
        print(f"[OK] Database tables created at {config.DATABASE_PATH}")
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def drop_all_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(self.engine)
        print("⚠️  All tables dropped")


if __name__ == "__main__":
    # Initialize database
    print("=== Initializing Database ===\n")
    
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    # Test insert
    session = db_manager.get_session()
    
    test_case = TriageCase(
        case_id='TEST_001',
        patient_age=45,
        chief_complaint='Test case',
        pain_level=5,
        duration_hours=2.0,
        conscious_status=True,
        ml_risk_score=0.35,
        ml_confidence=0.80,
        ml_recommendation='non_emergency',
        routed_to='nurse',
        queue_priority='MEDIUM',
    )
    
    session.add(test_case)
    session.commit()
    
    print(f"[OK] Test case inserted: {test_case.case_id}")
    
    # Query back
    retrieved = session.query(TriageCase).filter_by(case_id='TEST_001').first()
    print(f"[OK] Test case retrieved: {retrieved.chief_complaint}")
    
    # Cleanup
    session.delete(retrieved)
    session.commit()
    session.close()
    
    print("\n✓ Database initialization complete")
