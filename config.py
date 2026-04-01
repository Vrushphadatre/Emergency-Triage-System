"""
Configuration file for Emergency Triage Decision Support System
All safety thresholds, model parameters, and system settings
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models" / "saved_models"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, DATABASE_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DATABASE_PATH = DATABASE_DIR / "triage_system.db"
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

# ============================================================================
# ML MODEL CONFIGURATION
# ============================================================================
MODEL_PATH = MODELS_DIR / "triage_classifier.pkl"
VECTORIZER_PATH = MODELS_DIR / "feature_vectorizer.pkl"
FAISS_INDEX_PATH = MODELS_DIR / "symptom_index.faiss"

# Classification Thresholds (Conservative, Emergency-Biased)
EMERGENCY_THRESHOLD = 0.60  # Risk score >= 0.60 → Emergency (lowered for better separation)
CONFIDENCE_THRESHOLD = 0.70  # Confidence < 0.70 → Recommend human review

# Model Training Parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# ============================================================================
# SAFETY GUARDRAILS (NON-NEGOTIABLE)
# ============================================================================
# Mandatory escalation keywords - immediate emergency flag
CRITICAL_SYMPTOMS = [
    # Respiration
    "can't breathe",
    "difficulty breathing",
    "shortness of breath",
    "choking",
    "no breathing",
    
    # Cardiac
    "chest pain",
    "chest pressure",
    "chest tightness",
    "heart attack",
    "cardiac",
    
    # Neurological  
    "unconscious",
    "unresponsive",
    "stroke",
    "slurred speech",
    "face drooping",
    "arm weakness",
    "paralysis",
    
    # Seizures
    "seizure",
    "convulsion",
    "fits",
    "fitting",
    
    # Hemorrhage
    "severe bleeding",
    "heavy bleeding",
    "vomiting blood",
    "coughing blood",
    "uncontrolled bleeding",
    
    # Toxins
    "overdose",
    "poisoning",
    "toxic",
    "electrocution",
    
    # Trauma
    "pinned",
    "crushing",
    "trapped",
    "gunshot",
    "head trauma",
    
    # Behavioral
    "suicide",
    "self harm",
    "violent",
    "attacking",
    
    # Drowning
    "drowning",
    "water inhalation",
    
    # Critical pregnancy
    "baby delivered",
    "delivery",
    "labor",
    "bleeding pregnant",
    "ruptured",
]

# High-risk symptoms requiring elevated attention (score boost)
HIGH_RISK_SYMPTOMS = [
    # Pain
    "severe pain",
    "acute pain",
    "unbearable pain",
    
    # Trauma (non-critical)
    "fallen",
    "fallen from height",
    "broken bone",
    "fracture",
    "head injury",
    "wound",
    "burn",
    "animal bite",
    
    # Neurological (non-stroke)
    "confusion",
    "altered mental",
    "delirium",
    "altered consciousness",
    "dizzy",
    "fainting",
    "loss of consciousness",
    
    # GI
    "severe vomiting",
    "severe diarrhea",
    "abdominal pain",
    "stomach pain",
    
    # Pregnancy/OB
    "pregnant",
    "pregnancy",
    "abdominal pain pregnant",
    "vaginal bleeding",
    
    # Metabolic  
    "low sugar",
    "hypoglycemia",
    "low temperature",
    "hypothermia",
    
    # Allergic
    "allergic reaction",
    "anaphylaxis",
    "swelling face",
    
    # Environmental
    "heat stroke",
    "severe heat",
    "exposure",
    "hazardous",
    
    # Other urgent
    "asthma attack",
    "breathing",
    "fever high",
    "severe infection",
]

# ============================================================================
# GENAI CONFIGURATION
# ============================================================================
# Local LLM Model (CPU-optimized)
LLM_MODEL_NAME = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
LLM_MODEL_FILE = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
LLM_MODEL_TYPE = "mistral"

# Generation Parameters
LLM_MAX_TOKENS = 512
LLM_TEMPERATURE = 0.3  # Lower = more conservative/predictable
LLM_TOP_P = 0.85
LLM_CONTEXT_LENGTH = 4096

# Embeddings for FAISS (CPU-friendly)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================================================
# INTAKE AGENT CONFIGURATION
# ============================================================================
# Maximum conversation turns before forcing conclusion
MAX_INTAKE_TURNS = 15

# Required fields for complete intake
REQUIRED_INTAKE_FIELDS = [
    "chief_complaint",
    "symptom_duration",
    "pain_level",
    "conscious_status",
    "patient_age",
]

# Structured intake questions (ordered)
INTAKE_QUESTIONS = [
    "What is the main reason for your call today?",
    "When did these symptoms start?",
    "On a scale of 1-10, how severe is the pain or discomfort?",
    "Is the patient conscious and able to respond?",
    "What is the patient's age?",
    "Does the patient have any chronic medical conditions?",
    "Is the patient taking any medications?",
    "Has this happened before?",
]

# ============================================================================
# ROUTING LOGIC
# ============================================================================
# Case routing rules based on risk score
ROUTING_RULES = {
    "emergency": {
        "min_score": 0.65,
        "queue": "dispatcher",
        "priority": "HIGH",
        "sla_minutes": 2,
    },
    "non_emergency": {
        "max_score": 0.64,
        "queue": "nurse",
        "priority": "MEDIUM",
        "sla_minutes": 15,
    },
}

# ============================================================================
# KPI TARGETS
# ============================================================================
KPI_TARGETS = {
    "non_emergency_reduction_pct": 30.0,
    "emergency_accuracy_pct": 95.0,
    "false_negative_rate_pct": 2.0,
    "avg_handling_time_minutes": 3.0,
    "human_override_rate_pct": 10.0,
}

# ============================================================================
# WEB APPLICATION CONFIGURATION
# ============================================================================
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True  # Set to False in production

# Session Configuration
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "emergency-triage-mvp-secret-key-change-in-production")
SESSION_TYPE = "filesystem"

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "triage_system.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# COMPLIANCE & AUDIT
# ============================================================================
# Retention periods (days)
AUDIT_LOG_RETENTION_DAYS = 2555  # ~7 years for healthcare compliance
FEEDBACK_DATA_RETENTION_DAYS = 730  # 2 years for model retraining

# Anonymization
ANONYMIZE_PATIENT_DATA = True
PII_FIELDS = ["patient_name", "phone_number", "address", "ssn"]

# ============================================================================
# DEMO MODE CONFIGURATION
# ============================================================================
DEMO_MODE = False  # Enable with --demo flag
DEMO_CASES_COUNT = 50
DEMO_AUTO_POPULATE = True

# ============================================================================
# FEATURE FLAGS
# ============================================================================
ENABLE_VOICE_TRANSCRIPTION = False  # Phase 2
ENABLE_MULTILINGUAL = False  # Phase 2
ENABLE_CAD_INTEGRATION = False  # Phase 2
ENABLE_BIAS_MONITORING = True  # MVP
ENABLE_REAL_TIME_DASHBOARD = True  # MVP

# ============================================================================
# MODEL RETRAINING CONFIGURATION
# ============================================================================
RETRAIN_FREQUENCY_DAYS = 30
MIN_FEEDBACK_SAMPLES = 100  # Minimum cases before retraining
RETRAIN_ACCURACY_THRESHOLD = 0.90  # Minimum accuracy to deploy new model

# ============================================================================
# VALIDATION RULES
# ============================================================================
INPUT_VALIDATION = {
    "max_text_length": 2000,
    "min_text_length": 10,
    "allowed_characters": "alphanumeric + punctuation",
    "require_json_output": True,
}

OUTPUT_VALIDATION = {
    "require_risk_score": True,
    "require_confidence": True,
    "require_explanation": True,
    "max_explanation_length": 500,
}

# ============================================================================
# ERROR HANDLING
# ============================================================================
# When system errors occur, default behavior
ERROR_DEFAULT_BEHAVIOR = "escalate_to_emergency"  # Safety first
ERROR_NOTIFICATION_ENABLED = True
ERROR_MAX_RETRIES = 3

# ============================================================================
# MONITORING & ALERTING
# ============================================================================
# Alert thresholds
ALERT_FALSE_NEGATIVE_THRESHOLD = 0.03  # Alert if >3% false negatives
ALERT_SYSTEM_DOWNTIME_SECONDS = 300  # Alert if system down >5 min
ALERT_AVG_RESPONSE_TIME_SECONDS = 10  # Alert if response >10 sec

# Health check interval
HEALTH_CHECK_INTERVAL_SECONDS = 60

# ============================================================================
# EXPLANABILITY REQUIREMENTS
# ============================================================================
EXPLANATION_MIN_LENGTH = 50  # Minimum characters for explanation
EXPLANATION_REQUIRED_ELEMENTS = [
    "risk_level",  # "high", "medium", "low"
    "key_symptoms",  # List of symptoms that influenced the score
    "confidence_note",  # Note about model confidence
]

# ============================================================================
# EXPORT SETTINGS
# ============================================================================
EXPORT_FORMATS = ["csv", "json"]
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

print(f"[OK] Configuration loaded successfully")
print(f"  - Database: {DATABASE_PATH}")
print(f"  - Model Path: {MODEL_PATH}")
print(f"  - Emergency Threshold: {EMERGENCY_THRESHOLD}")
print(f"  - Critical Symptoms: {len(CRITICAL_SYMPTOMS)} keywords")
