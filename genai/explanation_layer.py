"""
GenAI Explanation Layer
Converts ML risk scores into plain-language explanations
"""

from typing import Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config


class ExplanationLayer:
    """
    Translates ML predictions into human-readable explanations
    No medical diagnosis - only describes risk factors in simple terms
    """
    
    def explain_risk_score(self, case_data: Dict, ml_prediction: Dict) -> str:
        """
        Generate plain-language explanation of risk score
        
        Args:
            case_data: Patient case information
            ml_prediction: ML model output with risk_score, confidence, etc.
            
        Returns:
            Human-readable explanation string
        """
        risk_score = ml_prediction['risk_score']
        confidence = ml_prediction['confidence']
        is_emergency = ml_prediction['is_emergency']
        
        # Start with risk level
        if risk_score >= 0.85:
            risk_level = "very high risk"
            urgency = "requires immediate emergency response"
        elif risk_score >= 0.65:
            risk_level = "high risk"
            urgency = "requires emergency dispatch"
        elif risk_score >= 0.40:
            risk_level = "moderate risk"
            urgency = "should be reviewed by a nurse promptly"
        else:
            risk_level = "low risk"
            urgency = "can be handled through nurse callback or self-care guidance"
        
        # Build explanation
        explanation_parts = []
        
        # Opening statement
        explanation_parts.append(
            f"This case has been assessed as **{risk_level}** (score: {risk_score:.2f} out of 1.00) "
            f"and {urgency}."
        )
        
        # Explain key factors
        key_factors = self._identify_key_factors(case_data)
        if key_factors:
            explanation_parts.append(
                f"\n\n**Key Factors:**\n" + "\n".join(f"• {factor}" for factor in key_factors)
            )
        
        # Confidence note
        if confidence >= 0.80:
            confidence_text = "The system is highly confident in this assessment"
        elif confidence >= 0.60:
            confidence_text = "The system has moderate confidence in this assessment"
        else:
            confidence_text = "The system has low confidence, so a safety-first approach is applied"
        
        explanation_parts.append(f"\n\n**Confidence:** {confidence_text} ({confidence:.0%}).")
        
        # Safety overrides
        if ml_prediction.get('safety_override'):
            overrides = ml_prediction.get('safety_overrides', [])
            explanation_parts.append(
                f"\n\n**⚠️ Safety Override Applied:**\n" + 
                "\n".join(f"• {override}" for override in overrides)
            )
        
        # Recommendation
        recommendation = (
            "\n\n**Recommended Action:** " + ml_prediction.get('recommendation', 'Review required')
        )
        explanation_parts.append(recommendation)
        
        # Disclaimer
        disclaimer = (
            "\n\n*This is decision support only. Final dispatch decision must be made by dispatcher "
            "after reviewing all information.*"
        )
        explanation_parts.append(disclaimer)
        
        return "".join(explanation_parts)
    
    def _identify_key_factors(self, case_data: Dict) -> list:
        """
        Identify and describe key risk factors in plain language
        
        Args:
            case_data: Patient case information
            
        Returns:
            List of plain-language factor descriptions
        """
        factors = []
        
        # Check for critical symptoms
        transcript = case_data.get('transcript', '').lower()
        
        # Critical symptom categories
        critical_mappings = {
            'chest_cardiac': ['chest pain', 'chest pressure', 'heart attack'],
            'breathing': ['difficulty breathing', 'shortness of breath', "can't breathe"],
            'consciousness': ['unconscious', 'unresponsive', 'not responding'],
            'bleeding': ['severe bleeding', 'heavy bleeding', 'blood'],
            'neurological': ['stroke', 'seizure', 'slurred speech', 'face drooping'],
        }
        
        for category, keywords in critical_mappings.items():
            for keyword in keywords:
                if keyword in transcript:
                    if category == 'chest_cardiac':
                        factors.append("Reported chest pain or cardiac symptoms (highest priority)")
                    elif category == 'breathing':
                        factors.append("Breathing difficulties reported (critical concern)")
                    elif category == 'consciousness':
                        factors.append("Altered consciousness or unresponsive (immediate attention needed)")
                    elif category == 'bleeding':
                        factors.append("Significant bleeding reported (urgent)")
                    elif category == 'neurological':
                        factors.append("Possible stroke or neurological symptoms (time-critical)")
                    break
        
        # Pain level
        pain_level = case_data.get('pain_level', 0)
        if pain_level >= 8:
            factors.append(f"Severe pain reported ({pain_level}/10)")
        elif pain_level >= 6:
            factors.append(f"Significant pain level ({pain_level}/10)")
        
        # Duration (acute is more concerning)
        duration = case_data.get('duration_hours', 0)
        if duration < 1:
            factors.append("Symptoms started very recently (acute onset)")
        elif duration < 6:
            factors.append(f"Symptoms developed within the last {int(duration)} hours")
        
        # Age vulnerability
        age = case_data.get('age', 0)
        if age < 2:
            factors.append("Infant patient (heightened vulnerability)")
        elif age < 12:
            factors.append("Pediatric patient (requires careful assessment)")
        elif age > 65:
            factors.append(f"Elderly patient (age {age} - elevated risk factors)")
        
        # Medical history
        history = case_data.get('history', '').lower()
        high_risk_conditions = ['heart disease', 'diabetes', 'copd', 'asthma', 'stroke history']
        for condition in high_risk_conditions:
            if condition in history:
                factors.append(f"Pre-existing condition: {condition}")
        
        # If no specific factors, provide general note
        if not factors:
            factors.append("Based on overall symptom pattern and clinical presentation")
        
        return factors[:5]  # Limit to top 5 factors
    
    def generate_dispatcher_summary(self, case_data: Dict, ml_prediction: Dict) -> str:
        """
        Generate concise summary for dispatcher console
        
        Args:
            case_data: Patient case information
            ml_prediction: ML model output
            
        Returns:
            Brief summary for quick decision-making
        """
        risk_score = ml_prediction['risk_score']
        chief_complaint = case_data.get('chief_complaint', 'Not specified')
        age = case_data.get('age', 'Unknown')
        conscious = case_data.get('conscious', True)
        pain_level = case_data.get('pain_level', '?')
        
        # Header with risk
        if risk_score >= 0.85:
            header = "🚨 CRITICAL - IMMEDIATE DISPATCH"
        elif risk_score >= 0.65:
            header = "⚠️  HIGH PRIORITY - EMERGENCY"
        else:
            header = "ℹ️  REVIEW REQUIRED"
        
        summary = f"""
{header}

**Chief Complaint:** {chief_complaint}
**Patient Age:** {age}
**Pain Level:** {pain_level}/10
**Conscious:** {'Yes' if conscious else 'NO - UNCONSCIOUS'}
**Risk Score:** {risk_score:.2f} ({ml_prediction.get('recommendation', '')})

**Quick Assessment:**
{ml_prediction.get('reasoning', 'See full details below')}
"""
        
        return summary.strip()
    
    def generate_nurse_summary(self, case_data: Dict, ml_prediction: Dict) -> str:
        """
        Generate summary for nurse review queue
        
        Args:
            case_data: Patient case information
            ml_prediction: ML model output
            
        Returns:
            Summary for nurse callback
        """
        chief_complaint = case_data.get('chief_complaint', 'Not specified')
        duration = case_data.get('duration_hours', 0)
        history = case_data.get('history', 'None reported')
        
        summary = f"""
**Non-Emergency Case for Review**

**Chief Complaint:** {chief_complaint}
**Duration:** {duration:.1f} hours
**Medical History:** {history}
**Risk Assessment:** {ml_prediction.get('reasoning', '')}

**Recommended Action:** Nurse callback to assess and provide guidance or referral to appropriate care level.

**Notes:** This case was triaged as non-emergency but requires clinical judgment for appropriate follow-up.
"""
        
        return summary.strip()


if __name__ == "__main__":
    # Test explanation layer
    print("=== Testing Explanation Layer ===\n")
    
    explainer = ExplanationLayer()
    
    # Test case 1: Emergency
    case_emergency = {
        'transcript': 'severe chest pain and shortness of breath',
        'chief_complaint': 'chest pain',
        'pain_level': 9,
        'age': 58,
        'duration_hours': 0.5,
        'conscious': True,
        'history': 'high blood pressure, diabetes',
    }
    
    ml_emergency = {
        'risk_score': 0.95,
        'confidence': 0.88,
        'is_emergency': True,
        'recommendation': 'EMERGENCY - Dispatch ambulance',
        'reasoning': 'Critical symptoms detected: chest pain, shortness of breath',
        'safety_override': True,
        'safety_overrides': ['Critical symptoms detected: chest pain, shortness of breath']
    }
    
    print("Test 1: Emergency Case")
    print("=" * 50)
    explanation = explainer.explain_risk_score(case_emergency, ml_emergency)
    print(explanation)
    
    print("\n\nDispatcher Summary:")
    print("=" * 50)
    dispatcher_summary = explainer.generate_dispatcher_summary(case_emergency, ml_emergency)
    print(dispatcher_summary)
    
    # Test case 2: Non-emergency
    print("\n\n" + "=" * 70 + "\n")
    
    case_non_emergency = {
        'transcript': 'mild headache for two days',
        'chief_complaint': 'headache',
        'pain_level': 4,
        'age': 34,
        'duration_hours': 48,
        'conscious': True,
        'history': 'none',
    }
    
    ml_non_emergency = {
        'risk_score': 0.25,
        'confidence': 0.75,
        'is_emergency': False,
        'recommendation': 'NON-EMERGENCY - Nurse review',
        'reasoning': 'Based on overall symptom patterns and clinical indicators',
    }
    
    print("Test 2: Non-Emergency Case")
    print("=" * 50)
    explanation = explainer.explain_risk_score(case_non_emergency, ml_non_emergency)
    print(explanation)
    
    print("\n\nNurse Summary:")
    print("=" * 50)
    nurse_summary = explainer.generate_nurse_summary(case_non_emergency, ml_non_emergency)
    print(nurse_summary)
    
    print("\n\n✓ Explanation layer tests complete")
