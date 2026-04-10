import requests

print('Testing form with age input like user scenario...')
print('=' * 60)

# Test with age: 102 years (like the user showed)
payload = {
    'patientName': 'Raj Kumar',
    'patientAge': '102',
    'patientAgeUnit': 'years',
    'mobileNo': '2536987654',
    'patientGender': 'M',
    'incAddress': 'shankar kalate nagar wakad',
    'incLat': '18.595677',
    'incLong': '73.759011',
    'chiefComplaint': 'Trauma - Bleeding',
    'medicalHistory': 'None'
}

response = requests.post('http://localhost:5000/submit_assessment', json=payload, timeout=15)
result = response.json()
if response.status_code == 200:
    print('✅ SUCCESS')
    print('Patient Name:', result.get('patient_name'))
    print('Age Display:', result.get('patient_age_display'))
    print('Age Years:', result.get('patient_age_years'))
    print('Age Months:', result.get('patient_age_months'))
    print('Gender:', result.get('patient_gender'))
    print()
    print('Expected: 102 years 0 months / M')
    age_display = result.get('patient_age_display')
    print('Actual:', age_display)
    if age_display == '102 years 0 months':
        print('✅ Age display is CORRECT')
    else:
        print('❌ Age display is WRONG')
else:
    print('Error:', response.status_code)
    print(result)
