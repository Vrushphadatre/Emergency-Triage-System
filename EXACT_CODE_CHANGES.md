"""
EXACT CODE CHANGES NEEDED FOR DISPATCH INTEGRATION
Three modifications to connect everything
"""

# ============================================================================
# CHANGE #1: Activate Dispatch in submit_assessment()
# ============================================================================

CHANGE_1 = """
FILE: app.py, function: submit_assessment()

CURRENT CODE (lines ~440-470):
───────────────────────────────────────────
        # Handle ambulance dispatch if high risk OR immediate emergency
        ambulance_assigned = False
        estimated_arrival_time = None
        ambulance_type = get_ambulance_type(chief_complaint)
        prerarrival_instructions = get_instructions(chief_complaint)
        
        if risk_level == 'high' or is_immediate_emergency:
            try:
                # Find nearest ambulance
                nearest_ambulance = dispatch_manager.find_nearest_ambulance(
                    patient_latitude=default_lat,
                    patient_longitude=default_lon,
                    required_equipment_level='advanced' if is_immediate_emergency else 'basic',
                    db_session=db_session
                )
                
                if nearest_ambulance:
                    # Assign ambulance - BUT THIS CODE MIGHT BE BROKEN
                    assignment = dispatch_manager.assign_ambulance(  ← POTENTIAL ISSUE
                        case_id=case_id,
                        ambulance_id=nearest_ambulance['ambulance_id'],
                        ...
                    )

WHAT TO DO:
───────────────────────────────────────────
1. Check if dispatch_manager has the CORRECT function signature
2. Make sure find_nearest_ambulance() returns proper data structure
3. Make sure assign_ambulance() accepts correct parameters
4. Add error handling for cases with no available ambulances
5. Log dispatch events to database audit log

EXPECTED RESULT:
───────────────────────────────────────────
When form submitted with HIGH RISK complaint:
  ✓ Nearest ALS/BLS ambulance found
  ✓ Ambulance status changed to "Dispatched"
  ✓ DispatchAssignment record created
  ✓ ETA calculated and returned to frontend
"""

# ============================================================================
# CHANGE #2: Add Ambulance Endpoints
# ============================================================================

CHANGE_2 = """
FILE: app.py, add new routes

CODE TO ADD:
───────────────────────────────────────────

@app.route('/api/ambulances')
def api_ambulances():
    \"\"\"Get all ambulances with real-time status\"\"\"
    db_session = db_manager.get_session()
    try:
        ambulances = db_session.query(Ambulance).filter(
            Ambulance.in_service == True
        ).all()
        
        ambulances_data = [{
            'ambulance_id': a.ambulance_id,
            'unit_name': a.unit_name,
            'vehicle_type': a.vehicle_type,  # ALS or BLS
            'status': a.status,  # available/dispatched/en_route/on_scene
            'latitude': a.current_latitude or a.station_latitude,
            'longitude': a.current_longitude or a.station_longitude,
            'address': a.current_address or a.station_address,
            'crew_size': a.crew_size,
            'fuel_level': a.fuel_level
        } for a in ambulances]
        
        return jsonify({'ambulances': ambulances_data})
    finally:
        db_session.close()


@app.route('/api/dispatch_assignments')
def api_dispatch_assignments():
    \"\"\"Get current dispatch assignments linking cases to ambulances\"\"\"
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
            'priority': a.priority
        } for a in assignments]
        
        return jsonify({'assignments': assignments_data})
    finally:
        db_session.close()


@app.route('/api/update_dispatch_status', methods=['POST'])
def update_dispatch_status():
    \"\"\"Update dispatch status (dispatcher clicks: En Route, On Scene, etc)\"\"\"
    data = request.json
    assignment_id = data.get('assignment_id')
    new_status = data.get('status')  # en_route, on_scene, transporting, completed
    
    db_session = db_manager.get_session()
    try:
        dispatch_manager.update_dispatch_status(
            assignment_id=assignment_id,
            new_status=new_status,
            db_session=db_session
        )
        
        return jsonify({'success': True, 'message': f'Status updated to {new_status}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db_session.close()

RESULT:
───────────────────────────────────────────
✓ /api/ambulances returns all ambulance locations + status
✓ /api/dispatch_assignments returns which ambulance → which case
✓ /api/update_dispatch_status allows manual status changes
"""

# ============================================================================
# CHANGE #3: Update Dashboard JavaScript
# ============================================================================

CHANGE_3 = """
FILE: templates/admin_dashboard.html, JavaScript section

CODE TO ADD:
───────────────────────────────────────────

let casesList = [];
let ambulancesList = [];
let assignmentsList = [];

async function loadDashboard() {
    try {
        // Fetch all three data sources
        const casesResponse = await fetch('/api/active_cases');
        const ambulancesResponse = await fetch('/api/ambulances');
        const assignmentsResponse = await fetch('/api/dispatch_assignments');
        
        const casesData = await casesResponse.json();
        const ambulancesData = await ambulancesResponse.json();
        const assignmentsData = await assignmentsResponse.json();
        
        casesList = casesData.cases || [];
        ambulancesList = ambulancesData.ambulances || [];
        assignmentsList = assignmentsData.assignments || [];
        
        // Link assignments to cases
        linkAssignmentsToCases();
        
        // Update display
        updateCasesDisplay();
        updateAmbulancesDisplay();
        updateMetrics();
        
        console.log('Dashboard loaded:', casesList.length, 'cases,', 
                    ambulancesList.length, 'ambulances');
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function linkAssignmentsToCases() {
    // Add ambulance info to each case
    casesList.forEach(caseItem => {
        const assignment = assignmentsList.find(a => a.case_id === caseItem.case_id);
        if (assignment) {
            caseItem.assigned_ambulance = assignment.ambulance_id;
            caseItem.assignment_status = assignment.status;
            caseItem.eta = assignment.estimated_time_minutes;
            caseItem.distance = assignment.estimated_distance_km;
        }
    });
}

function updateCasesDisplay() {
    const container = document.getElementById('casesList');
    
    let html = '<div style="display: grid; gap: 15px;">';
    
    casesList.forEach(c => {
        const riskColor = c.risk_level === 'high' ? '#ff6b6b' : 
                         c.risk_level === 'moderate' ? '#ffa500' : '#51cf66';
        
        // Show ambulance if assigned
        const ambulanceInfo = c.assigned_ambulance ? 
            `<div style="margin-top: 10px; padding: 10px; background: #e3f2fd; border-radius: 4px;">
                <strong>Assigned: ${c.assigned_ambulance}</strong><br>
                Status: ${c.assignment_status}<br>
                ETA: ${c.eta} mins | Distance: ${c.distance} km
            </div>` : '';
        
        html += `
            <div style="border: 2px solid ${riskColor}; padding: 15px; border-radius: 8px;">
                <div style="font-weight: bold;">
                    ${c.patient_name} | ${c.ambulance_type}
                </div>
                <div style="font-size: 12px; margin: 10px 0;">
                    Complaint: ${c.chief_complaint}<br>
                    Address: ${c.patient_address}
                </div>
                ${ambulanceInfo}
                <div style="padding: 8px; background: ${riskColor}; color: white; border-radius: 4px; margin-top: 10px;">
                    RISK: ${c.risk_level.toUpperCase()} (${(c.risk_score * 100).toFixed(1)}%)
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function updateAmbulancesDisplay() {
    const container = document.getElementById('ambulancesList');
    
    const statusColors = {
        'available': '#51cf66',
        'dispatched': '#fff500',
        'en_route': '#ff9800',
        'on_scene': '#ff6b6b',
        'unavailable': '#ccc'
    };
    
    let html = '<div style="display: grid; gap: 10px;">';
    
    ambulancesList.forEach(a => {
        const statusColor = statusColors[a.status] || '#ccc';
        
        html += `
            <div style="border-left: 4px solid ${statusColor}; padding: 10px; background: white;">
                <strong>${a.unit_name}</strong> (${a.vehicle_type})<br>
                Status: <span style="background: ${statusColor}; padding: 2px 6px; color: white; border-radius: 3px;">
                    ${a.status}
                </span><br>
                Location: ${a.address}
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Auto-refresh every 5 seconds
setInterval(() => {
    loadDashboard();
}, 5000);

// Initial load
loadDashboard();

RESULT:
───────────────────────────────────────────
✓ Dashboard shows cases with assigned ambulance
✓ Dashboard shows ambulance locations + status
✓ Dashboard shows ETA and distance for each case
✓ Auto-refreshes every 5 seconds with live data
✓ Dispatcher sees complete picture at a glance
"""

print(__doc__)
print("\n" + "="*70)
print(CHANGE_1)
print("\n" + "="*70)
print(CHANGE_2)
print("\n" + "="*70)
print(CHANGE_3)
