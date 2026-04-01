# Emergency Triage System - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Complete Setup
```powershell
python scripts/setup_system.py
```

This single command will:
- Generate synthetic training data
- Initialize the database
- Train the ML model
- Verify all components

### 3. Start the Application
```powershell
python app.py
```

### 4. Access the System
Open your browser and navigate to:

- **Patient Intake**: http://localhost:5000/
- **Dispatcher Console**: http://localhost:5000/dispatcher
- **Nurse Queue**: http://localhost:5000/nurse
- **KPI Dashboard**: http://localhost:5000/dashboard
- **Health Check**: http://localhost:5000/health

---

## 🎯 Quick Demo Workflow

### Patient Intake Simulation

1. Go to http://localhost:5000/
2. Click "Start Assessment"
3. Answer the questions (try these for testing):

**Emergency Case:**
- "I have severe chest pain and can't breathe"
- "Started 30 minutes ago"
- "Pain is 9 out of 10"
- "Yes, conscious"
- "I'm 58 years old"
- "High blood pressure"

**Non-Emergency Case:**
- "I have a mild headache"
- "Started 2 days ago"
- "Pain is 3 out of 10"
- "Yes, conscious"
- "I'm 34 years old"
- "No medical conditions"

### Dispatcher Console
1. Go to http://localhost:5000/dispatcher
2. View emergency cases in queue
3. Click "Dispatch Ambulance" or "Refer to Nurse"
4. Add notes and confirm

### Nurse Queue
1. Go to http://localhost:5000/nurse
2. View non-emergency cases
3. Choose action: Callback, Self-Care, Clinic Referral, or Escalate

### KPI Dashboard
1. Go to http://localhost:5000/dashboard
2. View real-time metrics
3. Monitor queue lengths
4. Check performance against targets

---

## 🧪 Testing Safety Guardrails

Run the safety test suite:
```powershell
python tests/test_safety.py
```

This validates:
- Critical symptom detection
- Emergency bias for low confidence
- Unconscious patient override
- GenAI output validation
- Pain level escalation

---

## 📁 Project Structure

```
emergency-triage-mvp/
├── app.py                     # Main Flask application
├── config.py                  # Configuration & thresholds
├── requirements.txt           # Dependencies
├── data/
│   └── synthetic_training_data.py
├── models/
│   └── ml_model.py           # ML classifier
├── genai/
│   ├── intake_agent.py       # Conversational intake
│   └── explanation_layer.py  # Risk score explainer
├── safety/
│   └── guardrails.py         # Safety rules
├── routing/
│   └── decision_router.py    # Case routing
├── database/
│   └── models.py             # Database schema
├── templates/                # Web UI
│   ├── intake.html
│   ├── dispatcher.html
│   ├── nurse.html
│   └── dashboard.html
└── scripts/
    ├── setup_system.py       # One-command setup
    └── train_model.py        # Model training
```

---

## 🔧 Manual Setup (If Needed)

If you prefer to run steps individually:

### Step 1: Generate Training Data
```powershell
python -c "from data.synthetic_training_data import generate_training_data; generate_training_data(1000, 'data/training_data.csv')"
```

### Step 2: Initialize Database
```powershell
python scripts/init_database.py
```

### Step 3: Train ML Model
```powershell
python scripts/train_model.py
```

### Step 4: Start Application
```powershell
python app.py
```

---

## ⚙️ Configuration

Edit `config.py` to adjust:

### Safety Thresholds
```python
EMERGENCY_THRESHOLD = 0.65      # Risk score for emergency
CONFIDENCE_THRESHOLD = 0.70     # Confidence for safety bias
```

### Critical Symptoms (Mandatory Escalation)
```python
CRITICAL_SYMPTOMS = [
    "chest pain",
    "difficulty breathing",
    "unconscious",
    # ... add more
]
```

### Routing Rules
```python
ROUTING_RULES = {
    "emergency": {
        "min_score": 0.65,
        "queue": "dispatcher",
        "sla_minutes": 2,
    },
    # ...
}
```

---

## 📊 Understanding the Risk Score

The ML model outputs a risk score from 0.0 to 1.0:

- **0.85 - 1.0**: CRITICAL - Immediate dispatch
- **0.65 - 0.84**: HIGH - Emergency dispatch
- **0.40 - 0.64**: MEDIUM - Nurse review
- **0.0 - 0.39**: LOW - Routine callback

**Safety Bias**: When confidence < 70%, the system errs on the side of escalation.

---

## 🛡️ Safety Features

### 1. Mandatory Escalation
These symptoms automatically trigger emergency:
- Chest pain
- Breathing difficulty
- Unconscious
- Severe bleeding
- Stroke symptoms

### 2. Emergency Bias
- Low confidence (< 70%) → default to emergency
- Moderate risk + low confidence → escalate

### 3. Human Override
- All AI recommendations require human confirmation
- Override reasons are logged for feedback
- No autonomous dispatch decisions

### 4. Audit Trail
- Every action is logged
- Complete conversation history preserved
- ML predictions vs. human outcomes tracked

---

## 🎓 For Stakeholder Demos

### Demo Script

1. **Introduction** (2 min)
   - Show architecture diagram (README)
   - Explain human-in-the-loop approach

2. **Patient Intake Demo** (5 min)
   - Run through emergency case
   - Show ML risk assessment
   - Show safety override in action

3. **Dispatcher Console** (3 min)
   - Show case queue
   - Demonstrate decision workflow
   - Show override capability

4. **KPI Dashboard** (3 min)
   - Show real-time metrics
   - Explain accuracy tracking
   - Highlight false-negative monitoring

5. **Safety Demo** (2 min)
   - Run safety test suite
   - Show critical symptom detection

**Total: 15 minutes**

---

## 🐛 Troubleshooting

### Issue: Model not found
```
Solution: Run python scripts/train_model.py
```

### Issue: Database error
```
Solution: Run python scripts/init_database.py
```

### Issue: Port 5000 in use
```
Solution: Edit config.py and change FLASK_PORT
```

### Issue: Import errors
```
Solution: Ensure you're in the project root directory
```

---

## 📈 Performance Tips

### For Faster Inference
- Model is already CPU-optimized
- Uses TF-IDF (no heavy embeddings needed for MVP)
- Gradient Boosting with 200 estimators (good speed/accuracy balance)

### For Larger Datasets
- Replace SQLite with PostgreSQL
- Add Redis for queue management
- Implement background task processing

---

## 🔐 Security Notes

**For MVP Demo:**
- No authentication (add for production)
- Local deployment only
- No PII encryption (add for HIPAA compliance)

**For Production:**
- Add OAuth2/SAML authentication
- Implement role-based access control (RBAC)
- Encrypt PII fields
- Add HTTPS/TLS
- Implement rate limiting
- Add comprehensive logging

---

## 📞 Support

If you encounter issues:

1. Check `logs/triage_system.log` (when logging is enabled)
2. Run health check: http://localhost:5000/health
3. Run safety tests: `python tests/test_safety.py`
4. Verify database: Check if `database/triage_system.db` exists

---

## 🚀 Next Steps (Post-MVP)

### Phase 2 Features
- Voice transcription integration (Whisper)
- Multi-language support
- CAD system integration
- Real-time ambulance tracking
- Advanced analytics

### Production Readiness
- PostgreSQL migration
- Docker containerization
- Kubernetes deployment
- HIPAA compliance audit
- Load testing
- Disaster recovery

---

**Version:** 1.0.0-MVP  
**Last Updated:** February 24, 2026  
**Status:** Demo-Ready ✅
