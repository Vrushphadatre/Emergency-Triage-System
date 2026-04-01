"""
Chief Complaint to Ambulance Type & Pre-arrival Instructions
Maps each complaint to required ambulance type (ALS/BLS) and dispatcher instructions
"""

from typing import Dict, Tuple

# ============================================================================
# AMBULANCE TYPE ASSIGNMENT BY COMPLAINT
# ============================================================================

# ALS = Advanced Life Support (Paramedics, full equipment)
# BLS = Basic Life Support (EMTs, basic equipment)

COMPLAINT_TO_AMBULANCE_TYPE = {
    # ========== CRITICAL - ALWAYS ALS ==========
    "Chest pain": "ALS",
    "Difficulty breathing": "ALS",
    "Stroke symptoms": "ALS",
    "Severe allergic reaction": "ALS",
    "Unconsciousness": "ALS",
    "Severe trauma": "ALS",
    "Multiple injuries": "ALS",
    "Choking": "ALS",
    "Severe bleeding": "ALS",
    "Cardiac arrest": "ALS",
    "Respiratory distress": "ALS",
    "Anaphylaxis": "ALS",
    "Overdose": "ALS",
    "Poisoning": "ALS",
    "Severe burn": "ALS",
    "Loss of consciousness": "ALS",
    "Paralysis": "ALS",
    "Seizure": "ALS",
    
    # ========== MODERATE - OFTEN ALS ==========
    "Abdominal pain (severe)": "ALS",
    "Chest discomfort": "ALS",
    "Head injury": "ALS",
    "Severe headache": "ALS",
    "Severe dizziness": "ALS",
    "Weakness/Numbness": "ALS",
    "Severe back pain": "ALS",
    "Suspected fracture (leg)": "ALS",
    "Heavy bleeding": "ALS",
    "Severe fever": "ALS",
    "Eye injury": "ALS",
    "Chemical exposure": "ALS",
    "Electric shock": "ALS",
    "Pregnancy complications": "ALS",
    
    # ========== ROUTINE - BLS ==========
    "Minor cut/wound": "BLS",
    "Abdominal pain (mild)": "BLS",
    "Headache": "BLS",
    "Dizziness": "BLS",
    "Nausea/Vomiting": "BLS",
    "Fever": "BLS",
    "Cough": "BLS",
    "Sore throat": "BLS",
    "Backache": "BLS",
    "Joint pain": "BLS",
    "Ankle sprain": "BLS",
    "Minor burn": "BLS",
    "Rash": "BLS",
    "Ear pain / Infection": "BLS",
    "Eye irritation": "BLS",
    "Muscle ache": "BLS",
    "Stomach pain": "BLS",
    "Muscle strain": "BLS",
    "Dental pain": "BLS",
    "Allergic reaction (mild)": "BLS",
    "Asthma attack (stable)": "BLS",
    "Diabetic issue (stable)": "BLS",
    "Fall (minor)": "BLS",
    "Finger/toe injury": "BLS",
    "Contact lens issue": "BLS",
    "Nosebleed (minor)": "BLS",
}

# Default to ALS for unknown complaints (safer)
DEFAULT_AMBULANCE_TYPE = "ALS"


def get_ambulance_type(chief_complaint: str) -> str:
    """
    Determine required ambulance type (ALS/BLS) based on chief complaint
    
    Args:
        chief_complaint: Patient's chief complaint
        
    Returns:
        'ALS' or 'BLS'
    """
    # Exact match
    if chief_complaint in COMPLAINT_TO_AMBULANCE_TYPE:
        return COMPLAINT_TO_AMBULANCE_TYPE[chief_complaint]
    
    # Check if complaint contains key terms indicating ALS needed
    als_keywords = [
        'chest', 'cardiac', 'heart', 'unconscious', 'unresponsive',
        'stroke', 'bleeding', 'trauma', 'severe', 'critical',
        'difficulty breathing', 'respiratory', 'respiratory distress',
        'overdose', 'poisoning', 'allergic reaction', 'shock',
        'seizure', 'paralysis', 'unconsciousness'
    ]
    
    complaint_lower = chief_complaint.lower()
    if any(keyword in complaint_lower for keyword in als_keywords):
        return "ALS"
    
    # Default to ALS for safety
    return DEFAULT_AMBULANCE_TYPE


# ============================================================================
# PRE-ARRIVAL INSTRUCTIONS (DISPATCHER TELLS PATIENT)
# ============================================================================

PRERARRIVAL_INSTRUCTIONS = {
    "Chest pain": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Have the patient sit down and rest",
            "Loosen any tight clothing",
            "If conscious and able, chew aspirin (if no allergy)",
            "If patient loses consciousness, prepare for CPR",
            "Keep doors and gates unlocked for ambulance access",
            "Have someone meet ambulance outside if possible"
        ],
        "do_not": [
            "Do NOT lie patient flat unless unconscious",
            "Do NOT give food or water",
            "Do NOT move patient unnecessarily"
        ],
        "monitor": [
            "Monitor breathing - is patient gasping or struggling to breathe?",
            "Monitor consciousness - does patient respond to voice?",
            "Watch for cold sweat, nausea, or radiation to arm/jaw"
        ]
    },
    
    "Difficulty breathing": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Help patient sit upright - this eases breathing",
            "Loosen all tight clothing around neck and chest",
            "If patient has rescue inhaler, help them use it",
            "Keep patient calm - anxiety worsens breathing",
            "If they have home oxygen, help them put it on",
            "Position near a window for fresh air if safe"
        ],
        "do_not": [
            "Do NOT lay them flat",
            "Do NOT panic - keep voice calm",
            "Do NOT leave patient alone"
        ],
        "monitor": [
            "Is breathing getting worse or better?",
            "Check for wheezing or high-pitched sounds",
            "Watch for blue lips, face, or fingernails"
        ]
    },
    
    "Unconsciousness": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Check for responsiveness - gently shake shoulders and call out",
            "Check for breathing - look, listen, feel",
            "If not breathing, start CPR if trained (30 compressions, 2 breaths)",
            "If breathing, place in recovery position (on side)",
            "Clear airway - remove vomit, food, or loose teeth",
            "Do NOT give anything to eat or drink"
        ],
        "do_not": [
            "Do NOT move unnecessarily (could have spine injury)",
            "Do NOT put anything in mouth",
            "Do NOT leave patient alone"
        ],
        "monitor": [
            "Is patient breathing? How fast?",
            "Check pulse at neck (carotid artery)",
            "Any seizure activity or muscle twitching?"
        ]
    },
    
    "Severe bleeding": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Apply direct pressure with clean cloth/gauze",
            "Do NOT remove cloth if it soaks through - add more on top",
            "Elevate bleeding area above heart if possible",
            "Apply pressure to pressure point if limb bleeding:",
            "  - Inner thigh for leg bleeding",
            "  - Upper arm for arm bleeding",
            "If bleeding is internal/abdominal: lying flat with knees bent",
            "Keep patient calm and warm"
        ],
        "do_not": [
            "Do NOT apply tourniquet unless life-threatening (last resort)",
            "Do NOT probe wound or remove embedded objects",
            "Do NOT move patient more than necessary"
        ],
        "monitor": [
            "Is bleeding slowing down with pressure?",
            "Is patient staying conscious?",
            "Any signs of shock: pale, sweaty, drowsy?"
        ]
    },
    
    "Stroke symptoms": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Note exact time symptoms started",
            "Have them smile - is one side drooping?",
            "Ask them to raise both arms - does one drift?",
            "Ask them to repeat simple sentence - is speech slurred?",
            "If ANY YES, likely stroke - time is critical",
            "Place patient lying down, head supported",
            "Keep airways clear",
            "Check for choking hazard - clear mouth"
        ],
        "do_not": [
            "Do NOT give food or water (swallowing may be impaired)",
            "Do NOT give medication unless prescribed",
            "Do NOT wait - stroke is a time-critical emergency"
        ],
        "monitor": [
            "Can patient feel touch on both sides of face?",
            "Any facial drooping, arm weakness, speech problems?",
            "Time symptoms started?"
        ]
    },
    
    "Paralysis / stroke": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Note exact time symptoms started",
            "Have them smile - is one side drooping?",
            "Ask them to raise both arms - does one drift?",
            "Ask them to repeat simple sentence - is speech slurred?",
            "If ANY YES, likely stroke - time is critical",
            "Place patient lying down, head supported",
            "Keep airways clear",
            "Check for choking hazard - clear mouth"
        ],
        "do_not": [
            "Do NOT give food or water (swallowing may be impaired)",
            "Do NOT give medication unless prescribed",
            "Do NOT wait - stroke is a time-critical emergency"
        ],
        "monitor": [
            "Can patient feel touch on both sides of face?",
            "Any facial drooping, arm weakness, speech problems?",
            "Time symptoms started?"
        ]
    },
    
    "Drowning / Near Drowning": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Get patient out of water - do NOT put back in water",
            "Check for breathing - if not breathing, start CPR",
            "Place in recovery position on side",
            "Remove wet clothing if possible",
            "Wrap in warm blanket for hypothermia prevention",
            "Keep airways clear - tilted head back position",
            "Do NOT give food/water - risk of aspiration"
        ],
        "do_not": [
            "Do NOT move unnecessarily (spinal injury risk)",
            "Do NOT assume patient is fine if they briefly stopped breathing",
            "Do NOT delay CPR if not breathing"
        ],
        "monitor": [
            "Is patient breathing? Any gasping or wheezing?",
            "Any blue lips or pale skin?",
            "Is patient conscious and alert?",
            "Any coughing up water?"
        ]
    },
    
    "Choking": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Ask 'Are you choking?' - if can't speak/cough, act immediately",
            "Stand behind patient, make a fist above navel",
            "Perform Heimlich maneuver: quick upward thrusts",
            "Repeat until object comes out or patient becomes unconscious",
            "If unconscious: start CPR, check mouth for object",
            "DO NOT pat on back - can lodge object deeper"
        ],
        "do_not": [
            "Do NOT do back blows - can lodge object deeper",
            "Do NOT panic - stay calm",
            "Do NOT assume they can breathe if partially responsive"
        ],
        "monitor": [
            "Is object coming out?",
            "Can patient breathe or speak?",
            "Patient staying conscious?"
        ]
    },
    
    "Severe burn": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Stop the burn: remove from heat source",
            "Cool the burn: apply cool water for 10-20 minutes",
            "Remove clothing/jewelry (if not stuck to skin)",
            "Cover with clean, dry dressing or sheet",
            "Elevate burned area above heart if possible",
            "Do NOT apply ice directly - causes more damage",
            "Keep patient warm with blanket (except burn area)"
        ],
        "do_not": [
            "Do NOT use ice directly on burn",
            "Do NOT apply butter, oil, or salves",
            "Do NOT burst blisters",
            "Do NOT remove clothing stuck to skin"
        ],
        "monitor": [
            "How large is the burned area?",
            "Any breathing difficulty?",
            "Is patient in severe pain?"
        ]
    },
    
    "Seizure": {
        "priority": "URGENT",
        "instructions": [
            "Move nearby objects away to prevent injury",
            "Do NOT restrain - let seizure happen",
            "Place pillow under head",
            "Turn head to side so saliva can drain",
            "Note time seizure started",
            "After seizure stops, place in recovery position",
            "Let patient rest - confusion is normal after seizure"
        ],
        "do_not": [
            "Do NOT put anything in mouth",
            "Do NOT give food or water until fully alert",
            "Do NOT restrain movements during seizure",
            "Do NOT panic if it lasts 5-10 minutes"
        ],
        "monitor": [
            "How long did seizure last?",
            "Does patient know where they are after?",
            "Any injuries from falling or hitting objects?"
        ]
    },
    
    "Severe allergic reaction": {
        "priority": "IMMEDIATE",
        "instructions": [
            "If patient has EpiPen, help them use it immediately",
            "Inject into outer thigh through clothing if needed",
            "After EpiPen, patient still needs hospital - don't refuse transport",
            "Lay patient down, elevate legs if breathing okay",
            "If having trouble breathing, sit upright",
            "Remove any tight clothing from neck area",
            "Keep patient calm and reassured"
        ],
        "do_not": [
            "Do NOT delay EpiPen use - seconds matter",
            "Do NOT assume patient is fine after EpiPen",
            "Do NOT give food or water",
            "Do NOT try to identify allergen - focus on treatment"
        ],
        "monitor": [
            "Any swelling of face, lips, or tongue?",
            "Difficulty breathing or wheezing?",
            "Skin reaction worsening or improving?",
            "Patient staying conscious and alert?"
        ]
    },
    
    "Severe trauma / Multiple injuries": {
        "priority": "IMMEDIATE",
        "instructions": [
            "Check scene safety - is it safe to help?",
            "Check for consciousness and breathing",
            "If unconscious, place in recovery position",
            "Control any heavy bleeding with pressure",
            "Do NOT move patient unless in danger",
            "Suspect spinal injury - minimize movement",
            "Keep patient warm with blankets",
            "Reassure patient that help is coming"
        ],
        "do_not": [
            "Do NOT move patient unless absolutely necessary",
            "Do NOT remove helmets or protective gear",
            "Do NOT probe wounds",
            "Do NOT assume injuries from appearance alone"
        ],
        "monitor": [
            "Is patient responsive and alert?",
            "Any heavy bleeding or open wounds?",
            "Any numbness, tingling, or paralysis?",
            "Any difficulty breathing or chest pain?"
        ]
    },
    
    "Headache": {
        "priority": "ROUTINE",
        "instructions": [
            "Help patient to quiet, dark room",
            "Apply cold compress to forehead or neck",
            "Have patient drink water - dehydration is common cause",
            "If patient has migraine medication, help them take it",
            "Avoid loud noises and bright lights",
            "Patient can rest or take over-the-counter pain relief"
        ],
        "do_not": [
            "Do NOT assume harmless if: worst headache ever, fever, stiff neck, vision changes, confusion"
        ],
        "monitor": [
            "Is this the worst headache patient ever had?",
            "Fever or stiff neck?",
            "Any vision changes or confusion?",
            "If yes to any, treat as EMERGENCY"
        ]
    },
    
    "Abdominal pain": {
        "priority": "ROUTINE",
        "instructions": [
            "Have patient lie down in comfortable position",
            "Knees bent may ease pain",
            "Warm (not hot) compress may help",
            "Have patient sip water if not vomiting",
            "Avoid food until seen by doctor",
            "Keep track of when pain started and what makes it better/worse"
        ],
        "do_not": [
            "Do NOT assume harmless if: severe pain, fever, vomiting, blood in stool, pain after trauma"
        ],
        "monitor": [
            "Severity 1-10?",
            "Any vomiting or blood in stool?",
            "Fever?",
            "Recent trauma or injury?",
            "If serious signs, escalate to ALS"
        ]
    },
    
    "Fever": {
        "priority": "ROUTINE",
        "instructions": [
            "Patient should rest in cool environment",
            "Encourage drinking water to prevent dehydration",
            "Light clothing and blankets as patient feels comfortable",
            "Lukewarm (not cold) compress for forehead",
            "Over-the-counter fever reducer acceptable (aspirin, ibuprofen)",
            "Monitor for any signs of serious infection"
        ],
        "do_not": [
            "Do NOT assume harmless if: very high fever (>104F), confusion, difficulty breathing, severe headache"
        ],
        "monitor": [
            "How high is temperature?",
            "Any other symptoms: cough, sore throat, body aches?",
            "Does patient seem confused or delirious?",
            "Any difficulty breathing?"
        ]
    },
}


def get_instructions(chief_complaint: str) -> Dict:
    """
    Get pre-arrival instructions for patient/dispatcher
    
    Args:
        chief_complaint: Patient's chief complaint
        
    Returns:
        Dictionary with instructions, or default message if not found
    """
    # Exact match first
    if chief_complaint in PRERARRIVAL_INSTRUCTIONS:
        return PRERARRIVAL_INSTRUCTIONS[chief_complaint]
    
    # Smart partial matching for common variations
    complaint_lower = chief_complaint.lower()
    
    # Create all possible partial matches
    for complaint_key, instructions in PRERARRIVAL_INSTRUCTIONS.items():
        complaint_key_lower = complaint_key.lower()
        
        # Check if key appears in complaint or complaint appears in key
        if complaint_key_lower in complaint_lower or complaint_lower in complaint_key_lower:
            return instructions
    
    # Check for keyword matches
    keyword_matches = {
        'stroke': 'Stroke symptoms',
        'paralysis': 'Paralysis / stroke',
        'seizure': 'Seizure',
        'drowning': 'Drowning / Near Drowning',
        'choking': 'Choking',
        'burn': 'Severe burn',
        'conscious': 'Unconsciousness',
        'unresponsive': 'Unconsciousness',
        'bleeding': 'Severe bleeding',
        'trauma': 'Severe trauma / Multiple injuries',
        'allerg': 'Severe allergic reaction',
    }
    
    for keyword, instruction_key in keyword_matches.items():
        if keyword in complaint_lower and instruction_key in PRERARRIVAL_INSTRUCTIONS:
            return PRERARRIVAL_INSTRUCTIONS[instruction_key]
    
    # Default for unknown complaints
    return {
        "priority": "STANDARD",
        "instructions": [
            "Keep patient comfortable and calm",
            "Do NOT move patient unnecessarily",
            "Have all medications and medical records ready"
        ],
        "do_not": [
            "Do NOT delay seeking medical care"
        ],
        "monitor": [
            "Watch for any changes in patient condition",
            "Is pain, breathing, or consciousness changing?"
        ]
    }
