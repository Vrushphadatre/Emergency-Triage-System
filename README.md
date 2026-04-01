# Emergency Triage Decision Support System - MVP

## Overview
AI-assisted decision support system for emergency dispatch teams. Helps reduce ambulance overload by intelligently triaging calls while maintaining human oversight for all final decisions.

## Architecture

```
Patient → GenAI Intake → ML Risk Scoring → GenAI Explanation → Human Decision → Logging
```

## Key Features
- ✅ Structured conversational intake (GenAI)
- ✅ ML-based risk assessment (0-1 score + confidence)
- ✅ Plain-language explanations
- ✅ Human-in-the-loop approval (Dispatcher/Nurse)
- ✅ Safety-first guardrails with mandatory escalation
- ✅ Complete audit trail and feedback loop
- ✅ KPI monitoring dashboard

## Tech Stack
- **Python 3.9+**
- **LangChain**: Orchestration & GenAI
- **FAISS**: Vector search for symptom matching
- **Scikit-learn**: ML classification
- **Flask**: Web interface
- **SQLite**: Audit logging
- **Open-source LLM**: Local deployment (CPU-only)

## Installation

### Prerequisites
- Python 3.9 or higher
- No GPU required (CPU-only execution)

### Setup Steps

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Initialize Database**
```bash
python scripts/init_database.py
```

3. **Download LLM Model** (First run only)
```bash
python scripts/download_model.py
```

4. **Run the Application**
```bash
python app.py
```

5. **Access the System**
- Patient Intake Interface: `http://localhost:5000`
- Dispatcher Console: `http://localhost:5000/dispatcher`
- Nurse Queue: `http://localhost:5000/nurse`
- KPI Dashboard: `http://localhost:5000/dashboard`

## Project Structure

```
emergency-triage-mvp/
├── app.py                          # Main Flask application
├── config.py                       # Configuration & thresholds
├── requirements.txt                # Python dependencies
├── data/
│   ├── synthetic_training_data.py  # Generate demo data
│   └── emergency_keywords.json     # High-risk symptom database
├── models/
│   ├── ml_model.py                 # ML triage classifier
│   ├── train_model.py              # Model training script
│   └── saved_models/               # Trained model storage
├── genai/
│   ├── intake_agent.py             # Conversational intake
│   ├── explanation_layer.py        # Risk score explainer
│   └── prompts.py                  # Fixed prompt templates
├── safety/
│   ├── guardrails.py               # Safety rules & escalation
│   └── validation.py               # Input/output validation
├── routing/
│   └── decision_router.py          # Case routing logic
├── database/
│   ├── models.py                   # Database schema
│   └── operations.py               # CRUD operations
├── web/
│   ├── templates/                  # HTML templates
│   └── static/                     # CSS, JS assets
├── scripts/
│   ├── init_database.py            # Database setup
│   └── download_model.py           # LLM download
└── tests/
    └── test_safety.py              # Safety guardrail tests
```

## System Workflow

### 1. Patient Intake
- Patient initiates chat/voice interface
- GenAI conducts structured interview following predefined script
- Extracts: symptoms, duration, severity, patient history

### 2. ML Risk Assessment
- Converts unstructured input to feature vectors
- FAISS vector search matches against high-risk symptom database
- ML classifier outputs:
  - `risk_score`: 0.0 (low) to 1.0 (high)
  - `confidence_level`: Model certainty
  - `is_emergency`: Boolean recommendation

### 3. Safety Checks
**Mandatory Escalation** (Auto-flagged as emergency):
- Chest pain or pressure
- Difficulty breathing / shortness of breath
- Unconscious or unresponsive
- Severe bleeding
- Stroke symptoms

### 4. Human Decision
- **High Risk (≥0.65)** → Dispatcher Queue
- **Low Risk (<0.65)** → Nurse Review Queue
- Human sees: intake summary, risk score, explanation, override option

### 5. Outcome Logging
- All decisions logged with timestamp
- ML prediction vs human outcome recorded
- Audit trail maintained indefinitely

## Safety Guardrails

### Emergency Bias
- When confidence < 70%, default to emergency
- Low-risk threshold set conservatively (0.65)
- Mandatory keywords trigger immediate escalation

### GenAI Boundaries
**Allowed:**
- Ask predefined intake questions
- Extract structured data from responses
- Explain risk scores in plain language
- Generate follow-up scripts

**Prohibited:**
- Medical diagnosis
- Treatment recommendations
- Overriding human decisions
- Free-text medical advice

### Human Override
All automated recommendations can be overridden with:
- Mandatory reason field
- Logged for model improvement
- No penalty for disagreeing with AI

## KPIs Tracked

| Metric | Target | Current |
|--------|--------|---------|
| Non-Emergency Dispatch Reduction | 30% | TBD |
| Emergency Classification Accuracy | >95% | TBD |
| False-Negative Rate (Missed Emergencies) | <2% | **Critical** |
| Average Handling Time | <3 min | TBD |
| Human Override Rate | <10% | TBD |

## Demo Mode

For stakeholder demonstrations, run:
```bash
python app.py --demo
```

This enables:
- Pre-populated sample cases
- Simulated patient conversations
- Real-time KPI updates
- No real data required

## Feedback & Retraining

### Periodic Model Updates
1. Export logged cases: `python scripts/export_feedback.py`
2. Retrain model: `python models/train_model.py --feedback data/feedback.csv`
3. Validate: `python models/validate_model.py`
4. Deploy: `python scripts/deploy_model.py`

### Threshold Adjustment
Modify `config.py`:
```python
EMERGENCY_THRESHOLD = 0.65  # Adjust based on ops feedback
CONFIDENCE_THRESHOLD = 0.70  # Minimum confidence for low-risk
```

## Compliance & Ethics

- **Decision Support Only**: System makes recommendations, not decisions
- **Explainability**: Every risk score includes plain-language reasoning
- **Bias Monitoring**: Track performance across demographics (age, gender)
- **Audit Trail**: Complete log of all interactions and decisions
- **Data Privacy**: Local deployment, no external API calls

## Extending the MVP

### Phase 2 Enhancements
- Voice transcription integration (Whisper)
- Multi-language support
- Integration with CAD (Computer-Aided Dispatch) systems
- Real-time ambulance availability tracking
- Predictive wait time estimation

### Production Readiness
- Replace SQLite with PostgreSQL
- Add authentication & authorization (RBAC)
- Implement Redis caching
- Scale with containerization (Docker)
- Add comprehensive monitoring (Prometheus/Grafana)
- HIPAA compliance audit

## Support & Maintenance

For issues or questions:
1. Check logs: `logs/application.log`
2. Review audit trail: `database/audit_log.db`
3. Validate safety rules: `python tests/test_safety.py`

## License
Proprietary - Healthcare Emergency Services Provider

---

**Last Updated:** February 24, 2026  
**Version:** 1.0.0-MVP  
**Status:** Demo-Ready
