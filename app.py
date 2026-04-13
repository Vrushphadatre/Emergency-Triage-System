"""
Main Flask Application
Emergency Triage Decision Support System MVP
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import uuid
from datetime import datetime
import sys
from pathlib import Path
import json
import requests

# Add project root to path
sys.path.append(str(Path(__file__).parent))

import config
from models.ml_model import TriageClassifier
from genai.intake_agent import IntakeAgent
from genai.explanation_layer import ExplanationLayer
from safety.guardrails import SafetyGuardrails
from routing.decision_router import DecisionRouter
from database.models import DatabaseManager, TriageCase, AuditLog, KPIMetric, Ambulance, DispatchAssignment
from dispatch.dispatch_manager import DispatchManager, initialize_sample_ambulances
from dispatch.complaint_mapping import get_ambulance_type, get_instructions
from dispatch.eta_calculator import calculate_eta, get_eta_text
from dispatch.translations import get_text, translate_complaint

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = config.SESSION_TYPE

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize components
db_manager = DatabaseManager()
ml_classifier = TriageClassifier()
explanation_layer = ExplanationLayer()
safety_guardrails = SafetyGuardrails()
router = DecisionRouter()
dispatch_manager = DispatchManager()

# Global state for active cases (in production, use Redis)
active_cases = {}
dispatcher_queue = []
nurse_queue = []


# ============================================================================
# PARAMETER MAPPER - Handle different naming conventions
# ============================================================================

def map_incoming_parameters(data):
    """
    Map incoming parameters (camelCase) to system parameters (snake_case)
    Handles both naming conventions from different client systems
    """
    mapped = {}
    
    # Direct mappings (incoming_name -> system_name)
    mappings = {
        'patientName': 'patient_name',
        'patient_name': 'patient_name',
        
        'mobileNo': 'callback_phone',
        'mobile_no': 'callback_phone',
        'callback_phone': 'callback_phone',
        'phone': 'callback_phone',
        
        'patientGender': 'patient_gender',
        'patient_gender': 'patient_gender',
        'gender': 'patient_gender',
        
        'incAddress': 'patient_address',
        'patient_address': 'patient_address',
        'address': 'patient_address',
        
        'incLat': 'patient_address_latitude',
        'patient_address_latitude': 'patient_address_latitude',
        'latitude': 'patient_address_latitude',
        
        'incLong': 'patient_address_longitude',
        'patient_address_longitude': 'patient_address_longitude',
        'longitude': 'patient_address_longitude',
        
        'chiefComplaint': 'chief_complaint',
        'chief_complaint': 'chief_complaint',
        
        'associatedSymptoms': 'medical_history',
        'associated_symptoms': 'medical_history',
        'medical_history': 'medical_history',
        'symptoms': 'medical_history',
        
        'durationChiefComplaint': 'symptom_duration',
        'duration_chief_complaint': 'symptom_duration',
        'symptom_duration': 'symptom_duration',
        'duration': 'symptom_duration',
        
        'medicalHistory': 'medical_history',
        'callerName': 'caller_name',
        'caller_name': 'caller_name',
        'patientKnown': 'patient_known',
        'patient_known': 'patient_known',
        'isUnidentified': 'is_unidentified',
        'is_unidentified': 'is_unidentified',
        'language': 'language',
    }
    
    # Map parameters
    for incoming_key, system_key in mappings.items():
        if incoming_key in data:
            mapped[system_key] = data[incoming_key]
    
    # Handle age special case - supports Years, Months, and Days
    if 'patientAge' in data or 'patient_age' in data:
        age_value = data.get('patientAge') or data.get('patient_age')
        # Check for unit from different field names
        age_unit = (data.get('patientAgeUnit') or data.get('patient_age_unit') or 
                    data.get('patientAgeType') or data.get('patient_age_type') or 'years').lower()
        
        try:
            age_float = float(age_value) if age_value else 0
            
            if age_unit == 'months' or age_unit == 'month':
                # Input is months - store as-is
                total_months = int(age_float)
                mapped['patient_age_months'] = int(age_float % 12)
                mapped['patient_age_years'] = int(age_float // 12)
                mapped['age_in_months'] = total_months
            elif age_unit == 'days' or age_unit == 'day':
                # Convert days to months (30 days per month)
                total_months = int(age_float / 30)
                mapped['patient_age_months'] = int(total_months % 12)
                mapped['patient_age_years'] = int(total_months // 12)
                mapped['age_in_months'] = total_months
            else:  # Default to years
                age_years = int(age_float)
                mapped['patient_age_years'] = age_years
                mapped['patient_age_months'] = 0
                mapped['age_in_months'] = age_years * 12  # Convert to months for ML
        except (ValueError, TypeError):
            mapped['patient_age_years'] = 0
            mapped['patient_age_months'] = 0
            mapped['age_in_months'] = 0
    
    return mapped


# ============================================================================
# STARTUP
# ============================================================================

def initialize_system():
    """Initialize system"""
    global ml_classifier
    
    print("=" * 70)
    print("EMERGENCY TRIAGE DECISION SUPPORT SYSTEM - MVP")
    print("=" * 70)
    
    # Load ML model
    try:
        ml_classifier.load()
        print("✓ ML model loaded successfully")
    except FileNotFoundError:
        print("⚠️  ML model not found. Training new model...")
        # Generate training data if needed
        from data.synthetic_training_data import generate_training_data
        training_path = config.DATA_DIR / "training_data.csv"
        if not training_path.exists():
            generate_training_data(num_samples=1000, output_path=training_path)
        
        # Train model
        ml_classifier.train(training_path)
        ml_classifier.save()
        print("✓ New ML model trained and saved")
    
    # Initialize sample ambulances
    db_session = db_manager.get_session()
    initialize_sample_ambulances(db_session)
    db_session.close()
    
    print(f"[OK] Database ready at {config.DATABASE_PATH}")
    print(f"[OK] Server starting on http://localhost:{config.FLASK_PORT}")
    print("=" * 70)


# ============================================================================
# PATIENT INTAKE ROUTES
# ============================================================================

@app.route('/')
def index():
    """Patient intake landing page"""
    return render_template('intake.html')


@app.route('/test')
def test():
    """Test page - simple HTML"""
    return render_template('test.html')


@app.route('/simple')
def simple():
    """Simplified intake form"""
    return render_template('simple.html')


@app.route('/advanced')
def advanced():
    """Advanced clinical assessment form with vital signs"""
    return render_template('advanced_assessment.html')


@app.route('/dashboard')
def dashboard():
    """Admin dispatch dashboard"""
    return render_template('admin_dashboard.html')


@app.route('/api/active_cases')
def api_active_cases():
    """Get all active cases for dashboard"""
    db_session = db_manager.get_session()
    try:
        # Get recent cases (last 50)
        cases = db_session.query(TriageCase).order_by(TriageCase.created_at.desc()).limit(20).all()
        
        cases_data = []
        for c in cases:
            # Get ambulance type and instructions for this case
            ambulance_type = get_ambulance_type(c.chief_complaint)
            instructions = get_instructions(c.chief_complaint)
            
            # Format age from separate years/months columns
            age_display = f"{c.patient_age_years} years {c.patient_age_months} months" if (c.patient_age_years or c.patient_age_months) else '0 years 0 months'
            
            cases_data.append({
                'case_id': c.case_id,
                'patient_name': c.caller_name or 'Unknown',
                'patient_age_years': c.patient_age_years or 0,
                'patient_age_months': c.patient_age_months or 0,
                'patient_age_display': age_display,
                'patient_gender': c.patient_gender or 'Not specified',
                'chief_complaint': c.chief_complaint or '- N/A -',
                'callback_phone': c.callback_phone or 'N/A',
                'patient_address': c.patient_address or 'Unknown',
                'risk_level': 'high' if c.ml_risk_score >= 0.65 else ('moderate' if c.ml_risk_score >= 0.40 else 'low'),
                'risk_score': c.ml_risk_score or 0,
                'medical_history': c.medical_history or '',
                'ambulance_assigned': False,  # Will update this when dispatch info is added
                'estimated_arrival_time': None,
                'ambulance_type': ambulance_type,  # NEW: ALS or BLS
                'prerarrival_instructions': instructions,  # NEW: Instructions
                'created_at': c.created_at.isoformat() if c.created_at else None
            })
        
        return jsonify({'cases': cases_data})
    except Exception as e:
        print(f"ERROR in api_active_cases: {str(e)}")
        return jsonify({'cases': [], 'error': str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/ambulances')
def api_ambulances():
    """Get ambulance fleet status"""
    db_session = db_manager.get_session()
    try:
        ambulances = db_session.query(Ambulance).filter(Ambulance.in_service == True).all()
        
        ambulances_data = [{
            'ambulance_id': a.ambulance_id,
            'unit_name': a.unit_name,
            'vehicle_type': a.vehicle_type,  # ALS or BLS
            'status': a.status or 'Available',
            'location': a.current_address or a.station_address or 'Base Station',
            'latitude': a.current_latitude or a.station_latitude,
            'longitude': a.current_longitude or a.station_longitude,
            'crew_size': a.crew_size,
            'fuel_level': a.fuel_level
        } for a in ambulances]
        
        return jsonify({'ambulances': ambulances_data})
    except Exception as e:
        print(f"ERROR in api_ambulances: {str(e)}")
        return jsonify({'ambulances': [], 'error': str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/dispatch_assignments')
def api_dispatch_assignments():
    """Get current dispatch assignments linking cases to ambulances"""
    db_session = db_manager.get_session()
    try:
        assignments = db_session.query(DispatchAssignment).filter(
            DispatchAssignment.status.in_([
                'pending', 'dispatched', 'en_route', 'on_scene', 'transporting'
            ])
        ).all()
        
        assignments_data = [{
            'assignment_id': a.assignment_id,
            'case_id': a.case_id,
            'ambulance_id': a.ambulance_id,
            'status': a.status,
            'estimated_time_minutes': a.estimated_time_minutes,
            'estimated_distance_km': a.estimated_distance_km,
            'pickup_address': a.pickup_address,
            'priority': a.priority,
            'assigned_at': a.assigned_at.isoformat() if a.assigned_at else None
        } for a in assignments]
        
        return jsonify({'assignments': assignments_data})
    except Exception as e:
        print(f"ERROR in api_dispatch_assignments: {str(e)}")
        return jsonify({'assignments': [], 'error': str(e)}), 500
    finally:
        db_session.close()


@app.route('/start_intake', methods=['POST'])
def start_intake():
    """Initialize a new patient intake session"""
    # Create new case ID
    case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    # Initialize intake agent
    agent = IntakeAgent()
    first_question = agent.start_intake()
    
    # Store in session
    session['case_id'] = case_id
    session['intake_start_time'] = datetime.now().isoformat()
    
    # Store agent state
    active_cases[case_id] = {
        'agent': agent,
        'status': 'intake_in_progress',
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'case_id': case_id,
        'question': first_question,
        'status': 'started'
    })


@app.route('/submit_response', methods=['POST'])
def submit_response():
    """Process patient response and get next question"""
    data = request.json
    
    # Get case_id from request body or session
    case_id = data.get('case_id') or session.get('case_id')
    user_response = data.get('response', '')
    
    if not case_id or case_id not in active_cases:
        return jsonify({'error': 'Invalid session or case_id'}), 400
    
    # Get agent
    agent = active_cases[case_id]['agent']
    
    # Process response
    result = agent.process_response(user_response)
    
    # Check if complete or emergency
    if result['is_complete'] or result.get('immediate_emergency'):
        # Move to triage phase
        return complete_intake(case_id, agent, result)
    
    # Return next question
    return jsonify({
        'next_question': result['next_question'],
        'is_complete': False
    })


@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    """
    Process form-based assessment with patient details, chief complaint, and symptoms
    ENHANCED: Support for unknown/unidentified patients + real-time emergency detection
    Handles multiple parameter naming conventions
    """
    
    # Map incoming parameters to system format
    raw_data = request.json
    data = map_incoming_parameters(raw_data)
    
    # COMPREHENSIVE EMERGENCY COMPLAINT CLASSIFICATION
    # Based on emergency triage protocols for all 86+ complaint types
    
    IMMEDIATE_EMERGENCY_COMPLAINTS = {
        # CRITICAL AIRWAY/BREATHING (Life-threatening - minutes matter)
        "Breathing Difficulty",
        "Choking",
        "Drowning / Near Drowning",
        
        # CRITICAL CHEST CONDITIONS
        "Chest pain",
        "Hematemesis [vomiting blood]",
        
        # CRITICAL NEUROLOGICAL
        "Unconscious / unresponsive patient",
        "Convulsions / Fits / Seizures",
        "Paralysis / stroke",
        "Confusion or altered mental status",
        
        # CRITICAL TRAUMA
        "Trauma - Head injury",
        "Trauma - Bleeding",
        "Trauma - Gunshot injury",
        "Trauma - abdominal",
        "Trauma - chest wall",
        
        # CRITICAL ACCIDENTS
        "RTA (Road Traffic Accident)",
        "Road traffic accident: general",
        "Road traffic accident: vehicle on fire",
        "Road traffic accident: pinned / struck patient",
        "Road traffic accident: vehicle off bridge/height",
        "Road traffic accident: auto - pedestrian",
        "Road traffic accident: Pregnant lady",
        "Accident of boat/ship",
        "Fall from Height",
        
        # CRITICAL ENVIRONMENTAL/TOXIC
        "Electrocution / lightning strike",
        "Hazardous matter exposure",
        "Overdose / poisoning",
        "Heat stroke",
        
        # CRITICAL PREGNANCY
        "Pregnancy - baby delivered",
        "Pregnancy - bleeding",
        "Pregnancy - abdominal pain / labor pain",
        
        # CRITICAL OTHER
        "Suicide attempt",
        "Attack / Assault",
    }
    
    MODERATE_EMERGENCY_COMPLAINTS = {
        # SERIOUS BUT NOT IMMEDIATELY LIFE-THREATENING
        # (Needs urgent evaluation but not immediate resuscitation)
        
        "Burns",
        "Animal Bite",
        "Allergic reaction",
        "Giddiness / Fainting",
        "Abnormal Behavior [Delirium]",
        "Pain in abdomen / stomach",  # Severe abdominal pain
        "Vomiting",  # Severe vomiting
        "Loosemotion-Vomiting",  # Severe dehydration
        "Low sugar level",  # Hypoglycemia
        "Low body temperature",  # Severe hypothermia
        "Hypertension",  # Severe uncontrolled hypertension
        "Psychiatric problems",  # Severe psychiatric crisis
        "Eye pain",  # Trauma to eye
        "Child patient / Pediatric patient",  # Flag for special care
    }
    
    # Create case ID
    case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    # Extract patient information using mapped parameters
    patient_name = data.get('patient_name', 'Patient')
    caller_name = data.get('caller_name', '')  # For unknown patient reports
    callback_phone = data.get('callback_phone', '')
    patient_address = data.get('Location / Address', '')  # New field name format
    patient_age_years = data.get('patient_age_years', 0)
    patient_age_months = data.get('patient_age_months', 0)
    patient_age_in_months = data.get('age_in_months', 0)
    patient_gender = data.get('patient_gender', '')
    patient_known = data.get('patient_known', True)
    is_unidentified = data.get('is_unidentified', False)
    chief_complaint = data.get('chief_complaint', '')
    medical_history = data.get('medical_history', '')
    language = data.get('language', 'en')
    symptom_duration = data.get('symptom_duration', '')
    
    # VALIDATION: Patient name must contain only letters, spaces, and hyphens
    if patient_name and not all(c.isalpha() or c.isspace() or c == '-' for c in patient_name):
        return jsonify({'error': 'Patient name can only contain letters, spaces, and hyphens (no numbers or special characters)'}), 400
    
    # VALIDATION: Phone number must be 10 digits, no letters
    if callback_phone and not (len(str(callback_phone)) == 10 and str(callback_phone).isdigit()):
        return jsonify({'error': 'Phone number must be exactly 10 digits (0-9 only)'}), 400
    
    # VALIDATION: Age must be 0-150 years
    if patient_age_years and (patient_age_years < 0 or patient_age_years > 150):
        return jsonify({'error': 'Age must be between 0 and 150 years'}), 400
    
    # Extract geolocation data with new field names and validate
    patient_lat = data.get('incLat')  # Incident Latitude
    patient_lon = data.get('incLong')  # Incident Longitude
    
    # VALIDATION: Latitude must be between -90 and 90
    if patient_lat is not None:
        try:
            patient_lat = float(patient_lat)
            if patient_lat < -90 or patient_lat > 90:
                return jsonify({'error': 'Latitude must be between -90 and 90 degrees'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid latitude value'}), 400
    
    # VALIDATION: Longitude must be between -180 and 180
    if patient_lon is not None:
        try:
            patient_lon = float(patient_lon)
            if patient_lon < -180 or patient_lon > 180:
                return jsonify({'error': 'Longitude must be between -180 and 180 degrees'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid longitude value'}), 400
    
    # Check emergency classifications
    is_immediate_emergency = chief_complaint in IMMEDIATE_EMERGENCY_COMPLAINTS
    is_moderate_emergency = chief_complaint in MODERATE_EMERGENCY_COMPLAINTS
    
    # Prepare case data for ML model
    case_data = {
        'case_id': case_id,
        'patient_name': patient_name,
        'caller_name': caller_name if not patient_known else '',  # NEW
        'phone': callback_phone,
        'address': patient_address,
        'age': int(patient_age_in_months) if patient_age_in_months else 0,  # Use normalized months
        'gender': patient_gender,  # NEW
        'chief_complaint': chief_complaint,
        'history': medical_history,
        'transcript': f"Chief Complaint: {chief_complaint}\nMedical History: {medical_history}\nLocation: {patient_address}",
        'language': language,
        'is_immediate_emergency': is_immediate_emergency,  # NEW FLAG
        'is_moderate_emergency': is_moderate_emergency,  # NEW FLAG
        'is_unidentified_patient': is_unidentified  # NEW FLAG
    }
    
    # Get location data - prefer geolocation from patient, fall back to default (Seattle, WA)
    default_lat = 47.6062
    default_lon = -122.3321
    
    # Use geolocation if captured from form, otherwise use default
    final_lat = float(patient_lat) if patient_lat is not None else default_lat
    final_lon = float(patient_lon) if patient_lon is not None else default_lon
    
    try:
        # ML prediction using chief complaint
        ml_prediction = ml_classifier.predict(case_data)
        
        # EMERGENCY OVERRIDES - Based on severity level
        if is_immediate_emergency:
            # IMMEDIATE LIFE-THREATENING - Force maximum risk
            ml_prediction['risk_score'] = 0.95
            ml_prediction['is_emergency'] = True
            ml_prediction['reasoning'] = f"IMMEDIATE EMERGENCY: {chief_complaint} - Auto-dispatch initiated"
            ml_prediction['confidence'] = 1.0
        elif is_moderate_emergency:
            # SERIOUS BUT URGENT - Boost risk score significantly
            ml_prediction['risk_score'] = max(ml_prediction['risk_score'], 0.75)
            ml_prediction['is_emergency'] = True
            ml_prediction['reasoning'] = f"URGENT: {chief_complaint} - Requires immediate evaluation"
            ml_prediction['confidence'] = 0.95
        
        # Apply safety guardrails
        final_prediction = safety_guardrails.enforce_emergency_override(
            case_data, ml_prediction
        )
        
        # Generate explanation
        explanation = explanation_layer.explain_risk_score(case_data, final_prediction)
        
        # Route case
        routing_decision = router.route_case(final_prediction, case_data)
        
        # Determine risk level for response
        risk_level = 'high' if final_prediction['risk_score'] >= 0.65 else (
            'moderate' if final_prediction['risk_score'] >= 0.40 else 'low'
        )
        
        # Store in database
        db_session = db_manager.get_session()
        
        triage_case = TriageCase(
            case_id=case_id,
            patient_age_years=int(patient_age_years) if patient_age_years else 0,
            patient_age_months=int(patient_age_months) if patient_age_months else 0,
            patient_gender=patient_gender,
            chief_complaint=chief_complaint,
            transcript=case_data.get('transcript'),
            duration_hours=0,
            medical_history=medical_history,
            # Location fields - use geolocation if captured, otherwise default
            inc_lat=final_lat,
            inc_long=final_lon,
            patient_address=patient_address if patient_address else 'Address not provided',
            patient_city='City',
            patient_state='State',
            callback_phone=callback_phone,
            caller_name=caller_name if not patient_known else patient_name,
            # ML prediction
            ml_risk_score=final_prediction['risk_score'],
            ml_confidence=final_prediction['confidence'],
            ml_recommendation='emergency' if final_prediction['is_emergency'] else 'non_emergency',
            ml_reasoning=final_prediction['reasoning'],
            safety_override_applied=final_prediction.get('safety_override', False) or is_immediate_emergency,
            safety_override_reasons=final_prediction.get('safety_overrides'),
            routed_to=routing_decision['queue'],
            queue_priority=routing_decision['priority'],
            intake_duration_seconds=1,
            conversation_turns=1,
            assessment_language=language
        )
        
        db_session.add(triage_case)
        
        # Audit log
        audit_entry = AuditLog(
            case_id=case_id,
            action_type='assessment_submitted',
            actor=caller_name if not patient_known else patient_name,  # NEW
            action_details={
                'chief_complaint': chief_complaint,
                'medical_history': medical_history,
                'is_immediate_emergency': is_immediate_emergency,  # NEW
                'is_unidentified_patient': is_unidentified,  # NEW
                'patient_known': patient_known,  # NEW
                'ml_prediction': final_prediction,
                'routing': routing_decision
            }
        )
        db_session.add(audit_entry)
        
        db_session.commit()
        
        # No automatic dispatch - only submit cases to system
        ambulance_assigned = False
        estimated_arrival_time = None
        ambulance_type = None
        prerarrival_instructions = None
        
        db_session.close()
        
        # Add to appropriate queue
        queue_entry = {
            'case_id': case_id,
            'case_data': case_data,
            'prediction': final_prediction,
            'explanation': explanation,
            'routing': routing_decision,
            'is_immediate_emergency': is_immediate_emergency,  # NEW
            'is_unidentified_patient': is_unidentified,  # NEW
            'timestamp': datetime.now().isoformat()
        }
        
        if routing_decision['queue'] == 'dispatcher':
            dispatcher_queue.append(queue_entry)
        else:
            nurse_queue.append(queue_entry)
        
        # Return response
        response_data = {
            'case_id': case_id,
            'patient_name': patient_name,
            'patient_age_years': int(patient_age_years) if patient_age_years else 0,
            'patient_age_months': int(patient_age_months) if patient_age_months else 0,
            'patient_age_display': f"{int(patient_age_years) if patient_age_years else 0} years {int(patient_age_months) if patient_age_months else 0} months",
            'patient_age_in_months': patient_age_in_months,
            'patient_gender': patient_gender,
            'chief_complaint': chief_complaint,
            'callback_phone': callback_phone,
            'patient_address': patient_address,
            'patient_address_latitude': final_lat,
            'patient_address_longitude': final_lon,
            'risk_score': final_prediction['risk_score'],
            'risk_level': risk_level,
            'recommendation': final_prediction['recommendation'],
            'routed_to': routing_decision['queue'],
            'explanation': explanation if not is_immediate_emergency else f"🚨 IMMEDIATE EMERGENCY - {chief_complaint}",
            'estimated_wait': routing_decision['estimated_wait_minutes'],
            'ambulance_assigned': ambulance_assigned,
            'estimated_arrival_time': estimated_arrival_time,
            'is_immediate_emergency': is_immediate_emergency,
            'is_unidentified_patient': is_unidentified
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Error in submit_assessment: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error processing assessment: {str(e)}'}), 500


def complete_intake(case_id, agent, intake_result):
    """Complete intake and move to ML triage"""
    # Get extracted data
    case_data = intake_result['extracted_data']
    case_data['case_id'] = case_id
    
    # ML prediction
    ml_prediction = ml_classifier.predict(case_data)
    
    # Apply safety guardrails
    final_prediction = safety_guardrails.enforce_emergency_override(
        case_data, ml_prediction
    )
    
    # Generate explanation
    explanation = explanation_layer.explain_risk_score(case_data, final_prediction)
    
    # Route case
    routing_decision = router.route_case(final_prediction, case_data)
    
    # Store in database
    db_session = db_manager.get_session()
    
    # Default location (Seattle, WA) - in production, collect from caller or use GPS
    default_lat = 47.6062
    default_lon = -122.3321
    
    triage_case = TriageCase(
        case_id=case_id,
        patient_age=case_data.get('age'),
        chief_complaint=case_data.get('chief_complaint'),
        transcript=case_data.get('transcript'),
        pain_level=case_data.get('pain_level'),
        duration_hours=case_data.get('duration_hours'),
        conscious_status=case_data.get('conscious'),
        medical_history=case_data.get('history'),
        # Location fields (use defaults for now)
        inc_lat=case_data.get('latitude', default_lat),
        inc_long=case_data.get('longitude', default_lon),
        patient_address=case_data.get('address', 'Address not provided'),
        patient_city=case_data.get('city', 'Seattle'),
        patient_state=case_data.get('state', 'WA'),
        callback_phone=case_data.get('phone', ''),
        # ML prediction
        ml_risk_score=final_prediction['risk_score'],
        ml_confidence=final_prediction['confidence'],
        ml_recommendation='emergency' if final_prediction['is_emergency'] else 'non_emergency',
        ml_reasoning=final_prediction['reasoning'],
        safety_override_applied=final_prediction.get('safety_override', False),
        safety_override_reasons=final_prediction.get('safety_overrides'),
        routed_to=routing_decision['queue'],
        queue_priority=routing_decision['priority'],
        intake_duration_seconds=agent.current_question_idx * 30,  # Estimate
        conversation_turns=len(agent.conversation_history),
    )
    
    db_session.add(triage_case)
    
    # Audit log
    audit_entry = AuditLog(
        case_id=case_id,
        action_type='case_created',
        actor='system',
        action_details={
            'ml_prediction': final_prediction,
            'routing': routing_decision
        }
    )
    db_session.add(audit_entry)
    
    db_session.commit()
    db_session.close()
    
    # Add to appropriate queue
    queue_entry = {
        'case_id': case_id,
        'case_data': case_data,
        'prediction': final_prediction,
        'explanation': explanation,
        'routing': routing_decision,
        'timestamp': datetime.now().isoformat()
    }
    
    if routing_decision['queue'] == 'dispatcher':
        dispatcher_queue.append(queue_entry)
    else:
        nurse_queue.append(queue_entry)
    
    # Update active cases
    active_cases[case_id]['status'] = 'pending_review'
    active_cases[case_id]['prediction'] = final_prediction
    active_cases[case_id]['routing'] = routing_decision
    
    return jsonify({
        'is_complete': True,
        'case_id': case_id,
        'risk_score': final_prediction['risk_score'],
        'recommendation': final_prediction['recommendation'],
        'routed_to': routing_decision['queue'],
        'explanation': explanation,
        'estimated_wait': routing_decision['estimated_wait_minutes']
    })


# ============================================================================
# DISPATCHER CONSOLE ROUTES
# ============================================================================

@app.route('/dispatcher')
def dispatcher_console():
    """Dispatcher console view"""
    return render_template('dispatcher.html')


@app.route('/dispatcher/queue', methods=['GET'])
def get_dispatcher_queue():
    """Get current dispatcher queue"""
    # Sort by priority
    sorted_queue = sorted(
        dispatcher_queue,
        key=lambda x: (
            0 if x['routing']['priority'] == 'CRITICAL' else
            1 if x['routing']['priority'] == 'HIGH' else 2
        )
    )
    
    return jsonify({
        'queue': sorted_queue,
        'count': len(sorted_queue)
    })


@app.route('/dispatcher/decision', methods=['POST'])
def dispatcher_decision():
    """Record dispatcher decision"""
    data = request.json
    case_id = data.get('case_id')
    decision = data.get('decision')  # 'dispatch_ambulance' or 'refer_to_nurse'
    operator_id = data.get('operator_id', 'dispatcher_001')
    notes = data.get('notes', '')
    
    # Update database
    db_session = db_manager.get_session()
    
    case = db_session.query(TriageCase).filter_by(case_id=case_id).first()
    if case:
        case.human_decision = decision
        case.human_decision_by = operator_id
        case.human_decision_at = datetime.now()
        case.completed_at = datetime.now()
        
        if decision == 'dispatch_ambulance':
            case.final_disposition = 'ambulance_dispatched'
        else:
            case.final_disposition = 'referred_to_nurse'
        
        # Check if override
        if decision == 'refer_to_nurse' and case.ml_recommendation == 'emergency':
            case.human_override = True
            case.human_override_reason = notes
        
        # Audit log
        audit = AuditLog(
            case_id=case_id,
            action_type='human_decision',
            actor=operator_id,
            action_details={'decision': decision, 'notes': notes}
        )
        db_session.add(audit)
        
        db_session.commit()
    
    db_session.close()
    
    # Remove from queue
    global dispatcher_queue
    dispatcher_queue = [c for c in dispatcher_queue if c['case_id'] != case_id]
    
    return jsonify({'status': 'success', 'message': 'Decision recorded'})


# ============================================================================
# NURSE QUEUE ROUTES
# ============================================================================

@app.route('/nurse')
def nurse_console():
    """Nurse queue view"""
    return render_template('nurse.html')


@app.route('/nurse/queue', methods=['GET'])
def get_nurse_queue():
    """Get current nurse queue"""
    return jsonify({
        'queue': nurse_queue,
        'count': len(nurse_queue)
    })


@app.route('/nurse/decision', methods=['POST'])
def nurse_decision():
    """Record nurse decision"""
    data = request.json
    case_id = data.get('case_id')
    decision = data.get('decision')
    nurse_id = data.get('nurse_id', 'nurse_001')
    notes = data.get('notes', '')
    
    # Update database
    db_session = db_manager.get_session()
    
    case = db_session.query(TriageCase).filter_by(case_id=case_id).first()
    if case:
        case.human_decision = decision
        case.human_decision_by = nurse_id
        case.human_decision_at = datetime.now()
        case.completed_at = datetime.now()
        case.final_disposition = decision
        
        # Check if escalating to emergency
        if decision == 'escalate_to_emergency' and case.ml_recommendation == 'non_emergency':
            case.human_override = True
            case.human_override_reason = notes
        
        # Audit log
        audit = AuditLog(
            case_id=case_id,
            action_type='human_decision',
            actor=nurse_id,
            action_details={'decision': decision, 'notes': notes}
        )
        db_session.add(audit)
        
        db_session.commit()
    
    db_session.close()
    
    # Remove from queue
    global nurse_queue
    nurse_queue = [c for c in nurse_queue if c['case_id'] != case_id]
    
    return jsonify({'status': 'success', 'message': 'Decision recorded'})


# ============================================================================
# KPI DASHBOARD ROUTES
# ============================================================================


@app.route('/dashboard/metrics', methods=['GET'])
def get_metrics():
    """Get current KPI metrics"""
    db_session = db_manager.get_session()
    
    # Get all cases
    all_cases = db_session.query(TriageCase).all()
    completed_cases = [c for c in all_cases if c.completed_at is not None]
    
    # Calculate metrics
    total_cases = len(all_cases)
    emergency_cases = len([c for c in all_cases if c.ml_recommendation == 'emergency'])
    non_emergency_cases = total_cases - emergency_cases
    
    # Accuracy (where we have ground truth)
    verified_cases = [c for c in completed_cases if c.outcome_verified]
    if verified_cases:
        correct = len([c for c in verified_cases 
                       if (c.ml_recommendation == 'emergency') == c.actual_emergency])
        accuracy = (correct / len(verified_cases)) * 100
    else:
        accuracy = None
    
    # False negatives (critical metric)
    false_negatives = len([c for c in verified_cases 
                          if c.ml_recommendation == 'non_emergency' and c.actual_emergency])
    
    # Human override rate
    overrides = len([c for c in completed_cases if c.human_override])
    override_rate = (overrides / len(completed_cases) * 100) if completed_cases else 0
    
    # Average handling time
    handling_times = [c.total_handling_time_seconds for c in completed_cases 
                     if c.total_handling_time_seconds]
    avg_handling_time = (sum(handling_times) / len(handling_times)) if handling_times else 180
    
    db_session.close()
    
    metrics = {
        'total_cases': total_cases,
        'emergency_cases': emergency_cases,
        'non_emergency_cases': non_emergency_cases,
        'accuracy_pct': round(accuracy, 1) if accuracy else 'N/A',
        'false_negatives': false_negatives,
        'override_rate_pct': round(override_rate, 1),
        'avg_handling_time_seconds': round(avg_handling_time),
        'current_queue_lengths': {
            'dispatcher': len(dispatcher_queue),
            'nurse': len(nurse_queue)
        }
    }
    
    return jsonify(metrics)


# ============================================================================
# UTILITY ROUTES
# ============================================================================

@app.route('/health')
def health_check():
    """System health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ml_model_loaded': ml_classifier.is_trained,
        'database_connected': True,
        'active_cases': len(active_cases)
    })


@app.route('/api/case/<case_id>')
def get_case_details(case_id):
    """Get detailed information about a specific case"""
    db_session = db_manager.get_session()
    case = db_session.query(TriageCase).filter_by(case_id=case_id).first()
    
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    case_dict = case.to_dict()
    db_session.close()
    
    return jsonify(case_dict)


# ============================================================================
# DISPATCH & AMBULANCE MANAGEMENT
# ============================================================================

@app.route('/dispatch_map')
def dispatch_map():
    """Dispatch map and ambulance management interface"""
    return render_template('dispatch_map.html')


@app.route('/api/ambulances')
def get_ambulances():
    """Get list of all ambulances with their status"""
    db_session = db_manager.get_session()
    ambulances = db_session.query(Ambulance).all()
    
    result = [amb.to_dict() for amb in ambulances]
    db_session.close()
    
    return jsonify(result)


@app.route('/api/ambulances/<ambulance_id>')
def get_ambulance_details(ambulance_id):
    """Get details of a specific ambulance"""
    db_session = db_manager.get_session()
    ambulance = db_session.query(Ambulance).filter_by(ambulance_id=ambulance_id).first()
    
    if not ambulance:
        return jsonify({'error': 'Ambulance not found'}), 404
    
    result = ambulance.to_dict()
    db_session.close()
    
    return jsonify(result)


@app.route('/api/find_nearest_ambulance', methods=['POST'])
def find_nearest_ambulance_api():
    """Find nearest available ambulance to a location"""
    data = request.json
    
    patient_lat = data.get('latitude')
    patient_lon = data.get('longitude')
    
    if not patient_lat or not patient_lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    db_session = db_manager.get_session()
    result = dispatch_manager.find_nearest_ambulance(patient_lat, patient_lon, db_session)
    
    if result:
        ambulance, distance, eta = result
        response = {
            'ambulance': ambulance.to_dict(),
            'distance_km': round(distance, 2),
            'eta_minutes': eta
        }
        db_session.close()
        return jsonify(response)
    else:
        db_session.close()
        return jsonify({'error': 'No ambulances available'}), 404


@app.route('/api/dispatch', methods=['POST'])
def dispatch_ambulance():
    """Assign an ambulance to a case"""
    data = request.json
    
    case_id = data.get('case_id')
    ambulance_id = data.get('ambulance_id')
    dispatcher_id = data.get('dispatcher_id', 'dispatcher_1')
    priority = data.get('priority', 'high')
    notes = data.get('notes', '')
    
    if not case_id or not ambulance_id:
        return jsonify({'error': 'case_id and ambulance_id required'}), 400
    
    db_session = db_manager.get_session()
    
    # Get case and ambulance
    case = db_session.query(TriageCase).filter_by(case_id=case_id).first()
    ambulance = db_session.query(Ambulance).filter_by(ambulance_id=ambulance_id).first()
    
    if not case:
        db_session.close()
        return jsonify({'error': 'Case not found'}), 404
    
    if not ambulance:
        db_session.close()
        return jsonify({'error': 'Ambulance not found'}), 404
    
    if ambulance.status != 'available':
        db_session.close()
        return jsonify({'error': 'Ambulance not available'}), 400
    
    # Create dispatch assignment
    assignment = dispatch_manager.assign_ambulance(
        case, ambulance, db_session, dispatcher_id, priority, notes
    )
    
    # Update case status
    case.final_disposition = 'ambulance_dispatched'
    db_session.commit()
    
    # Log action
    audit_log = AuditLog(
        case_id=case_id,
        action_type='ambulance_dispatched',
        actor=dispatcher_id,
        action_details={
            'assignment_id': assignment.assignment_id,
            'ambulance_id': ambulance_id,
            'eta_minutes': assignment.estimated_time_minutes
        }
    )
    db_session.add(audit_log)
    db_session.commit()
    
    result = assignment.to_dict()
    db_session.close()
    
    return jsonify(result)


@app.route('/api/dispatch/<assignment_id>/status', methods=['PUT'])
def update_dispatch_status(assignment_id):
    """Update dispatch assignment status"""
    data = request.json
    new_status = data.get('status')
    notes = data.get('notes')
    
    if not new_status:
        return jsonify({'error': 'status required'}), 400
    
    db_session = db_manager.get_session()
    
    try:
        dispatch_manager.update_dispatch_status(assignment_id, new_status, db_session, notes)
        db_session.close()
        return jsonify({'success': True, 'message': f'Status updated to {new_status}'})
    except ValueError as e:
        db_session.close()
        return jsonify({'error': str(e)}), 404


@app.route('/api/active_dispatches')
def get_active_dispatches():
    """Get all active dispatch assignments"""
    db_session = db_manager.get_session()
    assignments = dispatch_manager.get_active_dispatches(db_session)
    
    result = [assignment.to_dict() for assignment in assignments]
    db_session.close()
    
    return jsonify(result)


@app.route('/api/dispatch_summary')
def get_dispatch_summary():
    """Get dispatch operations summary"""
    db_session = db_manager.get_session()
    summary = dispatch_manager.get_dispatch_summary(db_session)
    db_session.close()
    
    return jsonify(summary)


@app.route('/fetch_incident_data', methods=['POST'])
def fetch_incident_data():
    """
    Sync with external incident data from Apollo EMS
    """
    import requests
    
    try:
        # Step A: Call external API to get incident data
        external_api_url = 'https://apolloems.in/api/getIncAiData'
        
        # Send POST request to external API
        response = requests.post(external_api_url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch from external API'}), 400
        
        # Step B: Get the data
        incident_data = response.json()
        
        # Step C: Map external data to your system format
        mapped_data = {
            'patientName': incident_data.get('patient_name', 'Unknown'),
            'patientAge': incident_data.get('patient_age', 0),
            'patientAgeUnit': 'years',
            'mobileNo': incident_data.get('phone', '0000000000'),
            'patientGender': incident_data.get('gender', 'M'),
            'incAddress': incident_data.get('address', ''),
            'incLat': incident_data.get('latitude', 0),
            'incLong': incident_data.get('longitude', 0),
            'chiefComplaint': incident_data.get('complaint', ''),
            'medicalHistory': incident_data.get('medical_history', ''),
        }
        
        # Step D: Create case in your system
        # (Use your existing parameter mapper and submit logic)
        data = map_incoming_parameters(mapped_data)
        case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Save to database (simplified)
        case = TriageCase(
            case_id=case_id,
            patient_name=data.get('patient_name', 'Patient'),
            patient_age_years=data.get('patient_age_years', 0),
            patient_age_months=data.get('patient_age_months', 0),
            chief_complaint=data.get('chief_complaint', ''),
            # ... add other fields
        )
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'case_id': case_id,
            'message': 'Incident data fetched and case created'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Ensure database is initialized
    db_manager.create_tables()
    
    # Initialize system
    initialize_system()
    
    # Run app
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
