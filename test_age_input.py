import requests

print("=" * 70)
print("AGE INPUT UNIT CONVERSION TEST")
print("=" * 70)

# Test 1: Years
print("\n[TEST 1] Age in Years (35 years)")
print("-" * 70)
payload1 = {
    'patientName': 'John Doe',
    'patientAge': '35',
    'patientAgeUnit': 'years',
    'mobileNo': '9876543210',
    'patientGender': 'M',
    'incAddress': 'Mumbai',
    'incLat': '19.0760',
    'incLong': '72.8777',
    'chiefComplaint': 'Chest pain',
    'medicalHistory': 'Hypertension'
}
response1 = requests.post('http://localhost:5000/submit_assessment', json=payload1, timeout=15)
if response1.status_code == 200:
    r1 = response1.json()
    print(f"✅ Patient: {r1.get('patient_name')}")
    print(f"   Input: 35 years")
    print(f"   Stored: {r1.get('patient_age_years')} years {r1.get('patient_age_months')} months")
    print(f"   Display: {r1.get('patient_age_display')}")
    print(f"   Gender: {r1.get('patient_gender')}")
else:
    print(f"❌ ERROR: {response1.status_code}")

# Test 2: Months
print("\n[TEST 2] Age in Months (18 months)")
print("-" * 70)
payload2 = {
    'patientName': 'Baby Child',
    'patientAge': '18',
    'patientAgeUnit': 'months',
    'mobileNo': '9876543211',
    'patientGender': 'F',
    'incAddress': 'Delhi',
    'incLat': '28.7041',
    'incLong': '77.1025',
    'chiefComplaint': 'Fever',
    'medicalHistory': 'None'
}
response2 = requests.post('http://localhost:5000/submit_assessment', json=payload2, timeout=15)
if response2.status_code == 200:
    r2 = response2.json()
    print(f"✅ Patient: {r2.get('patient_name')}")
    print(f"   Input: 18 months")
    print(f"   Stored: {r2.get('patient_age_years')} years {r2.get('patient_age_months')} months")
    print(f"   Display: {r2.get('patient_age_display')}")
    print(f"   Gender: {r2.get('patient_gender')}")
else:
    print(f"❌ ERROR: {response2.status_code}")

# Test 3: Days
print("\n[TEST 3] Age in Days (500 days)")
print("-" * 70)
payload3 = {
    'patientName': 'Infant Patient',
    'patientAge': '500',
    'patientAgeUnit': 'days',
    'mobileNo': '9876543212',
    'patientGender': 'M',
    'incAddress': 'Bangalore',
    'incLat': '12.9716',
    'incLong': '77.5946',
    'chiefComplaint': 'Vomiting',
    'medicalHistory': 'None'
}
response3 = requests.post('http://localhost:5000/submit_assessment', json=payload3, timeout=15)
if response3.status_code == 200:
    r3 = response3.json()
    print(f"✅ Patient: {r3.get('patient_name')}")
    print(f"   Input: 500 days (~16.67 months)")
    print(f"   Stored: {r3.get('patient_age_years')} years {r3.get('patient_age_months')} months")
    print(f"   Display: {r3.get('patient_age_display')}")
    print(f"   Gender: {r3.get('patient_gender')}")
else:
    print(f"❌ ERROR: {response3.status_code}")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETED")
print("=" * 70)
