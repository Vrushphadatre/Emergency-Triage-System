"""
Multi-language support for Emergency Dispatch System
English, Marathi, Tamil, Kannada
"""

TRANSLATIONS = {
    'en': {
        # Form Labels
        'patient_name': 'Patient Name',
        'age': 'Age',
        'gender': 'Gender',
        'phone': 'Phone Number',
        'address': 'Address',
        'chief_complaint': 'Chief Complaint',
        'medical_history': 'Medical History',
        'symptom_duration': 'How long symptoms?',
        
        # Instructions
        'step_1': 'Step 1: Patient Information',
        'step_2': 'Step 2: Chief Complaint & Symptoms',
        'step_3': 'Step 3: Review & Submit',
        'next': 'Next',
        'submit': 'Submit & Dispatch',
        'back': 'Back',
        
        # Placeholders
        'enter_name': 'Enter patient name',
        'enter_phone': 'Enter phone number',
        'enter_address': 'Enter address',
        'enter_history': 'Any medical conditions, surgeries, allergies?',
        
        # Messages
        'no_cases': 'No submitted cases yet',
        'risk_high': 'HIGH RISK',
        'risk_moderate': 'MODERATE RISK',
        'risk_low': 'LOW RISK',
        'instructions': 'Dispatcher Instructions',
        'do_not': 'Do NOT',
    },
    'mr': {  # Marathi - मराठी
        # Form Labels
        'patient_name': 'रोगीचे नाव',
        'age': 'वय',
        'gender': 'लिंग',
        'phone': 'फोन नंबर',
        'address': 'पत्ता',
        'chief_complaint': 'मुख्य तक्रार',
        'medical_history': 'वैद्यकीय इतिहास',
        'symptom_duration': 'लक्षणे किती काळ आहेत?',
        
        # Instructions
        'step_1': 'पद्धति 1: रोगीची माहिती',
        'step_2': 'पद्धति 2: मुख्य तक्रार व लक्षणे',
        'step_3': 'पद्धति 3: पुनरावलोकन व सादर करा',
        'next': 'पुढे',
        'submit': 'सादर करा व डिस्पॅच करा',
        'back': 'मागे',
        
        # Placeholders
        'enter_name': 'रोगीचे नाव प्रविष्ट करा',
        'enter_phone': 'फोन नंबर प्रविष्ट करा',
        'enter_address': 'पत्ता प्रविष्ट करा',
        'enter_history': 'कोणत्या वैद्यकीय स्थितीत, शस्त्रक्रिया, अ‍ॅलर्जी आहे?',
        
        # Messages
        'no_cases': 'अद्याप कोणतेही सादर केलेले प्रकरण नाही',
        'risk_high': 'उच्च जोखीम',
        'risk_moderate': 'मध्यम जोखीम',
        'risk_low': 'कमी जोखीम',
        'instructions': 'डिस्पॅचरच्या सूचना',
        'do_not': 'हे करू नका',
    },
    'ta': {  # Tamil - தமிழ்
        # Form Labels
        'patient_name': 'நோயாளியின் பெயர்',
        'age': 'வயது',
        'gender': 'பாலினம்',
        'phone': 'தொலைபேசி எண்',
        'address': 'முகவரி',
        'chief_complaint': 'மூல நோக்கம்',
        'medical_history': 'மருத்துவ வரலாறு',
        'symptom_duration': 'அறிகுறிகள் எவ்வளவு காலம்?',
        
        # Instructions
        'step_1': 'படி 1: நோயாளி தகவல்',
        'step_2': 'படி 2: மூல நோக்கம் & அறிகுறிகள்',
        'step_3': 'படி 3: மறுஆய்வு & சமர்ப்பிக்கவும்',
        'next': 'அடுத்தது',
        'submit': 'சமர்ப்பிக்கவும் & விநியோகிக்கவும்',
        'back': 'பின்னே',
        
        # Placeholders
        'enter_name': 'நோயாளியின் பெயர் உள்ளிடவும்',
        'enter_phone': 'தொலைபேசி எண் உள்ளிடவும்',
        'enter_address': 'முகவரி உள்ளிடவும்',
        'enter_history': 'மருத்துவ நிலை, அறுவை சிகிற்சை, அலர்ஜி?',
        
        # Messages
        'no_cases': 'இன்னும் சமர்ப்பிக்கப்பட்ட வழக்குகள் இல்லை',
        'risk_high': 'உச்ச ஆபத்து',
        'risk_moderate': 'மிதமான ஆபத்து',
        'risk_low': 'குறைந்த ஆபத்து',
        'instructions': 'விநியோககர்த்தா வழிமுறைகள்',
        'do_not': 'செய்யாதீர்கள்',
    },
    'kn': {  # Kannada - ಕನ್ನಡ
        # Form Labels
        'patient_name': 'ರೋಗಿಯ ಹೆಸರು',
        'age': 'ವಯಸ್ಸು',
        'gender': 'ಪ್ರವೃತ್ತಿ',
        'phone': 'ಫೋನ್ ಸಂಖ್ಯೆ',
        'address': 'ವಿಳಾಸ',
        'chief_complaint': 'ಮುಖ್ಯ ಆರೋಪ',
        'medical_history': 'ವೈದ್ಯಕೀಯ ಇತಿಹಾಸ',
        'symptom_duration': 'ರೋಗ ಲಕ್ಷಣಗಳು ಎಷ್ಟು ಕಾಲ?',
        
        # Instructions
        'step_1': 'ಹಂತ 1: ರೋಗಿ ಮಾಹಿತಿ',
        'step_2': 'ಹಂತ 2: ಮುಖ್ಯ ಆರೋಪ & ರೋಗ ಲಕ್ಷಣಗಳು',
        'step_3': 'ಹಂತ 3: ಪರಿಶೀಲನೆ & ಸಲ್ಲಿಸು',
        'next': 'ಮುಂದೆ',
        'submit': 'ಸಲ್ಲಿಸು & ವಿತರಣೆ ಮಾಡು',
        'back': 'ಹಿಂದೆ',
        
        # Placeholders
        'enter_name': 'ರೋಗಿಯ ಹೆಸರು ನಮೂದಿಸಿ',
        'enter_phone': 'ಫೋನ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ',
        'enter_address': 'ವಿಳಾಸ ನಮೂದಿಸಿ',
        'enter_history': 'ವೈದ್ಯಕೀಯ ಸ್ಥಿತಿ, ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ, ಅಲರ್ಜಿ?',
        
        # Messages
        'no_cases': 'ಇನ್ನೂ ಸಲ್ಲಿಸಿದ ಪ್ರಕರಣಗಳಿಲ್ಲ',
        'risk_high': 'ಹೆಚ್ಚಿನ ಝುಂಬುವ',
        'risk_moderate': 'ಮಧ್ಯಮ ಝುಂಬುವ',
        'risk_low': 'ಕಡಿಮೆ ಝುಂಬುವ',
        'instructions': 'ವಿತರಣಕಾರ ಸೂಚನೆಗಳು',
        'do_not': 'ಮಾಡಬೇಡಿ',
    }
}

# Chief Complaints in Marathi
COMPLAINTS_MARATHI = {
    'Chest pain': 'छातीत दुखापण',
    'Difficulty breathing': 'श्वास घेण्यात अडचण',
    'Stroke symptoms': 'स्ट्रोकचे लक्षणे',
    'Severe allergic reaction': 'गंभीर अ‍ॅलर्जी प्रतिक्रिया',
    'Unconsciousness': 'बेहोशी',
    'Severe trauma': 'गंभीर दुरुस्ती',
    'Seizure': 'दौरे पडणे',
    'Abdominal pain': 'पोटात दुखापण',
    'Headache': 'डोकेदुखी',
    'Fever': 'ताप',
    'Nausea/Vomiting': 'मळमळ / उलट',
    'Cough': 'खोकला',
    'Sore throat': 'घसरान दुखणे',
    'Minor cut/wound': 'लहान जख्म',
    'Rash': 'पोळे येणे',
}

# Chief Complaints in Tamil
COMPLAINTS_TAMIL = {
    'Chest pain': 'மார்பு வலி',
    'Difficulty breathing': 'சுவாச கஷ்டம்',
    'Stroke symptoms': 'பக்ஷாघாத அறிகுறிகள்',
    'Severe allergic reaction': 'கடுமையான ஒவ்வாமை எதிர்வினை',
    'Unconsciousness': 'நிலைதிரிந்த நிலை',
    'Severe trauma': 'கடுமையான காயம்',
    'Seizure': 'வலிப்பு நோய்',
    'Abdominal pain': 'வயிற்று வலி',
    'Headache': 'தலைவலி',
    'Fever': 'காய்ச்சல்',
    'Nausea/Vomiting': 'குமட்டல் / வாந்தி',
    'Cough': 'இருமல்',
    'Sore throat': 'தொண்டை வலி',
    'Minor cut/wound': 'சிறிய வெட்டு/காயம்',
    'Rash': 'தோல் பாதிப்பு',
}

# Chief Complaints in Kannada
COMPLAINTS_KANNADA = {
    'Chest pain': 'ಛಾತಿಯ ನೋವು',
    'Difficulty breathing': 'ಉಸಿರಾಟದ ಕಷ್ಟ',
    'Stroke symptoms': 'ಸ್ಟ್ರೋಕ್ ರೋಗ ಲಕ್ಷಣಗಳು',
    'Severe allergic reaction': 'ತೀವ್ರ ಅಲರ್ಜಿ ಪ್ರತಿಕ್ರಿಯೆ',
    'Unconsciousness': 'ಬೇಹೋಶ್ೆ',
    'Severe trauma': 'ತೀವ್ರ ಆಘಾತ',
    'Seizure': 'ಗಿರುವಾರು',
    'Abdominal pain': 'ಹೊಟ್ಟೆ ನೋವು',
    'Headache': 'ತಲೆನೋವು',
    'Fever': 'ಜ್ವರ',
    'Nausea/Vomiting': 'ವಮನ ಪ್ರವೃತ್ತಿ / ವಾಕುನಿ',
    'Cough': 'ಕೆಮ್ಮು',
    'Sore throat': 'ಗಂಟಲು ಬೆಚ್ಚುವಿಕೆ',
    'Minor cut/wound': 'ಚಿಕ್ಕ ಕತ್ತರಿ/ಗಾಯ',
    'Rash': 'ತ್ವಕ್ ದಾಹ',
}

def get_text(key: str, language: str = 'en') -> str:
    """
    Get translated text
    
    Args:
        key: Translation key
        language: Language code ('en', 'mr', 'ta', 'kn')
        
    Returns:
        Translated text or key if not found
    """
    if language not in TRANSLATIONS:
        language = 'en'
    
    return TRANSLATIONS[language].get(key, key)

def get_complaints_list(language: str = 'en') -> dict:
    """
    Get chief complaints in specified language
    
    Args:
        language: Language code ('en', 'mr', 'ta', 'kn')
        
    Returns:
        Dictionary of complaints
    """
    if language == 'mr':
        return COMPLAINTS_MARATHI
    elif language == 'ta':
        return COMPLAINTS_TAMIL
    elif language == 'kn':
        return COMPLAINTS_KANNADA
    
    # Default English - return keys as they are
    return {k: k for k in COMPLAINTS_MARATHI.keys()}

def translate_complaint(complaint_en: str, to_language: str = 'mr') -> str:
    """
    Translate complaint from English to target language
    """
    if to_language == 'mr':
        return COMPLAINTS_MARATHI.get(complaint_en, complaint_en)
    elif to_language == 'ta':
        return COMPLAINTS_TAMIL.get(complaint_en, complaint_en)
    elif to_language == 'kn':
        return COMPLAINTS_KANNADA.get(complaint_en, complaint_en)
    return complaint_en

def get_supported_languages() -> dict:
    """Return all supported languages with flags"""
    return {
        'en': '🇬🇧 English',
        'mr': '🇮🇳 मराठी',
        'ta': '🇮🇳 தமிழ்',
        'kn': '🇮🇳 ಕನ್ನಡ'
    }
