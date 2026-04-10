import requests

payload = {
    'patientName': 'Test User',
    'patientAge': '5',
    'patientAgeUnit': 'years',
    'mobileNo': '9876543210',
    'patientGender': 'M',
    'incAddress': 'Delhi',
    'incLat': '28.7041',
    'incLong': '77.1025',
    'chiefComplaint': 'Fever',
    'medicalHistory': 'None'
}

response = requests.post('http://localhost:5000/submit_assessment', json=payload, timeout=15)
result = response.json()
if response.status_code == 200:
    print('✅ SUCCESS - Age capture working')
    print(f'Patient: {result.get("patient_name")}')
    print(f'Age Display: {result.get("patient_age_display")}')
    print(f'Age Years: {result.get("patient_age_years")}')
    print(f'Age Months: {result.get("patient_age_months")}')
else:
    print(f'Error: {response.status_code}')
    print(result)
