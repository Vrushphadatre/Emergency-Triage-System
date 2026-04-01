"""
ETA Calculation Module
Calculates estimated time of arrival for ambulances
"""

import math
from typing import Tuple, Optional
from datetime import datetime, timedelta


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lon1: Ambulance latitude, longitude
        lat2, lon2: Patient latitude, longitude
        
    Returns:
        Distance in kilometers
    """
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    R = 6371  # Earth radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return distance


def calculate_eta(
    ambulance_lat: float,
    ambulance_lon: float,
    patient_lat: float,
    patient_lon: float,
    avg_speed_kmh: float = 40,
    response_delay_mins: float = 2.0
) -> Tuple[Optional[float], Optional[datetime]]:
    """
    Calculate ETA for ambulance to reach patient
    
    Args:
        ambulance_lat, ambulance_lon: Current ambulance location
        patient_lat, patient_lon: Patient location
        avg_speed_kmh: Average speed in km/h (default 40 for city)
        response_delay_mins: Seconds to dispatch/prepare (default 2 minutes)
        
    Returns:
        Tuple of (travel_time_minutes, eta_datetime) or (None, None) if coordinates missing
    """
    # Get distance
    distance_km = haversine_distance(ambulance_lat, ambulance_lon, patient_lat, patient_lon)
    
    if distance_km is None:
        return None, None
    
    # Calculate travel time
    travel_time_mins = (distance_km / avg_speed_kmh) * 60
    
    # Add response delay
    total_time_mins = travel_time_mins + response_delay_mins
    
    # Calculate ETA
    now = datetime.now()
    eta = now + timedelta(minutes=total_time_mins)
    
    return round(total_time_mins, 1), eta


def get_eta_text(minutes: Optional[float]) -> str:
    """
    Convert minutes to readable text
    
    Args:
        minutes: Number of minutes
        
    Returns:
        Readable text like "5-7 minutes"
    """
    if minutes is None:
        return "Unable to calculate"
    
    if minutes < 1:
        return "Less than 1 minute"
    elif minutes < 2:
        return "1-2 minutes"
    elif minutes < 5:
        return f"{int(minutes)} minutes"
    elif minutes < 10:
        return f"6-10 minutes"
    elif minutes < 15:
        return f"10-15 minutes"
    elif minutes < 20:
        return f"15-20 minutes"
    else:
        return f"{int(minutes)}+ minutes"


def is_urgent_based_on_eta(minutes: Optional[float]) -> bool:
    """
    Determine if case is urgent based on ETA to patient
    Used to bump priority if ambulance response slow
    
    Args:
        minutes: ETA in minutes
        
    Returns:
        True if ETA > 15 minutes (may need to escalate instructions)
    """
    if minutes is None:
        return False
    
    return minutes > 15
