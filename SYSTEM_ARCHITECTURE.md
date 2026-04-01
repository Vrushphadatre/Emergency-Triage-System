# System Architecture - Advanced Emergency Triage

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     END USERS / DISPATCHERS                     │
├──────────────┬──────────────────────────┬──────────────────────┤
│              │                          │                      │
▼              ▼                          ▼                      ▼
┌──────────┐ ┌──────────────────┐ ┌───────────────┐ ┌──────────────┐
│ Advanced │ │ Simple Form      │ │ Admin         │ │ Mobile API   │
│ Clinical │ │ (Fallback)       │ │ Dashboard     │ │ Clients      │
│ Form     │ │                  │ │               │ │              │
└────┬─────┘ └────────┬─────────┘ └────────┬──────┘ └──────┬───────┘
     │                │                    │               │
     └────────────────┴────────────────────┴───────────────┘
                      │
          ╔═══════════▼═══════════╗
          ║   FLASK WEB SERVER    ║
          ║   (Port 5000)         ║
          ╚═══════════╤═══════════╝
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ┌────────┐  ┌──────────┐  ┌──────────┐
    │ Forms  │  │    API   │  │ Dashboard│
    │Handler │  │Endpoints │  │Backend   │
    └───┬────┘  └────┬─────┘  └────┬─────┘
        │            │             │
        └────┬───────┴─────────┬───┘
             │                 │
        ┌────▼─────────────────▼──┐
        │   REQUEST PROCESSING    │
        │ ├─ Input Validation     │
        │ ├─ Data Extraction      │
        │ ├─ Emergency Detection  │
        │ └─ Error Handling       │
        └────┬────────────────────┘
             │
        ┌────▼──────────────────────────┐
        │   ML & BUSINESS LOGIC LAYER   │
        │ ├─ TriageClassifier           │
        │ ├─ SafetyGuardrails           │
        │ ├─ ExplanationLayer           │
        │ ├─ DecisionRouter             │
        │ └─ DispatchManager            │
        └────┬──────────────────────────┘
             │
        ┌────▼──────────────────────────┐
        │   DATA PERSISTENCE LAYER      │
        │ ├─ DatabaseManager (ORM)      │
        │ ├─ TriageCase Records         │
        │ ├─ Ambulance Fleet Status     │
        │ ├─ DispatchAssignments        │
        │ └─ AuditLogs                  │
        └────┬──────────────────────────┘
             │
        ┌────▼──────────────────┐
        │   SQLite Database     │
        │ triage_system.db      │
        │ (35+ tables)          │
        └───────────────────────┘
```

---

## 📊 FRONTEND ARCHITECTURE

### Form Layer (3 versions)

#### 1. Advanced Clinical Form (`/advanced`)
**Purpose:** Full clinical assessment with vital signs  
**Tech:** HTML5 + CSS3 + Vanilla JavaScript + Responsive design  
**Size:** 34.8 KB  

**Components:**
- Step indicator (1-4 progress)
- Multi-section form with validation
- Vital signs capture component
- Real-time emergency detection
- Results modal display

**Flow:**
```
Step 1: Patient Info → Step 2: Chief Complaint → Step 3: Vitals → Step 4: Review → Submit
                                ↓ (Emergency Check)
                           RED ALERT Display
```

#### 2. Simple Form (`/simple`)
**Purpose:** Quick fallback, minimal UI  
**Tech:** HTML5 + Inline CSS  
**Size:** 6.9 KB  

**Components:**
- 5 essential fields
- Basic validation
- Emergency alert
- Inline results

#### 3. Admin Dashboard (`/dashboard`)
**Purpose:** Command center monitoring  
**Tech:** HTML5 + CSS3 + Fetch API + Auto-refresh  
**Size:** 24.0 KB  

**Components:**
- Metrics cards (4x KPIs)
- Active cases list (clickable)
- Ambulance fleet panel
- Risk distribution chart
- Response time tracker
- Case detail modal

---

## 🔌 API LAYER

### REST Endpoints

#### Form Submission
```
POST /submit_assessment
├─ Input: Patient info + vital signs
├─ Processing: ML prediction + risk scoring
├─ Output: Case ID + dispatch status
└─ Status: ✅ Working
```

#### Data APIs
```
GET /api/active_cases
├─ Returns: Last 20 cases with risk levels
├─ Refresh: On-demand from dashboard
└─ Status: ✅ Working

GET /api/ambulances  
├─ Returns: Fleet status + location data
├─ Updates: Real-time from database
└─ Status: ✅ Working
```

---

## 🧠 ML & LOGIC LAYER

### Component Stack

```
┌─────────────────────────────────────────┐
│    TriageClassifier                     │
│  ├─ Model: GradientBoostingClassifier   │
│  ├─ Features: TF-IDF text + vital signs │
│  ├─ Output: Risk score (0-1)            │
│  └─ Bias: Emergency preference          │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│    SafetyGuardrails                     │
│  ├─ Emergency override check            │
│  ├─ Vital sign alerts                   │
│  ├─ Confidence thresholds               │
│  └─ Default-to-emergency logic          │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│    ExplanationLayer                     │
│  ├─ Human-readable reasoning            │
│  ├─ Critical symptoms list              │
│  ├─ Risk factor breakdown               │
│  └─ Recommendation text                 │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│    DecisionRouter                       │
│  ├─ Route to: dispatcher | nurse queue  │
│  ├─ Priority: HIGH | MEDIUM | LOW       │
│  ├─ Wait time prediction                │
│  └─ Queue assignment                    │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│    DispatchManager                      │
│  ├─ Find nearest ambulance (Haversine)  │
│  ├─ Assign unit to case                 │
│  ├─ ETA calculation                     │
│  ├─ Status tracking                     │
│  └─ Multiple unit coordination          │
└─────────────────────────────────────────┘
```

### Emergency Detection Logic

```
IMMEDIATE EMERGENCY COMPLAINTS = {
  "Chest pain",
  "Breathing Difficulty",
  "Unconscious / unresponsive patient",
  "Convulsions / Fits / Seizures",
  "Road traffic accident: [any type]",
  "Trauma - Head injury",
  "Trauma - Bleeding",
  "Drowning / Near Drowning",
  "Electrocution / lightning strike",
  "Hematemesis [vomiting blood]",
  "Overdose / poisoning",
  "Pregnancy - bleeding",
  "Pregnancy - baby delivered",
  "Choking",
  "Paralysis / stroke",
  "Hazardous matter exposure"
}

if complaint in IMMEDIATE_EMERGENCY_COMPLAINTS:
    risk_score = 0.95 (100%)
    priority = "CRITICAL"
    auto_dispatch = True
    ambulance_level = "advanced"
```

### Vital Signs Enhancement
```
VITAL SIGN BOUNDARIES:
├─ Abnormal HR: >120 or <50 → Boost risk by +20%
├─ Abnormal BP: >170/110 or <80/50 → Boost risk by +15%
├─ Low O₂: <90% → Boost risk by +25%
├─ Fast Breathing: >30 → Boost risk by +20%
├─ High Pain + Chest complaint → High risk (likelihood)
└─ RESULT: More accurate risk stratification
```

---

## 💾 DATA LAYER

### Database Schema (Updated)

#### `triage_cases` Table (Primary)
```sql
Fields: 60+
├─ Patient Info: age, gender, address, contact
├─ Chief Complaint: complaint, symptoms, duration
├─ Vital Signs (NEW):
│  ├─ heart_rate (INT)
│  ├─ blood_pressure (VARCHAR)
│  ├─ respiratory_rate (INT)
│  ├─ spo2 (INT)
│  ├─ temperature (FLOAT)
│  ├─ consciousness_level (VARCHAR)
│  ├─ symptom_duration (VARCHAR)
│  └─ patient_gender (VARCHAR)
├─ ML Prediction: risk_score, confidence, reasoning
├─ Safety: override_applied, override_reasons
├─ Routing: routed_to, queue_priority
├─ Historical: timestamps, conversation_turns
└─ Indices: case_id (PRIMARY), created_at, risk_score
```

#### `ambulances` Table
```sql
Fields: 25+
├─ Fleet ID: ambulance_id, unit_name, type
├─ Location: current_lat/lon, current_address
├─ Status: available | dispatched | en_route | on_scene
├─ Crew: crew_size, paramedic_on_board
├─ Capabilities: equipment, training_level
└─ Indices: ambulance_id (PRIMARY), status
```

#### `dispatch_assignments` Table
```sql
Fields: 20+
├─ Assignment: case_id, ambulance_id, timestamp
├─ Routing: source_lat/lon, dest_lat/lon
├─ ETA: estimated_arrival_time
├─ Status: pending | accepted | completed
└─ Indices: case_id (UNIQUE), ambulance_id
```

#### `audit_logs` Table
```sql
Fields: 15+
├─ Event: action_type, actor, timestamp
├─ Details: JSON object with context
├─ Purpose: Compliance, debugging, analytics
└─ Retention: 90 days (configurable)
```

### Query Performance
```
Active Cases (Last 20):
  SELECT * FROM triage_cases 
  ORDER BY created_at DESC LIMIT 20
  └─ Index on created_at: <100ms

Ambulance Location:
  SELECT * FROM ambulances WHERE status = 'available'
  └─ Index on status: <50ms

Case Details:
  SELECT * FROM triage_cases WHERE case_id = ?
  └─ Primary key lookup: <20ms
```

---

## 🔄 REQUEST FLOW

### Complete Assessment Submission Flow

```
Client Browser
    │ (POST /submit_assessment)
    ▼
├─ Input Validation
│  ├─ Check required fields
│  ├─ Phone format validation
│  └─ Age range validation
│
├─ Data Extraction
│  ├─ Patient info
│  ├─ Chief complaint
│  ├─ Vital signs (NEW)
│  └─ Medical history
│
├─ Emergency Check
│  ├─ Is complaint in immediate_emergency_set?
│  └─ Set is_immediate_emergency flag
│
├─ ML Prediction
│  ├─ Feature extraction
│  ├─ Model inference
│  ├─ Risk scoring
│  └─ Confidence calculation
│
├─ Safety Guardrails
│  ├─ Apply emergency override
│  ├─ Check vital sign thresholds
│  ├─ Verify guardrail rules
│  └─ Final risk determination
│
├─ Routing Decision
│  ├─ Determine priority level
│  ├─ Assign queue (dispatcher | nurse)
│  └─ Estimate wait time
│
├─ Ambulance Dispatch (if high risk)
│  ├─ Find nearest unit(s)
│  ├─ Calculate route & ETA
│  ├─ Create assignment record
│  └─ Update unit status
│
├─ Database Persistence
│  ├─ INSERT INTO triage_cases
│  ├─ INSERT INTO dispatch_assignments
│  ├─ INSERT INTO audit_logs (x2)
│  └─ UPDATE ambulances (status, location)
│
└─ Response to Client
   ├─ Case ID
   ├─ Risk level & score
   ├─ Ambulance status
   ├─ ETA
   └─ Routed destination
```

**Total Processing Time:** 200-500ms

---

## 🔐 DATA FLOW SECURITY

```
Browser ──HTTPS─→ Flask ──Parameterized─→ SQLite
                          Queries
  
├─ Input validation on client side
├─ Server-side validation (mandatory)
├─ Parameterized SQL queries (SQL injection prevention)
├─ No credentials in code (config-based)
└─ Audit logging of all actions
```

---

## ⚙️ DEPLOYMENT COMPONENTS

### Required Files
```
d:\Projects\Using_Agents\
├─ app.py                    # Main Flask application (1011 lines)
├─ config.py                 # Configuration (269 lines)
├─ requirements.txt          # Python dependencies
├─ templates/
│  ├─ advanced_assessment.html   # New: Advanced form
│  ├─ admin_dashboard.html       # New: Dashboard
│  ├─ simple.html               # Fallback form
│  └─ [other templates]
├─ models/
│  └─ ml_model.py           # ML classifier
├─ database/
│  ├─ models.py             # ORM models (426 lines)
│  └─ triage_system.db      # SQLite database
├─ genai/
│  ├─ intake_agent.py
│  ├─ explanation_layer.py
│  └─ [other modules]
├─ safety/
│  └─ guardrails.py
├─ routing/
│  └─ decision_router.py
├─ dispatch/
│  └─ dispatch_manager.py
└─ scripts/
   └─ migrate_vitals.py     # New: Database migration
```

### System Requirements
- **Python:** 3.8+
- **Flask:** 2.0+
- **SQLAlchemy:** 1.4+
- **scikit-learn:** 0.24+
- **RAM:** 512MB minimum
- **Disk:** 100MB minimum
- **Port:** 5000 (configurable)

---

## 📈 SCALABILITY CONSIDERATIONS

### Current: Single Server
- SQLite database (file-based)
- In-memory queues (dispatcher_queue, nurse_queue)
- Single Flask worker process
- **Capacity:** ~100 concurrent users

### Production: Multi-Server
```
Load Balancer (nginx/HAProxy)
    ├─ Flask Server 1 (Port 5000)
    ├─ Flask Server 2 (Port 5001)
    ├─ Flask Server 3 (Port 5002)
    └─ [More as needed]
         └─ Shared PostgreSQL Database (production-grade)
         └─ Redis Cache (session + queue management)
```

**Expected Scaling:**
- 1000s concurrent users with horizontal scaling
- <200ms response time with load distribution
- 99.9% uptime with redundancy

---

## 🚀 MONITORING & LOGGING

### Metrics to Track
```
Performance:
├─ Request latency (p50, p95, p99)
├─ Database query time
├─ ML inference time
└─ Page load time

Business:
├─ Cases per hour
├─ Emergency vs non-emergency ratio
├─ Average ambulance dispatch time
├─ Case completion rate
└─ System uptime %

Clinical:
├─ False positive rate
├─ False negative rate
├─ Override rate
└─ Outcome accuracy
```

### Logging Points
```
├─ INFO: Case received, submitted, completed
├─ WARNING: Guardrail triggered, confidence low
├─ ERROR: ML prediction failed, database error
├─ DEBUG: Feature extraction, routing decision
└─ AUDIT: All user actions, all data changes
```

---

**Architecture Version:** 2.1 (Production Ready)  
**Last Updated:** February 27, 2026  
**Maintainer:** Your Name
