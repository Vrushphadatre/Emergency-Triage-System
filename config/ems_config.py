# EMS System Configuration - Chief Complaints and Multilingual Support

# ============================================================================
# REAL-TIME EMERGENCY DETECTION (Life-Threatening Complaints)
# These trigger IMMEDIATE high-priority dispatch (even before full assessment)
# ============================================================================
IMMEDIATE_EMERGENCY_COMPLAINTS = {
    "Chest pain",
    "Breathing Difficulty",
    "Unconscious / unresponsive patient",
    "Convulsions / Fits / Seizures",
    "Road traffic accident: general",
    "Road traffic accident: vehicle on fire",
    "Road traffic accident: pinned / struck patient",
    "Trauma - Head injury",
    "Trauma - Bleeding",
    "Drowning / Near Drowning",
    "Electrocution / lightning strike",
    "Hematemesis [vomiting blood]",
    "Overdose / poisoning",
    "Pregnancy - bleeding",
    "Pregnancy - baby delivered",
    "Choking",
    "Paralysis / stroke",
    "Hazardous matter exposure",
}

# When emergency detected, auto-dispatch = TRUE (risk_score automatically = HIGH)
# Notify dispatcher: "IMMEDIATE_EMERGENCY - Dispatch without delay"

# ============================================================================
# EMS CHIEF COMPLAINT CATEGORIES (From your system - 80+ categories)
# ============================================================================

EMS_CHIEF_COMPLAINTS = {
    "Pain in abdomen/stomach": "पोटात/पोटाच्या क्षेत्रात दर्द",
    "Abnormal Behavior [Delirium]": "असामान्य वर्तन [भ्रम]",
    "Allergic reaction": "अ allergीक प्रतिक्रिया",
    "Confusion or altered mental status": "गोंधळ किंवा बदलले मानसिक स्थिती",
    "Animal Bite": "जनावराचा चावा",
    "Attack / Assault": "हल्ला / आक्रमण",
    "Back Pain": "पाठीचा दर्द",
    "Breathing Difficulty": "श्वसन कठिनाई",
    "Burns": "जळे",
    "Chest pain": "छातीचा दर्द",
    "Choking": "गुदमरणे",
    "Diarrhea / Loose motions": "दस्त / सैल मलमूत्र",
    "Drowning / Near Drowning": "बुडणे / जवळपास बुडणे",
    "Dizziness": "चक्कर",
    "Electrocution / lightning strike": "विद्युत शॉक / वीज आघात",
    "Eye pain": "डोळ्याचा दर्द",
    "Fainting": "बेहोशी",
    "Fall from Height": "उंचीवरून पडणे",
    "Fever": "ज्वर",
    "Hazardous matter exposure": "हानिकारक पदार्थाचा संपर्क",
    "Headache": "डोकेदुखी",
    "Hematemesis [vomiting blood]": "रक्त उलट्या",
    "Low sugar level": "निम्न शर्करा स्तर",
    "Low body temperature": "कम शरीर तापमान",
    "Heat stroke": "उष्ण लहर",
    "Overdose / poisoning": "अतिमात्रा / विषबाधा",
    "Pregnancy - bleeding": "गर्भावस्था - रक्तस्राव",
    "Pregnancy - abdominal pain / labor pain": "गर्भावस्था - पोटदर्द / प्रसव दर्द",
    "Pregnancy - baby delivered": "गर्भावस्था - बाळ जन्मले",
    "Psychiatric problems": "मानसिक समस्या",
    "Paralysis / stroke": "पक्षाघात / स्ट्रोक",
    "Child patient / Pediatric patient": "बाल रोगी / बालरोग रोगी",
    "Road traffic accident: general": "रस्ता अपघात: सामान्य",
    "Road traffic accident: auto - pedestrian": "रस्ता अपघात: ऑटो - पदचारी",
    "Road traffic accident: ejection from vehicle": "रस्ता अपघात: वाहनातून बाहेर निकालणे",
    "Road traffic accident: vehicle rollover": "रस्ता अपघात: वाहन पलटणे",
    "Road traffic accident: vehicle off bridge/height": "रस्ता अपघात: पुलावरून वाहन",
    "Road traffic accident: Pediatric patient": "रस्ता अपघात: बालरोग रोगी",
    "Road traffic accident: Pregnant lady": "रस्ता अपघात: गर्भवती महिला",
    "Road traffic accident: pinned / struck patient": "रस्ता अपघात: अडकलेला रोगी",
    "Road traffic accident: vehicle on fire": "रस्ता अपघात: आग लागलेले वाहन",
    "Accident of boat/ship": "बोट/जहाज अपघात",
    "Convulsions / Fits / Seizures": "आक्षेप / दौरे / झटके",
    "Trauma - abdominal": "आघात - पोटात",
    "Trauma - Bleeding": "आघात - रक्तस्राव",
    "Trauma - chest wall": "आघात - छाती भिंत",
    "Trauma - Head injury": "आघात - डोक्यात दुखापत",
    "Trauma - Gunshot injury": "आघात - बंदूकीचा गोळी",
    "Vomiting": "उलट्या",
    "Unconscious / unresponsive patient": "बेशुद्ध / प्रतिक्रिया नसलेला रोगी",
    "Weakness": "कमजोरी",
    "Sick Room Treatment": "आजारी खोली उपचार",
    "Suicide attempt": "आत्महत्या प्रयत्न",
    "Pregnancy Care": "गर्भावस्था काळजी",
    "Child Care call": "बालकांची काळजी कॉल",
    "Drop Back Call": "ड्रॉप बैक कॉल",
    "Corona": "कोरोना",
    "Corona HD": "कोरोना एचडी",
    "Body Pain / Swelling": "शरीरदर्द / सूज",
    "Joint Pain": "जोडणीचा दर्द",
    "Cough & Cold": "खोकला & सर्दी",
    "Worm Infection": "कृमि संक्रमण",
    "Gastritis": "जठरशोथ",
    "Anemia": "अक्षमता",
    "Urine Problem": "मूत्र समस्या",
    "BP Checkup": "रक्तदाब तपासणी",
    "Toothache / Dental Pain": "दातदुखी / दंत दर्द",
    "Mouth Ulcer / Infection": "तोंडाचा अल्सर / संक्रमण",
    "Skin Infection": "त्वचा संक्रमण",
    "Ear Pain / Infection": "कान दर्द / संक्रमण",
    "Acidity": "अम्लता",
    "Throat Infection": "घसरा संक्रमण",
    "Hypertension": "उच्च रक्तदाब",
    "Body Itching": "शरीर खुजली",
    "Fungal Infection": "बुरशी संक्रमण",
    "Vertigo": "चक्कर",
    "Numbness": "अंगमर्दन",
    "Giddiness / Fainting": "सुस्ती / बेहोशी",
    "General Weakness": "सामान्य कमजोरी",
    "Joint Pain - Body Movement Difficulty": "जोडणीचा दर्द - शरीर हालचाल कठिनाई",
    "Loose motion - Vomiting": "सैल मलमूत्र - उलट्या",
    "Traumatic Injury": "दर्दनाक जखम",
    "RTA (Road Traffic Accident)": "आरटीए (रस्ता अपघात)",
    "Other": "इतर"
}

# ============================================================================
# DYNAMIC QUESTIONS BASED ON CHIEF COMPLAINT TYPE
# CLINICALLY GROUNDED IN EMS PROTOCOLS:
# - OPQRST for cardiac complaints
# - ABC for trauma/breathing
# - HEILO for neuro/OB
# ============================================================================

COMPLAINT_SPECIFIC_QUESTIONS = {
    "Chest pain": {
        "protocol": "OPQRST - Cardiac Assessment",
        "icon": "🫀",
        "en": [
            "Did pain start suddenly or gradually? (Onset)",
            "What provokes/relieves the pain? Exertion, rest, position?",
            "How would you describe the quality? Sharp, pressure, heaviness, burning?",
            "Does the pain travel to arm, neck, back, or jaw? (Radiation)",
            "On scale 1-10, how severe is the pain? (Severity)",
            "How long has the pain lasted? (Timing)",
            "Do you have shortness of breath, sweating, or nausea?",
            "Any history of heart disease or diabetes?"
        ],
        "mr": [
            "दर्द अचानक शुरु हुआ किंवा धीरे धीरे?",
            "काय दर्द वाढवते किंवा कमी करते? व्यायाम, विश्राम?",
            "दर्दाची गुणवत्ता कशी आहे? तीव्र, दबाव, भारीपना?",
            "दर्द हात, गर्दन, पाठीला, किंवा जबडा चा लागतो का?",
            "दर्द 1-10 पर किती तीव्र आहे?",
            "दर्द किती वेळ चालू आहे?",
            "श्वसन कठिनाई, घाम, किंवा मळमळ आहे का?",
            "हृदय रोग किंवा मधुमेह इतिहास?"
        ]
    },
    "Breathing Difficulty": {
        "protocol": "ABC Assessment - Airway, Breathing, Circulation",
        "icon": "🫁",
        "en": [
            "Rate breathing difficulty 1-10 (1=mild, 10=severe)",
            "Can you speak complete sentences or just words?",
            "What color are lips/nails? Normal, pale, blue?",
            "Do you hear wheezing, whistling, or stridor (high-pitched)?",
            "Is there cough? Productive with mucus/blood or dry?",
            "Any chest pain with breathing?",
            "Recent illness, allergies, or choking incident?",
            "Current medications or respiratory conditions?"
        ],
        "mr": [
            "श्वसन कठिनाई 1-10 वर किती गंभीर आहे?",
            "तुम्ही संपूर्ण वाक्य बोलू शकता किंवा फक्त शब्द?",
            "ओठ/नख रंग काय आहे? सामान्य, फिकट, निळा?",
            "सीटी, सांस लाचणे किंवा उच्च-पिच्ड आवाज आहे का?",
            "खोकला आहे का? बलगम/रक्त किंवा सुका?",
            "श्वसनात छातीचा दर्द आहे का?",
            "अलीकडे आजारी, अ allergीक, किंवा गुदमरण?",
            "वर्तमान औषधे किंवा श्वसन स्थिती?"
        ]
    },
    "Trauma - Head injury": {
        "protocol": "GCS + Head Trauma Assessment",
        "icon": "🧠",
        "en": [
            "How was the head injured? (Fall, impact, object?)",
            "Is patient conscious and alert? Any confusion?",
            "Any loss of consciousness? How long?",
            "Headache severity (1-10)? Vomiting?",
            "Any visible bleeding, bruising, or deformity?",
            "Can patient remember the incident?",
            "Any seizures or abnormal movements?",
            "Currently on blood thinners or anticoagulants?"
        ],
        "mr": [
            "डोक्यात चोट कसे लागली? पडणे, आघात, वस्तु?",
            "रोगी सचेत आणि सतर्क आहे का? भ्रम?",
            "चेतना नष्ट झाली का? किती वेळ?",
            "डोकेदुखी गंभीरता (1-10)? उलट्या?",
            "दृश्यमान रक्तस्राव, मार, विकृती?",
            "रोगी घटना लक्षात ठेवू शकतो का?",
            "दौरे किंवा असामान्य हालचाल?",
            "वर्तमान रक्त पातळीकरण औषधे?"
        ]
    },
    "Road traffic accident: general": {
        "protocol": "Trauma Alert - Mechanism of Injury",
        "icon": "🚗",
        "en": [
            "Type of accident? (Car-car, car-bike, pedestrian?)",
            "How many vehicles/people involved?",
            "Was patient ejected? Seatbelt used?",
            "Vehicle damage severity? (Minor, Moderate, Severe?)",
            "Any visible injuries? Bleeding? Deformity?",
            "Can patient move all limbs? Numbness/tingling?",
            "High speed impact? (>40 km/h?)",
            "Approximate time since accident?"
        ],
        "mr": [
            "अपघाताचा प्रकार? कार-कार, बाईक, पदचारी?",
            "किती वाहने/लोक जिंकले?",
            "रोगी बाहेर निकाला गेला? सीट बेल्ट होती?",
            "वाहन नुकसान गंभीरता? किती गंभीर?",
            "दृश्यमान जखमे? रक्तस्राव? विकृती?",
            "रोगी सर्व अंग हलवू शकतो? सुन्नपणा?",
            "उच्च गती आघात? (>40 किमी/तास?)",
            "अपघातानंतर अंदाजे वेळ?"
        ]
    },
    "Trauma - Bleeding": {
        "protocol": "Hemorrhage Control - Tourniquet Protocol",
        "icon": "🩸",
        "en": [
            "Where is the bleeding from? (Limb, torso, head?)",
            "Is bleeding active or controlled? How profuse?",
            "Estimated blood loss? (Small, Moderate, <2units, >2units?)",
            "How long has patient been bleeding?",
            "Is there an object impaled in wound? (DO NOT REMOVE)",
            "Can you apply direct pressure safely?",
            "Any other injuries besides bleeding?",
            "Is patient conscious? Dizziness/weakness?"
        ],
        "mr": [
            "रक्तस्राव कुठून? हात, धड, डोक?",
            "सक्रिय किंवा नियंत्रित? किती तीव्र?",
            "अनुमानित रक्त हानि? कमी, मध्यम, मोठा?",
            "रोगी किती वेळ रक्त बहा रहा आहे?",
            "घावात अटकली वस्तु? काढू नका",
            "तुम्ही सरळ दबाव सुरक्षितपणे लागू करू शकता?",
            "रक्तस्राव व्यतिरिक्त इतर जखमे?",
            "रोगी सचेत? चक्कर/कमजोरी?"
        ]
    },
    "Unconscious / unresponsive patient": {
        "protocol": "AVPU Scale + ABC Assessment",
        "icon": "😴",
        "en": [
            "How long unconscious? Witnessed event?",
            "Last known normal activity before unconsciousness?",
            "Recent illness, injury, or medication change?",
            "Breathing: Normal, slow, rapid, gasping, absent?",
            "Skin: Warm/dry, cold/clammy, pale, flushed, blue?",
            "Any seizures, jerking, or rigidity?",
            "Pupils: Equal/reactive, dilated, or pinpoint?",
            "Known medical conditions? Diabetes, seizures, heart?"
        ],
        "mr": [
            "अचेत किती वेळ? साक्षी घटना आहे का?",
            "अचेतता आधी अंतिम सामान्य क्रियाकलाप?",
            "अलीकडे आजारी, चोट, औषध बदल?",
            "श्वसन: सामान्य, मंद, द्रुत, हांफणे, नाही?",
            "त्वचा: उष्ण, थंड-चिकट, फिकट, लाल, निळा?",
            "दौरे, झटके, किंवा कडकपणा?",
            "पुतलिया: समान/प्रतिक्रियाशील, विस्तृत?",
            "मधुमेह, हृदय रोग, दौरे?"
        ]
    },
    "Convulsions / Fits / Seizures": {
        "protocol": "Seizure Assessment - Safety Protocol",
        "icon": "⚡",
        "en": [
            "Is patient currently seizing or post-ictal?",
            "How long has seizure been occurring?",
            "First-time seizure or history of epilepsy?",
            "Any head trauma or fever before seizure?",
            "On anti-seizure medications? Missed doses?",
            "Tongue bitten, saliva frothy, incontinent?",
            "Is patient breathing effectively?",
            "Recent medication, drug, or alcohol?"
        ],
        "mr": [
            "रोगी वर्तमानात दौरे किंवा उपरांत?",
            "दौरा किती वेळ चालू आहे?",
            "पहिला दौरा किंवा एपिलेप्सी इतिहास?",
            "दौर्याआधी डोक्यात चोट किंवा ज्वर?",
            "विरोधी-दौरे औषधे? गमावलेले डोज?",
            "जिभ चावली, लार फेसबुक, अपवर्लीय?",
            "रोगी प्रभावीपणे श्वसन करत आहे?",
            "औषध, ड्रग, मद?"
        ]
    },
    "Pregnancy - abdominal pain / labor pain": {
        "protocol": "OB/GYN HEILO Assessment",
        "icon": "🤰",
        "en": [
            "How many weeks/months pregnant?",
            "Contractions: Frequency? Duration? Intensity (1-10)?",
            "Any vaginal bleeding or discharge? Color?",
            "Last menstrual period date? Due date?",
            "Previous pregnancies/complications?",
            "Regular prenatal checkups and ultrasounds normal?",
            "Fever, chills, foul odor discharge?",
            "Feel baby movements? Membranes ruptured (water broke)?"
        ],
        "mr": [
            "किती आठवडे/महिने गर्भवती?",
            "संकुचन: वारंवारता? अवधी? तीव्रता (1-10)?",
            "योनी रक्तस्राव किंवा भारी स्राव? रंग?",
            "शेवटचे मासिक पीरियड? नियत तारीख?",
            "पिछली गर्भावस्था? जटिलता?",
            "प्रसवपूर्व काळजी: नियमित तपास? अल्ट्रासाउंड?",
            "ज्वर, थरथराहट, दुर्गंध?",
            "बाळाची हालचाल? पाण्याचा फुटणे?"
        ]
    },
    "Overdose / poisoning": {
        "protocol": "Toxidrome Assessment - Poison Control",
        "icon": "☠️",
        "en": [
            "What substance was ingested? Amount? When?",
            "Route of exposure? (Ingested, inhaled, injected, skin?)",
            "Is patient conscious and responsive?",
            "Breathing: Normal, slow, rapid, gasping?",
            "Any seizures or unusual behavior?",
            "Pupils: Normal, dilated, or pinpoint?",
            "Skin: Warm/dry, cool/clammy, flushed, cyanotic?",
            "Any vomiting, burns to mouth/lips? Container available?"
        ],
        "mr": [
            "कोणता पदार्थ गिळला? किती? कधी?",
            "संपर्क मार्ग? गिळले, श्वसन, इंजेक्शन?",
            "रोगी सचेत आणि प्रतिक्रियाशील?",
            "श्वसन: सामान्य, मंद, द्रुत, हांफणे?",
            "दौरे किंवा अस्वाभाविक वर्तन?",
            "पुतलिया: सामान्य, विस्तृत, पिनपॉइंट?",
            "त्वचा: उष्ण, थंड, लाल, नीली?",
            "उलट्या, जळे? कंटेनर उपलब्ध?"
        ]
    }
}

# ============================================================================
# UNKNOWN PATIENT MODE - CRITICAL FOR BYSTANDER REPORTS
# When caller does NOT know patient (found person, stranger, etc.)
# ============================================================================

UNKNOWN_PATIENT_MODE_QUESTIONS = {
    "en": [
        "Do you know the patient's name?",
        "Is the patient conscious and responsive?",
        "Approximate age - infant, child, adult, elderly?",
        "Male or female?",
        "Your name (caller)?",
        "Your mobile number?",
        "Your relationship to patient? (Bystander, friend, family?)"
    ],
    "mr": [
        "तुम्हाला रोगीचे नाव माहित आहे का?",
        "रोगी सचेत आणि प्रतिक्रियाशील आहे का?",
        "अंदाजे वय - बाळ, मुल, प्रौढ, वृद्ध?",
        "पुरुष किंवा स्त्री?",
        "तुमचे नाव (कॉल करणारे)?",
        "तुमचा मोबाइल नंबर?",
        "रोगीशी तुमचे नाते? (अजनबी, मित्र, कुटुंब?)"
    ]
}

# ============================================================================
# UI TRANSLATIONS (English & Marathi) - UPDATED FOR UNKNOWN PATIENT MODE
# ============================================================================

UI_TRANSLATIONS = {
    "header": {
        "en": "🚑 Emergency Triage Assessment",
        "mr": "🚑 आपातकालीन ट्राइएज मूल्यांकन"
    },
    "patient_known_question": {
        "en": "Do you know the patient?",
        "mr": "तुम्हाला रोगी माहित आहे का?"
    },
    "patient_known_yes": {
        "en": "Yes, I know the patient",
        "mr": "होय, मी रोगी ओळखतो"
    },
    "patient_known_no": {
        "en": "No, I found them/bystander report",
        "mr": "नाही, मी त्यांना शोधले/अजनबी रिपोर्ट"
    },
    "patient_name": {
        "en": "Patient Name (Optional)",
        "mr": "रोगी का नाम (वैकल्पिक)"
    },
    "patient_name_placeholder": {
        "en": "Enter name if known",
        "mr": "नाम दर्ज करें यदि ज्ञात हो"
    },
    "caller_name": {
        "en": "Your Name (Required)",
        "mr": "आपका नाम (आवश्यक)"
    },
    "caller_name_placeholder": {
        "en": "Caller/Reporter name",
        "mr": "कॉलर/रिपोर्टर नाम"
    },
    "mobile_number": {
        "en": "Mobile Number (10 digits)",
        "mr": "मोबाइल नंबर (10 अंक)"
    },
    "mobile_placeholder": {
        "en": "10-digit number (e.g., 9876543210)",
        "mr": "10-अंकीय नंबर (जैसे 9876543210)"
    },
    "current_location": {
        "en": "Current Location (Where is the emergency?)",
        "mr": "मौजूदा स्थान (आपातकाल कहां है?)"
    },
    "location_placeholder": {
        "en": "Enter address or landmark",
        "mr": "पता या स्थलचिन्ह दर्ज करें"
    },
    "patient_age": {
        "en": "Patient Age (years) - Optional",
        "mr": "रोगी की आयु (वर्ष) - वैकल्पिक"
    },
    "patient_gender": {
        "en": "Patient Gender",
        "mr": "रोगी का लिंग"
    },
    "male": {
        "en": "Male",
        "mr": "पुरुष"
    },
    "female": {
        "en": "Female",
        "mr": "स्त्री"
    },
    "chief_complaint": {
        "en": "Chief Complaint",
        "mr": "मुख्य शिकायत"
    },
    "select_complaint": {
        "en": "Select main complaint...",
        "mr": "मुख्य शिकायत चुनें..."
    },
    "medical_history": {
        "en": "Medical History (Optional - leave blank if unknown)",
        "mr": "चिकित्सा इतिहास (वैकल्पिक - यदि अज्ञात हो तो रिक्त छोड़ें)"
    },
    "medical_history_placeholder": {
        "en": "Any conditions? (diabetes, asthma, etc.)",
        "mr": "कोई स्थितियां? (मधुमेह, अस्थमा, आदि)"
    },
    "begin_assessment": {
        "en": "Submit Emergency Report",
        "mr": "आपातकालीन रिपोर्ट सबमिट करें"
    },
    "please_fill_required": {
        "en": "Please fill all required fields (*)",
        "mr": "कृपया सभी आवश्यक फ़ील्ड भरें (*)"
    },
    "invalid_phone": {
        "en": "Invalid phone number. Please enter 10 digits.",
        "mr": "अमान्य फोन नंबर। कृपया 10 अंक दर्ज करें।"
    },
    "immediate_emergency_alert": {
        "en": "🚨 IMMEDIATE EMERGENCY - Ambulance dispatching without delay!",
        "mr": "🚨 तत्काल आपातकाल - एम्बुलेंस तुरंत भेजा जा रहा है!"
    },
    "language": {
        "en": "English",
        "mr": "मराठी"
    },
    "risk_assessment": {
        "en": "🏥 Risk Assessment Result",
        "mr": "🏥 जोखिम मूल्यांकन परिणाम"
    },
    "risk_score": {
        "en": "Risk Score",
        "mr": "जोखिम स्कोर"
    },
    "recommendation": {
        "en": "Recommendation",
        "mr": "सिफारिश"
    },
    "high_risk": {
        "en": " HIGH RISK - Emergency Department (Ambulance Dispatched)",
        "mr": "🔴 उच्च जोखिम - आपातकालीन विभाग (एम्बुलेंस भेजा गया)"
    },
    "moderate_risk": {
        "en": "🟡 MODERATE RISK - Urgent Care",
        "mr": "🟡 मध्यम जोखिम - तत्काल देखभाल"
    },
    "low_risk": {
        "en": "🟢 LOW RISK - Routine Care",
        "mr": "🟢 कम जोखिम - नियमित देखभाल"
    },
    "ambulance_dispatch": {
        "en": "🚑 Ambulance Dispatch Initiated",
        "mr": "🚑 एम्बुलेंस डिस्पैच शुरू किया गया"
    },
    "estimated_arrival": {
        "en": "Estimated Arrival",
        "mr": "अनुमानित आगमन"
    },
    "minutes": {
        "en": "minutes",
        "mr": "मिनट"
    },
    "case_id": {
        "en": "Case ID",
        "mr": "केस आईडी"
    },
    "unidentified_patient": {
        "en": "⚠️ UNIDENTIFIED PATIENT - Bystander Report",
        "mr": "⚠️ अज्ञात रोगी - अजनबी रिपोर्ट"
    }
}

# ============================================================================
# VALIDATION RULES
# ============================================================================

PHONE_REGEX = r"^[6-9]\d{9}$"  # Indian 10-digit starting with 6-9
LOCATION_MIN_LENGTH = 5
NAME_MIN_LENGTH = 2
CALLER_NAME_MIN_LENGTH = 2

#  # ============================================================================
# EMERGENCY RESPONSE TIMES
# ============================================================================

IMMEDIATE_EMERGENCY_AUTO_DISPATCH = True  # Auto-dispatch on immediate complaints
IMMEDIATE_EMERGENCY_ETA = 8  # Standard ETA in minutes for ambulances
