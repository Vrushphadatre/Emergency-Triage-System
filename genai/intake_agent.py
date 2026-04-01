"""
GenAI Intake Agent using LangChain
Conducts structured patient intake following predefined script
"""

from typing import Dict, List, Optional
import json
import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
import config
from safety.guardrails import SafetyGuardrails


class IntakeAgent:
    """
    Conversational agent for structured patient intake
    Uses predefined questions - does NOT deviate or provide medical advice
    """
    
    def __init__(self):
        self.questions = config.INTAKE_QUESTIONS
        self.current_question_idx = 0
        self.conversation_history = []
        self.extracted_data = {}
        self.max_turns = config.MAX_INTAKE_TURNS
        self.safety = SafetyGuardrails()
        
    def start_intake(self) -> str:
        """
        Begin intake conversation
        
        Returns:
            First question
        """
        self.current_question_idx = 0
        self.conversation_history = []
        self.extracted_data = {}
        
        greeting = (
            "Hello, I'm here to help gather information about your situation. "
            "I'll ask you a few questions. Please answer as clearly as possible. "
            "This information will be reviewed by our dispatch team.\n\n"
        )
        
        first_question = self.questions[0]
        self.conversation_history.append({
            'speaker': 'agent',
            'message': greeting + first_question
        })
        
        return greeting + first_question
    
    def process_response(self, user_response: str) -> Dict:
        """
        Process user response and determine next question
        
        Args:
            user_response: User's answer to current question
            
        Returns:
            dict with:
                - next_question: Next question to ask (or None if complete)
                - extracted_data: Data extracted so far
                - is_complete: Whether intake is finished
                - safety_alert: Any critical symptoms detected
        """
        # Sanitize input
        user_response = self.safety.sanitize_input(user_response)
        
        # Record response
        self.conversation_history.append({
            'speaker': 'user',
            'message': user_response
        })
        
        # Check for critical symptoms
        has_critical, critical_symptoms = self.safety.check_critical_symptoms(user_response)
        
        # Extract information based on current question
        self._extract_information(user_response, self.current_question_idx)
        
        # Determine if we should continue or escalate immediately
        if has_critical:
            return {
                'next_question': None,
                'extracted_data': self._compile_extracted_data(),
                'is_complete': True,
                'safety_alert': f"CRITICAL SYMPTOMS DETECTED: {', '.join(critical_symptoms)}. Immediate escalation required.",
                'immediate_emergency': True
            }
        
        # Move to next question
        self.current_question_idx += 1
        
        # Check if intake is complete
        if self.current_question_idx >= len(self.questions) or len(self.conversation_history) >= self.max_turns:
            return {
                'next_question': None,
                'extracted_data': self._compile_extracted_data(),
                'is_complete': True,
                'safety_alert': None,
                'immediate_emergency': False
            }
        
        # Ask next question
        next_question = self.questions[self.current_question_idx]
        self.conversation_history.append({
            'speaker': 'agent',
            'message': next_question
        })
        
        return {
            'next_question': next_question,
            'extracted_data': self._compile_extracted_data(),
            'is_complete': False,
            'safety_alert': None,
            'immediate_emergency': False
        }
    
    def _extract_information(self, response: str, question_idx: int):
        """
        Extract structured information from response based on question type
        Uses simple pattern matching (no LLM needed for MVP)
        """
        response_lower = response.lower()
        
        # Question 0: Chief complaint
        if question_idx == 0:
            self.extracted_data['chief_complaint'] = response[:200]
        
        # Question 1: Duration
        elif question_idx == 1:
            duration = self._extract_duration(response)
            self.extracted_data['symptom_duration'] = duration
            self.extracted_data['duration_hours'] = duration
        
        # Question 2: Pain level
        elif question_idx == 2:
            pain = self._extract_pain_level(response)
            self.extracted_data['pain_level'] = pain
        
        # Question 3: Consciousness
        elif question_idx == 3:
            conscious = self._extract_consciousness(response)
            self.extracted_data['conscious_status'] = conscious
            self.extracted_data['conscious'] = conscious
        
        # Question 4: Age
        elif question_idx == 4:
            age = self._extract_age(response)
            self.extracted_data['patient_age'] = age
            self.extracted_data['age'] = age
        
        # Question 5: Medical history
        elif question_idx == 5:
            self.extracted_data['medical_history'] = response[:300]
            self.extracted_data['history'] = response[:300]
        
        # Question 6: Medications
        elif question_idx == 6:
            self.extracted_data['medications'] = response[:300]
        
        # Question 7: Previous episodes
        elif question_idx == 7:
            self.extracted_data['previous_episodes'] = response[:200]
    
    def _extract_duration(self, text: str) -> float:
        """Extract duration in hours from text"""
        text_lower = text.lower()
        
        # Look for time patterns
        minutes_match = re.search(r'(\d+)\s*(minute|min)', text_lower)
        if minutes_match:
            return float(minutes_match.group(1)) / 60
        
        hours_match = re.search(r'(\d+)\s*(hour|hr)', text_lower)
        if hours_match:
            return float(hours_match.group(1))
        
        days_match = re.search(r'(\d+)\s*(day)', text_lower)
        if days_match:
            return float(days_match.group(1)) * 24
        
        weeks_match = re.search(r'(\d+)\s*(week)', text_lower)
        if weeks_match:
            return float(weeks_match.group(1)) * 24 * 7
        
        # Keywords for relative time
        if any(word in text_lower for word in ['just now', 'right now', 'just started']):
            return 0.1
        if any(word in text_lower for word in ['today', 'this morning', 'this afternoon']):
            return 6.0
        if 'yesterday' in text_lower:
            return 24.0
        
        # Default
        return 12.0  # Conservative estimate
    
    def _extract_pain_level(self, text: str) -> int:
        """Extract pain level (1-10) from text"""
        # Look for numbers
        numbers = re.findall(r'\b(\d+)\b', text)
        if numbers:
            pain = int(numbers[0])
            return min(10, max(1, pain))
        
        # Keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['severe', 'excruciating', 'worst', 'unbearable']):
            return 9
        if any(word in text_lower for word in ['bad', 'terrible', 'intense']):
            return 7
        if any(word in text_lower for word in ['moderate', 'medium', 'noticeable']):
            return 5
        if any(word in text_lower for word in ['mild', 'slight', 'minor', 'little']):
            return 3
        
        return 5  # Default moderate
    
    def _extract_consciousness(self, text: str) -> bool:
        """Extract consciousness status"""
        text_lower = text.lower()
        
        unconscious_keywords = ['unconscious', 'unresponsive', 'not responding', 'passed out', 'fainted']
        if any(keyword in text_lower for keyword in unconscious_keywords):
            return False
        
        return True  # Default to conscious
    
    def _extract_age(self, text: str) -> int:
        """Extract age from text"""
        # Look for numbers
        numbers = re.findall(r'\b(\d+)\b', text)
        if numbers:
            age = int(numbers[0])
            return min(120, max(0, age))
        
        # Age group keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['infant', 'baby', 'newborn']):
            return 1
        if any(word in text_lower for word in ['child', 'kid', 'toddler']):
            return 8
        if any(word in text_lower for word in ['teen', 'teenager', 'adolescent']):
            return 15
        if any(word in text_lower for word in ['elderly', 'senior', 'old']):
            return 75
        
        return 40  # Default adult
    
    def _compile_extracted_data(self) -> Dict:
        """
        Compile all extracted data into structured format
        
        Returns:
            Complete case data dictionary
        """
        # Create transcript from conversation
        transcript_parts = []
        for turn in self.conversation_history:
            if turn['speaker'] == 'user':
                transcript_parts.append(turn['message'])
        
        transcript = " ".join(transcript_parts)
        
        # Combine into complete case data
        case_data = {
            'transcript': transcript,
            'conversation_history': self.conversation_history,
            **self.extracted_data
        }
        
        # Ensure all required fields have defaults
        defaults = {
            'chief_complaint': 'Not specified',
            'symptom_duration': 0,
            'duration_hours': 0,
            'pain_level': 5,
            'conscious_status': True,
            'conscious': True,
            'patient_age': 40,
            'age': 40,
            'medical_history': 'None reported',
            'history': 'None reported',
        }
        
        for key, default_value in defaults.items():
            if key not in case_data:
                case_data[key] = default_value
        
        return case_data
    
    def get_conversation_summary(self) -> str:
        """Get formatted summary of conversation"""
        summary_parts = []
        
        for turn in self.conversation_history:
            speaker = "Agent" if turn['speaker'] == 'agent' else "Patient"
            summary_parts.append(f"{speaker}: {turn['message']}")
        
        return "\n\n".join(summary_parts)


if __name__ == "__main__":
    # Test intake agent
    print("=== Testing Intake Agent ===\n")
    
    agent = IntakeAgent()
    
    # Start intake
    first_question = agent.start_intake()
    print(f"Agent: {first_question}\n")
    
    # Simulate responses
    test_responses = [
        "I have severe chest pain",
        "It started about 30 minutes ago",
        "The pain is 9 out of 10",
        "Yes, I'm conscious and talking to you",
        "I'm 58 years old",
        "I have high blood pressure and diabetes",
        "I take metformin and lisinopril",
        "No, this has never happened before"
    ]
    
    for response in test_responses:
        print(f"User: {response}\n")
        
        result = agent.process_response(response)
        
        if result['safety_alert']:
            print(f"⚠️  SAFETY ALERT: {result['safety_alert']}\n")
            print("=== Intake Terminated - Emergency Escalation ===")
            break
        
        if result['is_complete']:
            print("=== Intake Complete ===\n")
            print("Extracted Data:")
            print(json.dumps(result['extracted_data'], indent=2))
            break
        
        if result['next_question']:
            print(f"Agent: {result['next_question']}\n")
    
    print("\n✓ Intake agent test complete")
