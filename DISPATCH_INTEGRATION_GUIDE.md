"""
AMBULANCE DISPATCH SYSTEM - INTEGRATION GUIDE
Complete flow from patient form → ambulance dispatch
"""

# ============================================================================
# CURRENT ARCHITECTURE
# ============================================================================

CURRENT_FLOW = """
1. PATIENT SUBMITS FORM (advanced_assessment.html)
   ↓
2. POST /submit_assessment (app.py)
   ├── Extract patient data
   ├── ML classification (risk score)
   ├── Get ALS/BLS type (complaint_mapping.py)
   ├── Get instructions (prerarrival_instructions)
   ├── Store TriageCase in database
   └── Return case details to form
   ↓
3. DASHBOARD LOADS (admin_dashboard.html)
   ├── Fetch /api/active_cases
   ├── Display patient cards
   ├── Show risk level, complaint, instructions
   └── Show ambulance type needed
"""

# ============================================================================
# WHAT WE NEED TO ADD - DISPATCH LOGIC
# ============================================================================

MISSING_INTEGRATION = """
✗ MISSING: Auto-assign ambulance when high-risk case submitted
✗ MISSING: Track ambulance location on dashboard  
✗ MISSING: Show ambulance → patient → hospital route
✗ MISSING: Real-time status (Dispatched → En Route → On Scene)
✗ MISSING: Ambulance notifications/alerts
"""

# ============================================================================
# COMPLETE INTEGRATED FLOW
# ============================================================================

INTEGRATED_FLOW = """
┌─────────────────────────────────────────────────────────────────────┐
│                    PATIENT SUBMITS CASE                            │
│              (advanced_assessment.html form)                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  BACKEND: /submit_assessment                         │
│                          (app.py)                                    │
│                                                                      │
│  1. Extract: name, age, phone, address, complaint, medical_history  │
│  2. ML Classification → risk_score, risk_level                      │
│  3. Get ALS/BLS type → ambulance_type                               │
│  4. Get instructions → prerarrival_instructions                      │
│  5. Store TriageCase in database                                    │
│                                                                      │
│  *** NEW: If HIGH RISK or IMMEDIATE EMERGENCY ***                  │
│  6. Call dispatch_manager.find_nearest_ambulance()                  │
│     ├── Get patient latitude/longitude                              │
│     ├── Query available ambulances from database                    │
│     ├── Calculate distance using Haversine formula                  │
│     ├── Filter by ambulance type (ALS/BLS)                          │
│     └── Return nearest ambulance                                    │
│                                                                      │
│  7. Call dispatch_manager.assign_ambulance()                        │
│     ├── Create DispatchAssignment record                            │
│     ├── Update ambulance status → "Dispatched"                      │
│     ├── Calculate ETA                                               │
│     └── Save to database                                            │
│                                                                      │
│  8. Send response to frontend with:                                 │
│     ├── ambulance_assigned: true/false                              │
│     ├── ambulance_id: "Unit-X"                                      │
│     ├── estimated_arrival_time: "5 minutes"                         │
│     └── instructions for dispatcher/patient                         │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│            DATABASE UPDATES (triage_system.db)                       │
│                                                                      │
│  TriageCase Table:                                                  │
│  ├── case_id, patient_name, chief_complaint                         │
│  ├── ml_risk_score, risk_level                                      │
│  ├── ambulance_type                                                 │
│  ├── prerarrival_instructions                                       │
│  └── created_at                                                     │
│                                                                      │
│  Ambulance Table:                                                   │
│  ├── ambulance_id, unit_name, vehicle_type (ALS/BLS)               │
│  ├── current_latitude, current_longitude                            │
│  ├── status: "available" → "dispatched" → "en_route" → ...         │
│  └── in_service: true/false                                         │
│                                                                      │
│  DispatchAssignment NEW RECORD:                                     │
│  ├── assignment_id                                                  │
│  ├── case_id, ambulance_id                                          │
│  ├── pickup_latitude, pickup_longitude (patient location)           │
│  ├── estimated_distance_km                                          │
│  ├── estimated_time_minutes → ETA                                   │
│  ├── status: "pending" → "dispatched" → "en_route" → "on_scene"    │
│  └── priority: "CRITICAL" / "HIGH" / "MEDIUM" / "LOW"               │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│        DISPATCHER DASHBOARD (admin_dashboard.html)                   │
│                                                                      │
│  Updated to show:                                                   │
│  ├── ACTIVE CASES panel                                             │
│  │   ├── Patient Name, Age, Gender                                  │
│  │   ├── Chief Complaint, Address                                   │
│  │   ├── Ambulance Type badge (ALS/BLS)                             │
│  │   ├── Risk Level (HIGH/MODERATE/LOW)                             │
│  │   ├── Instructions for dispatcher                                │
│  │   ├── Assigned Ambulance: "Unit-12"                              │
│  │   └── ETA: "5 minutes"                                           │
│  │                                                                  │
│  ├── AMBULANCE STATUS panel                                         │
│  │   ├── Unit-1: Available, Downtown, Latitude: 47.60              │
│  │   ├── Unit-2: En Route, Capital Hill, Latitude: 47.61           │
│  │   ├── Unit-3: On Scene, Queen Anne, Latitude: 47.62             │
│  │   └── Unit-4: Unavailable, Hospital, Latitude: 47.58            │
│  │                                                                  │
│  ├── ROUTES & MAP                                                   │
│  │   ├── Show ambulance location (green)                            │
│  │   ├── Show patient location (red)                                │
│  │   ├── Draw line from ambulance to patient                        │
│  │   └── Show distance in km                                        │
│  │                                                                  │
│  └── LIVE UPDATES every 2-5 seconds                                 │
│      ├── Fetch /api/active_cases                                    │
│      ├── Fetch /api/ambulances                                      │
│      ├── Fetch /api/dispatch_assignments                            │
│      └── Update cards + map                                         │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│          AMBULANCE DRIVER NOTIFICATION (Optional App)                │
│                                                                      │
│  Ambulance receives alert:                                          │
│  ├── Beep/vibration notification                                    │
│  ├── Case details popup:                                            │
│  │   ├── Patient: John Smith                                        │
│  │   ├── Age: 45, Male                                              │
│  │   ├── Complaint: Chest pain                                      │
│  │   ├── Address: 123 Main St                                       │
│  │   ├── Phone: 555-1234                                            │
│  │   ├── Instructions: "Sit down, chew aspirin, loosen clothing"   │
│  │   └── "Accept" / "Decline" buttons                                │
│  │                                                                  │
│  When "Accept":                                                     │
│  ├── Status updates in system                                       │
│  ├── GPS nav to patient address                                     │
│  ├── Show ETA countdown                                             │
│  └── Pass through dispatch_manager functions                        │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│            REAL-TIME STATUS TRACKING                                 │
│                                                                      │
│  As ambulance responds:                                             │
│                                                                      │
│  Dispatcher sees progression:                                       │
│  ├── PENDING (just assigned)                                        │
│  ├── DISPATCHED (ambulance accepted)                                │
│  ├── EN_ROUTE (ambulance moving to patient)                         │
│  ├── ON_SCENE (ambulance at patient location)                       │
│  ├── TRANSPORTING (patient in ambulance)                            │
│  ├── HOSPITAL (arrived at hospital)                                 │
│  └── COMPLETED (case closed)                                        │
│                                                                      │
│  Each status update triggers:                                       │
│  ├── Update ambulance status in database                            │
│  ├── Update dispatch assignment status                              │
│  ├── Refresh dashboard display                                      │
│  └── Alert dispatcher if delays                                     │
└─────────────────────────────────────────────────────────────────────┘
"""

# ============================================================================
# KEY FUNCTIONS & WHERE THEY'RE CALLED
# ============================================================================

FUNCTION_FLOW = """
FUNCTION CHAIN:

1. submit_assessment() (app.py)
   └─→ get_ambulance_type(complaint) [complaint_mapping.py]
   └─→ get_instructions(complaint) [complaint_mapping.py]
   └─→ ml_classifier.predict() [ML model]
   └─→ db_session.add(triage_case)
   
   *** IF HIGH RISK OR IMMEDIATE EMERGENCY ***
   └─→ dispatch_manager.find_nearest_ambulance()
       └─→ haversine_distance() [eta_calculator.py]
       └─→ Filter by ambulance_type (ALS/BLS)
       └─→ Return (ambulance, distance, eta)
   └─→ dispatch_manager.assign_ambulance()
       └─→ Calculate distance & ETA
       └─→ Create DispatchAssignment record
       └─→ Update ambulance.status = 'dispatched'
       └─→ db_session.commit()
   └─→ Return response with ambulance_id + ETA


2. GET /api/active_cases (app.py)
   └─→ Query all TriageCase from database
   └─→ For each case, get_ambulance_type() + get_instructions()
   └─→ Return JSON with all case details
   
   
3. GET /api/ambulances (app.py)
   └─→ Query all Ambulance from database  
   └─→ Return JSON with ambulance status + location
   

4. GET /api/dispatch_assignments (NEW)
   └─→ Query all DispatchAssignment from database
   └─→ Link case_id with ambulance_id
   └─→ Show which ambulance assigned to which case
   

5. loadDashboard() (admin_dashboard.html - JavaScript)
   ├─→ Fetch /api/active_cases
   ├─→ Fetch /api/ambulances
   ├─→ Fetch /api/dispatch_assignments
   └─→ Merge data and render on page
        ├─→ Show case cards with ambulance assigned
        ├─→ Show ambulance markers on map
        ├─→ Show routes/distances
        └─→ Repeat every 5 seconds
"""

print(__doc__)
print(CURRENT_FLOW)
print("\n" + "="*70 + "\n")
print(MISSING_INTEGRATION)
print("\n" + "="*70 + "\n")
print(INTEGRATED_FLOW)
print("\n" + "="*70 + "\n")
print(FUNCTION_FLOW)
