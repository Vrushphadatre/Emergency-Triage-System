"""
Synthetic Training Data Generator for Emergency Triage System
Generates realistic emergency vs non-emergency call scenarios for model training
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Emergency cases with high-risk symptoms
EMERGENCY_CASES = [
    {
        "chief_complaint": "severe chest pain and pressure",
        "symptoms": ["chest pain", "shortness of breath", "sweating", "nausea"],
        "duration_hours": 0.5,
        "pain_level": 9,
        "conscious": True,
        "age": 58,
        "history": "high blood pressure, diabetes",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "can't breathe properly",
        "symptoms": ["difficulty breathing", "wheezing", "chest tightness"],
        "duration_hours": 1,
        "pain_level": 8,
        "conscious": True,
        "age": 42,
        "history": "asthma",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "patient unresponsive",
        "symptoms": ["unconscious", "not responding", "fell down"],
        "duration_hours": 0.1,
        "pain_level": 10,
        "conscious": False,
        "age": 72,
        "history": "heart disease",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "severe bleeding from arm",
        "symptoms": ["severe bleeding", "cut", "pale", "dizzy"],
        "duration_hours": 0.2,
        "pain_level": 8,
        "conscious": True,
        "age": 28,
        "history": "none",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "stroke symptoms",
        "symptoms": ["slurred speech", "face drooping", "arm weakness", "confusion"],
        "duration_hours": 0.5,
        "pain_level": 6,
        "conscious": True,
        "age": 68,
        "history": "hypertension",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "having a seizure",
        "symptoms": ["convulsions", "seizure", "shaking", "loss of consciousness"],
        "duration_hours": 0.1,
        "pain_level": 10,
        "conscious": False,
        "age": 15,
        "history": "epilepsy",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
]

# Non-emergency cases
NON_EMERGENCY_CASES = [
    {
        "chief_complaint": "Headache",
        "symptoms": ["headache"],
        "duration_hours": 0,
        "pain_level": 0,
        "conscious": True,
        "age": 24,
        "history": "none",
        "outcome": "non_emergency",
        "final_disposition": "self_care_advised",
    },
    {
        "chief_complaint": "mild headache for two days",
        "symptoms": ["headache", "tired", "slight nausea"],
        "duration_hours": 48,
        "pain_level": 4,
        "conscious": True,
        "age": 34,
        "history": "migraines occasionally",
        "outcome": "non_emergency",
        "final_disposition": "nurse_callback",
    },
    {
        "chief_complaint": "sprained ankle yesterday",
        "symptoms": ["swollen ankle", "bruising", "limping"],
        "duration_hours": 24,
        "pain_level": 5,
        "conscious": True,
        "age": 22,
        "history": "none",
        "outcome": "non_emergency",
        "final_disposition": "self_care_advised",
    },
    {
        "chief_complaint": "minor cut needs cleaning",
        "symptoms": ["small cut", "bleeding stopped", "needs bandage"],
        "duration_hours": 2,
        "pain_level": 2,
        "conscious": True,
        "age": 12,
        "history": "none",
        "outcome": "non_emergency",
        "final_disposition": "self_care_advised",
    },
    {
        "chief_complaint": "runny nose and cough",
        "symptoms": ["cough", "runny nose", "sore throat", "low fever"],
        "duration_hours": 72,
        "pain_level": 3,
        "conscious": True,
        "age": 29,
        "history": "none",
        "outcome": "non_emergency",
        "final_disposition": "clinic_referral",
    },
    {
        "chief_complaint": "upset stomach",
        "symptoms": ["stomach ache", "bloating", "mild nausea"],
        "duration_hours": 12,
        "pain_level": 4,
        "conscious": True,
        "age": 41,
        "history": "none",
        "outcome": "non_emergency",
        "final_disposition": "nurse_callback",
    },
]

# Borderline cases (for model training complexity)
BORDERLINE_CASES = [
    {
        "chief_complaint": "severe abdominal pain",
        "symptoms": ["sharp stomach pain", "vomiting", "fever"],
        "duration_hours": 6,
        "pain_level": 8,
        "conscious": True,
        "age": 35,
        "history": "none",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
    {
        "chief_complaint": "twisted knee with swelling",
        "symptoms": ["knee pain", "swelling", "can't walk"],
        "duration_hours": 3,
        "pain_level": 7,
        "conscious": True,
        "age": 26,
        "history": "previous knee surgery",
        "outcome": "non_emergency",
        "final_disposition": "urgent_care_referral",
    },
    {
        "chief_complaint": "pregnancy complications",
        "symptoms": ["pregnant", "cramping", "spotting", "worried"],
        "duration_hours": 2,
        "pain_level": 6,
        "conscious": True,
        "age": 28,
        "history": "pregnant 7 months",
        "outcome": "emergency",
        "final_disposition": "ambulance_dispatched",
    },
]


def generate_training_data(num_samples=500, output_path=None):
    """
    Generate synthetic training data for the ML model
    
    Args:
        num_samples: Total number of samples to generate
        output_path: Path to save the CSV file
    
    Returns:
        pandas.DataFrame with training data
    """
    all_cases = []
    
    # Calculate distribution (60% non-emergency, 30% emergency, 10% borderline)
    num_emergency = int(num_samples * 0.30)
    num_non_emergency = int(num_samples * 0.60)
    num_borderline = num_samples - num_emergency - num_non_emergency
    
    # Generate emergency cases
    for _ in range(num_emergency):
        base_case = random.choice(EMERGENCY_CASES)
        case = generate_variant(base_case)
        all_cases.append(case)
    
    # Generate non-emergency cases
    for _ in range(num_non_emergency):
        base_case = random.choice(NON_EMERGENCY_CASES)
        case = generate_variant(base_case)
        all_cases.append(case)
    
    # Generate borderline cases
    for _ in range(num_borderline):
        base_case = random.choice(BORDERLINE_CASES)
        case = generate_variant(base_case)
        all_cases.append(case)
    
    # Shuffle
    random.shuffle(all_cases)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_cases)
    
    # Add timestamps
    base_time = datetime.now() - timedelta(days=180)
    df['timestamp'] = [base_time + timedelta(hours=i*2) for i in range(len(df))]
    
    # Save to file if path provided
    if output_path:
        df.to_csv(output_path, index=False)
        print(f"[OK] Generated {len(df)} training samples")
        print(f"  - Emergency: {len(df[df['outcome'] == 'emergency'])}")
        print(f"  - Non-Emergency: {len(df[df['outcome'] == 'non_emergency'])}")
        print(f"  - Saved to: {output_path}")
    
    return df


def generate_variant(base_case):
    """Create a variant of a base case with slight modifications"""
    case = base_case.copy()
    
    # Add some natural variation
    case['pain_level'] = max(1, min(10, case['pain_level'] + random.randint(-1, 1)))
    case['duration_hours'] = case['duration_hours'] * random.uniform(0.8, 1.2)
    case['age'] = max(1, case['age'] + random.randint(-5, 5))
    
    # Combine symptoms into a text transcript
    symptoms_text = ", ".join(case['symptoms'])
    case['transcript'] = f"{case['chief_complaint']}. Symptoms include: {symptoms_text}. " \
                        f"Pain level {case['pain_level']}/10. Duration: {case['duration_hours']:.1f} hours."
    
    return case


def generate_emergency_keywords():
    """Generate the emergency keywords database for FAISS"""
    keywords = {
        "critical_immediate": [
            "chest pain", "chest pressure", "heart attack", 
            "can't breathe", "difficulty breathing", "shortness of breath",
            "unconscious", "unresponsive", "not breathing",
            "severe bleeding", "heavy bleeding", "blood gushing",
            "stroke", "slurred speech", "face drooping",
            "seizure", "convulsion", "shaking uncontrollably",
            "suicide", "want to die", "overdose", "took too many pills",
            "poisoning", "swallowed chemicals",
        ],
        "high_priority": [
            "severe pain", "excruciating pain", "worst pain ever",
            "broken bone", "bone sticking out", "deformed limb",
            "head injury", "hit head hard", "lost consciousness briefly",
            "pregnant bleeding", "pregnancy pain", "labor pains",
            "allergic reaction", "swelling throat", "can't swallow",
            "vomiting blood", "blood in stool", "blood in urine",
            "high fever", "fever over 103", "baby won't wake up",
        ],
        "moderate_priority": [
            "fallen", "fell down", "injured in fall",
            "dizzy", "lightheaded", "feeling faint",
            "confusion", "disoriented", "not making sense",
            "severe vomiting", "can't keep anything down",
            "severe diarrhea", "dehydrated",
            "eye injury", "can't see", "vision problems",
            "burn", "scalded", "chemical burn",
        ],
    }
    
    return keywords


if __name__ == "__main__":
    # Generate training data
    output_dir = Path(__file__).parent
    training_data_path = output_dir / "training_data.csv"
    
    df = generate_training_data(num_samples=1000, output_path=training_data_path)
    
    # Generate emergency keywords
    keywords = generate_emergency_keywords()
    keywords_path = output_dir / "emergency_keywords.json"
    
    with open(keywords_path, 'w') as f:
        json.dump(keywords, f, indent=2)
    
    print(f"[OK] Generated emergency keywords database")
    print(f"  - Saved to: {keywords_path}")
    
    print("\n=== Data Generation Complete ===")
