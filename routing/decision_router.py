"""
Case Routing Logic
Routes cases to appropriate queues based on risk assessment
"""

from typing import Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config


class DecisionRouter:
    """
    Routes triage cases to appropriate human decision-makers
    """
    
    def __init__(self):
        self.routing_rules = config.ROUTING_RULES
    
    def route_case(self, ml_prediction: Dict, case_data: Dict) -> Dict:
        """
        Determine routing for a case based on ML prediction
        
        Args:
            ml_prediction: ML model output with risk_score, is_emergency, etc.
            case_data: Patient case information
            
        Returns:
            Routing decision with queue assignment and priority
        """
        risk_score = ml_prediction['risk_score']
        is_emergency = ml_prediction['is_emergency']
        
        # Emergency routing
        if is_emergency or risk_score >= config.EMERGENCY_THRESHOLD:
            queue = 'dispatcher'
            priority = 'HIGH'
            
            # Ultra-critical gets CRITICAL priority
            if risk_score >= 0.90 or ml_prediction.get('safety_override'):
                priority = 'CRITICAL'
            
            sla_minutes = self.routing_rules['emergency']['sla_minutes']
            
            routing_decision = {
                'queue': queue,
                'priority': priority,
                'sla_minutes': sla_minutes,
                'reason': 'Emergency risk detected - immediate dispatcher review required',
                'recommended_action': 'Dispatch ambulance after review',
            }
        
        # Non-emergency routing
        else:
            queue = 'nurse'
            
            # Risk-based priority within nurse queue
            if risk_score >= 0.50:
                priority = 'MEDIUM'
            elif risk_score >= 0.30:
                priority = 'LOW'
            else:
                priority = 'ROUTINE'
            
            sla_minutes = self.routing_rules['non_emergency']['sla_minutes']
            
            routing_decision = {
                'queue': queue,
                'priority': priority,
                'sla_minutes': sla_minutes,
                'reason': 'Non-emergency assessment - nurse callback recommended',
                'recommended_action': 'Nurse to contact patient and provide guidance',
            }
        
        # Add queue position estimate
        routing_decision['estimated_wait_minutes'] = self._estimate_wait_time(
            queue, priority
        )
        
        return routing_decision
    
    def _estimate_wait_time(self, queue: str, priority: str) -> int:
        """
        Estimate wait time based on queue and priority
        (In production, this would query actual queue lengths)
        
        Args:
            queue: 'dispatcher' or 'nurse'
            priority: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'ROUTINE'
            
        Returns:
            Estimated wait time in minutes
        """
        # Simplified estimation for MVP
        wait_times = {
            'dispatcher': {
                'CRITICAL': 1,
                'HIGH': 2,
                'MEDIUM': 5,
                'LOW': 10,
                'ROUTINE': 15,
            },
            'nurse': {
                'CRITICAL': 5,
                'HIGH': 10,
                'MEDIUM': 15,
                'LOW': 30,
                'ROUTINE': 60,
            }
        }
        
        return wait_times.get(queue, {}).get(priority, 15)
    
    def get_queue_assignment(self, case_id: str, routing_decision: Dict) -> Dict:
        """
        Create queue assignment record
        
        Args:
            case_id: Unique case identifier
            routing_decision: Output from route_case()
            
        Returns:
            Queue assignment details
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        sla_deadline = now + timedelta(minutes=routing_decision['sla_minutes'])
        
        assignment = {
            'case_id': case_id,
            'queue': routing_decision['queue'],
            'priority': routing_decision['priority'],
            'assigned_at': now.isoformat(),
            'sla_deadline': sla_deadline.isoformat(),
            'estimated_wait_minutes': routing_decision['estimated_wait_minutes'],
            'status': 'pending',  # 'pending', 'in_progress', 'completed'
        }
        
        return assignment


class WorkloadBalancer:
    """
    Balances workload across available operators
    (Simplified for MVP - can be extended for production)
    """
    
    def __init__(self):
        self.active_dispatchers = []
        self.active_nurses = []
    
    def assign_to_operator(self, queue: str, case_id: str) -> str:
        """
        Assign case to specific operator
        
        Args:
            queue: 'dispatcher' or 'nurse'
            case_id: Case to assign
            
        Returns:
            Operator ID
        """
        # For MVP, use round-robin or return 'available'
        # In production, this would integrate with staffing system
        
        if queue == 'dispatcher':
            if self.active_dispatchers:
                # Round-robin assignment
                operator = self.active_dispatchers[0]
                self.active_dispatchers.append(self.active_dispatchers.pop(0))
                return operator
            return 'dispatcher_pool'
        
        elif queue == 'nurse':
            if self.active_nurses:
                operator = self.active_nurses[0]
                self.active_nurses.append(self.active_nurses.pop(0))
                return operator
            return 'nurse_pool'
        
        return 'unassigned'
    
    def register_operator(self, queue: str, operator_id: str):
        """Register an available operator"""
        if queue == 'dispatcher' and operator_id not in self.active_dispatchers:
            self.active_dispatchers.append(operator_id)
        elif queue == 'nurse' and operator_id not in self.active_nurses:
            self.active_nurses.append(operator_id)
    
    def get_queue_status(self) -> Dict:
        """Get current queue status"""
        return {
            'dispatchers': {
                'active': len(self.active_dispatchers),
                'available_operators': self.active_dispatchers
            },
            'nurses': {
                'active': len(self.active_nurses),
                'available_operators': self.active_nurses
            }
        }


if __name__ == "__main__":
    # Test routing logic
    print("=== Testing Case Routing ===\n")
    
    router = DecisionRouter()
    
    # Test emergency case
    emergency_prediction = {
        'risk_score': 0.92,
        'confidence': 0.85,
        'is_emergency': True,
        'safety_override': True,
    }
    
    emergency_case = {
        'case_id': 'TEST_EMERGENCY_001',
        'chief_complaint': 'chest pain',
    }
    
    print("Test 1: Emergency Case Routing")
    print("-" * 50)
    routing = router.route_case(emergency_prediction, emergency_case)
    print(f"Queue: {routing['queue']}")
    print(f"Priority: {routing['priority']}")
    print(f"SLA: {routing['sla_minutes']} minutes")
    print(f"Reason: {routing['reason']}")
    print(f"Estimated Wait: {routing['estimated_wait_minutes']} minutes")
    
    # Test non-emergency case
    non_emergency_prediction = {
        'risk_score': 0.28,
        'confidence': 0.78,
        'is_emergency': False,
    }
    
    non_emergency_case = {
        'case_id': 'TEST_NON_EMERGENCY_001',
        'chief_complaint': 'mild headache',
    }
    
    print("\n\nTest 2: Non-Emergency Case Routing")
    print("-" * 50)
    routing = router.route_case(non_emergency_prediction, non_emergency_case)
    print(f"Queue: {routing['queue']}")
    print(f"Priority: {routing['priority']}")
    print(f"SLA: {routing['sla_minutes']} minutes")
    print(f"Reason: {routing['reason']}")
    print(f"Estimated Wait: {routing['estimated_wait_minutes']} minutes")
    
    print("\n\n✓ Routing logic tests complete")
