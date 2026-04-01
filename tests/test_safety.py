"""
Safety Guardrails Test Suite
Validates critical safety rules and emergency detection
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from safety.guardrails import SafetyGuardrails
from models.ml_model import TriageClassifier
import config

def test_critical_symptom_detection():
    """Test that critical symptoms are properly detected"""
    print("Testing Critical Symptom Detection...")
    
    safety = SafetyGuardrails()
    
    test_cases = [
        ("I have severe chest pain", True, "chest pain"),
        ("I can't breathe properly", True, "difficulty breathing"),
        ("Patient is unconscious", True, "unconscious"),
        ("My ankle hurts", False, None),
        ("I have a mild headache", False, None),
    ]
    
    all_passed = True
    for text, should_detect, expected_symptom in test_cases:
        has_critical, symptoms = safety.check_critical_symptoms(text)
        
        if has_critical == should_detect:
            print(f"  ✅ PASS: '{text}' → {'Detected' if has_critical else 'Not detected'}")
        else:
            print(f"  ❌ FAIL: '{text}' → Expected: {should_detect}, Got: {has_critical}")
            all_passed = False
    
    return all_passed


def test_emergency_bias():
    """Test that emergency bias is applied for low confidence"""
    print("\nTesting Emergency Bias for Low Confidence...")
    
    safety = SafetyGuardrails()
    
    # Simulate low confidence, moderate risk scenario
    ml_prediction = {
        'risk_score': 0.55,
        'confidence': 0.60,  # Below threshold
        'is_emergency': False,
        'reasoning': 'Test case'
    }
    
    case_data = {
        'transcript': 'moderate pain in stomach',
        'chief_complaint': 'stomach pain',
        'pain_level': 6,
        'conscious': True,
        'age': 40,
    }
    
    result = safety.enforce_emergency_override(case_data, ml_prediction)
    
    # Should be escalated to emergency due to low confidence
    if result['is_emergency'] and result['risk_score'] >= config.EMERGENCY_THRESHOLD:
        print("  ✅ PASS: Low confidence correctly escalated to emergency")
        return True
    else:
        print("  ❌ FAIL: Low confidence not escalated")
        return False


def test_unconscious_override():
    """Test that unconscious patients are always marked as emergency"""
    print("\nTesting Unconscious Patient Override...")
    
    safety = SafetyGuardrails()
    
    ml_prediction = {
        'risk_score': 0.30,  # Low risk initially
        'confidence': 0.90,
        'is_emergency': False,
        'reasoning': 'Test case'
    }
    
    case_data = {
        'transcript': 'fell and hit head',
        'chief_complaint': 'head injury',
        'pain_level': 5,
        'conscious': False,  # UNCONSCIOUS
        'age': 45,
    }
    
    result = safety.enforce_emergency_override(case_data, ml_prediction)
    
    if result['is_emergency'] and result['risk_score'] == 1.0:
        print("  ✅ PASS: Unconscious patient escalated to emergency")
        return True
    else:
        print("  ❌ FAIL: Unconscious patient not escalated")
        return False


def test_genai_output_validation():
    """Test that GenAI output validation rejects prohibited content"""
    print("\nTesting GenAI Output Validation...")
    
    safety = SafetyGuardrails()
    
    test_cases = [
        ("You have pneumonia", False),  # Diagnosis prohibited
        ("I think you have the flu", False),  # Diagnosis prohibited
        ("Based on your symptoms, this appears to be non-emergency", True),  # OK
        ("Take this medication", False),  # Medical advice prohibited
        ("Your symptoms suggest you should see a nurse", True),  # OK
    ]
    
    all_passed = True
    for output, should_pass in test_cases:
        is_valid, error = safety.validate_genai_output(output)
        
        if is_valid == should_pass:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False
        
        print(f"  {status}: '{output}' → {'Valid' if is_valid else 'Blocked'}")
    
    return all_passed


def test_critical_pain_level():
    """Test that extreme pain levels escalate appropriately"""
    print("\nTesting Extreme Pain Level Escalation...")
    
    safety = SafetyGuardrails()
    
    ml_prediction = {
        'risk_score': 0.50,
        'confidence': 0.80,
        'is_emergency': False,
        'reasoning': 'Test case'
    }
    
    case_data = {
        'transcript': 'very bad pain',
        'chief_complaint': 'pain',
        'pain_level': 9,  # Extreme pain
        'conscious': True,
        'age': 35,
    }
    
    result = safety.enforce_emergency_override(case_data, ml_prediction)
    
    if result['is_emergency'] and result['risk_score'] >= 0.90:
        print("  ✅ PASS: Extreme pain (9/10) escalated to emergency")
        return True
    else:
        print("  ❌ FAIL: Extreme pain not properly escalated")
        return False


def main():
    print("=" * 70)
    print("EMERGENCY TRIAGE SYSTEM - SAFETY GUARDRAILS TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_critical_symptom_detection,
        test_emergency_bias,
        test_unconscious_override,
        test_genai_output_validation,
        test_critical_pain_level,
    ]
    
    results = []
    for test_func in tests:
        try:
            passed = test_func()
            results.append((test_func.__name__, passed))
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append((test_func.__name__, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✅ ALL SAFETY TESTS PASSED!")
        print("The system is ready for deployment.")
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("Please review and fix the failing tests before deployment.")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
