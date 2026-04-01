#!/usr/bin/env python
"""
Fix HTML translations by completely replacing the translations section
Uses section boundaries to find and replace
"""

import re

# Read file
with open('templates/advanced_assessment.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Build clean translations section
cleaned_section = """const translations = {
            'en': {
                'headerSubtitle': 'Rapid triage system for emergency dispatch',
                'step_1_title': 'Step 1: Patient Information',
                'step_2_title': 'Step 2: Chief Complaint & Symptoms',
                'step_3_title': 'Step 3: Review & Submit',
                'patientName': 'Patient Name',
                'patientAge': 'Age',
                'patientGender': 'Gender',
                'callerPhone': 'Phone Number',
                'location': 'Address',
                'chief_complaint': 'Chief Complaint',
                'symptoms': 'Select all that apply',
                'medicalHistory': 'Medical History',
                'symptomDuration': 'How long have symptoms been present?',
                'nextBtn': 'Next',
                'backBtn': 'Back',
                'submitBtn': 'Submit & Dispatch',
                'reviewSummary': 'Review Summary'
            },
            'mr': {
                'headerSubtitle': 'आपत्कालीन डिस्पॅच साठी द्रुत वर्गीकरण प्रणाली',
                'step_1_title': 'पद्धति 1: रोगीची माहिती',
                'step_2_title': 'पद्धति 2: मुख्य तक्रार व लक्षणे',
                'step_3_title': 'पद्धति 3: पुनरावलोकन व सादर करा',
                'patientName': 'रोगीचे नाव',
                'patientAge': 'वय',
                'patientGender': 'लिंग',
                'callerPhone': 'फोन नंबर',
                'location': 'पत्ता',
                'chief_complaint': 'मुख्य तक्रार',
                'symptoms': 'सर्व लागू असणारे निवडा',
                'medicalHistory': 'वैद्यकीय इतिहास',
                'symptomDuration': 'लक्षणे किती काळ आहे?',
                'nextBtn': 'पुढे',
                'backBtn': 'मागे',
                'submitBtn': 'सादर करा व डिस्पॅच करा',
                'reviewSummary': 'सारांश पुनरावलोकन'
            },
            'ta': {
                'headerSubtitle': 'Emergency dispatch system',
                'step_1_title': 'படி 1: நோயாளி தகவல்',
                'step_2_title': 'படி 2: மூல நோக்கம் & அறிகுறிகள்',
                'step_3_title': 'படி 3: மறுஆய்வு & சமர்ப்பிக்கவும்',
                'patientName': 'நோயாளியின் பெயர்',
                'patientAge': 'வயது',
                'patientGender': 'பாலினம்',
                'callerPhone': 'தொலைபேசி எண்',
                'location': 'முகவரி',
                'chief_complaint': 'மூல நோக்கம்',
                'symptoms': 'பொருந்தக்கூடியவற்றை தேர்ந்தெடுக்கவும்',
                'medicalHistory': 'மருத்துவ வரலாறு',
                'symptomDuration': 'அறிகுறிகள் எவ்வளவு காலம் உள்ளன?',
                'nextBtn': 'அடுத்தது',
                'backBtn': 'பின்னே',
                'submitBtn': 'சமர்ப்பிக்கவும் & விநியோகிக்கவும்',
                'reviewSummary': 'சுருக்கம் மறுபரிசீலனை'
            },
            'kn': {
                'headerSubtitle': 'Emergency dispatch system',
                'step_1_title': 'ಹಂತ 1: ರೋಗಿ ಮಾಹಿತಿ',
                'step_2_title': 'ಹಂತ 2: ಮುಖ್ಯ ಆರೋಪ & ರೋಗ ಲಕ್ಷಣಗಳು',
                'step_3_title': 'ಹಂತ 3: ಪರಿಶೀಲನೆ & ಸಲ್ಲಿಸು',
                'patientName': 'ರೋಗಿಯ ಹೆಸರು',
                'patientAge': 'ವಯಸ್ಸು',
                'patientGender': 'ಪ್ರವೃತ್ತಿ',
                'callerPhone': 'ಫೋನ್ ಸಂಖ್ಯೆ',
                'location': 'ವಿಳಾಸ',
                'chief_complaint': 'ಮುಖ್ಯ ಆರೋಪ',
                'symptoms': 'ಅನ್ವಯವಾಗುವ ಎಲ್ಲವನ್ನೂ ಆಯ್ಕೆ ಮಾಡಿ',
                'medicalHistory': 'ವೈದ್ಯಕೀಯ ಇತಿಹಾಸ',
                'symptomDuration': 'ರೋಗ ಲಕ್ಷಣಗಳು ಎಷ್ಟು ಕಾಲ ಇದೆ?',
                'nextBtn': 'ಮುಂದೆ',
                'backBtn': 'ಹಿಂದೆ',
                'submitBtn': 'ಸಲ್ಲಿಸು & ವಿತರಣೆ ಮಾಡು',
                'reviewSummary': 'ಸಾರಾಂಶ ಪರಿಶೀಲನೆ'
            }
        };"""

# Use regex to replace everything between translations start and the closing brace
pattern = r"const translations = \{.*?\};"
replacement = cleaned_section

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('templates/advanced_assessment.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("SUCCESS: Cleaned HTML translations section")
print("Languages available: English, मराठी, தமிழ், ಕನ್ನಡ")
