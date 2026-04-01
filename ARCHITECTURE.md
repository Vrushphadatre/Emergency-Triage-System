# Emergency Triage Decision Support System
# System Architecture Documentation

## Executive Summary

This document provides a comprehensive technical overview of the Emergency Triage Decision Support MVP system. The system is designed to assist emergency dispatch teams in making informed decisions about ambulance deployment while maintaining strict human oversight and safety-first principles.

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PATIENT LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Web Interface (Chat/Voice Input)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GENAI LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Intake Agent (LangChain)                                 │  │
│  │  • Structured questioning                                 │  │
│  │  • Natural language processing                            │  │
│  │  • Data extraction                                        │  │
│  └────────────────┬─────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SAFETY GUARDRAILS LAYER                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Critical symptom detection                             │  │
│  │  • Mandatory escalation rules                             │  │
│  │  • Input/output validation                                │  │
│  └────────────────┬─────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ML PREDICTION LAYER                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Triage Classifier (Gradient Boosting)                    │  │
│  │  • Risk score (0-1)                                       │  │
│  │  • Confidence level                                       │  │
│  │  • Feature extraction (TF-IDF + numerical)                │  │
│  └────────────────┬─────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXPLANATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  GenAI Risk Explainer                                     │  │
│  │  • Plain-language explanations                            │  │
│  │  • Key factor identification                              │  │
│  │  • Reasoning transparency                                 │  │
│  └────────────────┬─────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ROUTING LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Decision Router                                          │  │
│  │  • Emergency → Dispatcher Queue                           │  │
│  │  • Non-Emergency → Nurse Queue                            │  │
│  └────────────────┬─────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   HUMAN-IN-THE-LOOP LAYER                        │
│  ┌──────────────────────┐     ┌──────────────────────────────┐ │
│  │  Dispatcher Console  │     │      Nurse Queue              │ │
│  │  • Emergency cases   │     │  • Non-emergency cases        │ │
│  │  • Final decision    │     │  • Callback/referral          │ │
│  └──────────┬───────────┘     └────────────┬─────────────────┘ │
└─────────────┼──────────────────────────────┼────────────────────┘
              │                              │
              └──────────┬───────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUDIT & FEEDBACK LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Database logging (SQLite/PostgreSQL)                   │  │
│  │  • KPI tracking                                           │  │
│  │  • Outcome vs. prediction comparison                      │  │
│  │  • Model retraining pipeline                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Details

### 2.1 GenAI Intake Agent

**Technology:** Pure Python with pattern matching (LangChain-ready for LLM integration)

**Purpose:** Conduct structured patient intake following a predefined script

**Key Features:**
- Fixed question sequence (no deviation)
- Natural language understanding for data extraction
- Safety-first approach with immediate escalation on critical symptoms

**Prohibited Actions:**
- Medical diagnosis
- Treatment recommendations
- Free-form conversation outside script

**Input:** Unstructured patient responses  
**Output:** Structured JSON with:
```json
{
  "chief_complaint": "chest pain",
  "symptom_duration": 0.5,
  "pain_level": 9,
  "conscious_status": true,
  "patient_age": 58,
  "medical_history": "diabetes, hypertension",
  "transcript": "Full conversation text"
}
```

---

### 2.2 ML Triage Classifier

**Algorithm:** Gradient Boosting (scikit-learn)

**Feature Engineering:**
- **Text Features:** TF-IDF vectorization of symptom transcripts (500 features, 1-3 ngrams)
- **Numerical Features:** Pain level, duration, age (scaled)
- **Categorical Features:** Consciousness status

**Training:**
- Emergency bias through 2x sample weighting for emergency cases
- 200 estimators, max depth 4 (prevents overfitting)
- Cross-validation with 5 folds

**Output:**
```json
{
  "risk_score": 0.92,
  "confidence": 0.85,
  "is_emergency": true,
  "reasoning": "Critical symptoms detected: chest pain, shortness of breath"
}
```

**Performance Targets:**
- Accuracy: >95%
- False-negative rate: <2% (critical)
- Emergency bias when confidence < 70%

---

### 2.3 Safety Guardrails

**Layer 1: Input Validation**
- Sanitize user input (XSS prevention)
- Length limits
- Character filtering

**Layer 2: Critical Symptom Detection**

Mandatory escalation triggers:
```python
CRITICAL_SYMPTOMS = [
    "chest pain", "chest pressure",
    "difficulty breathing", "shortness of breath",
    "unconscious", "unresponsive",
    "severe bleeding",
    "stroke symptoms", "slurred speech",
    "seizure", "convulsion",
]
```

**Layer 3: Override Logic**
- Unconscious patient → automatic emergency (risk_score = 1.0)
- Pain level ≥ 9 → escalate (risk_score ≥ 0.90)
- Low confidence (< 70%) + moderate risk → emergency
- Infant (< 1 year) + any risk → escalate

**Layer 4: Output Validation**
- Block medical diagnosis language
- Block treatment recommendations
- Ensure structured JSON output

---

### 2.4 Decision Routing

**Emergency Routing (risk_score ≥ 0.65):**
- Queue: Dispatcher
- Priority: HIGH or CRITICAL
- SLA: 2 minutes
- Action: Ambulance dispatch decision

**Non-Emergency Routing (risk_score < 0.65):**
- Queue: Nurse
- Priority: MEDIUM, LOW, or ROUTINE
- SLA: 15 minutes
- Action: Callback, self-care, or clinic referral

**Priority Levels:**
- CRITICAL: risk_score ≥ 0.90 or safety override
- HIGH: 0.65 ≤ risk_score < 0.90
- MEDIUM: 0.50 ≤ risk_score < 0.65
- LOW: 0.30 ≤ risk_score < 0.50
- ROUTINE: risk_score < 0.30

---

### 2.5 Human-in-the-Loop Interface

**Dispatcher Console:**
- Real-time queue display (auto-refresh: 10s)
- Risk score visualization
- Full case details
- Actions: Dispatch ambulance, Refer to nurse
- Override capability with mandatory reason

**Nurse Queue:**
- Case review interface
- Actions: Callback, Self-care advice, Clinic referral, Escalate to emergency
- Clinical notes entry

**Shared Features:**
- Manual override always available
- Complete conversation history visible
- ML reasoning displayed
- Audit trail for all actions

---

### 2.6 Database Schema

**Tables:**

1. **triage_cases** (Main record)
   - Case identification
   - Patient data (anonymized in production)
   - ML prediction
   - Human decision
   - Final disposition
   - Outcome verification

2. **audit_logs** (Complete audit trail)
   - Action type
   - Actor (system/user)
   - Timestamp
   - Before/after state

3. **kpi_metrics** (Daily aggregates)
   - Volume metrics
   - Accuracy metrics
   - Performance metrics
   - Safety metrics

4. **system_health** (Monitoring)
   - Status
   - Performance
   - Error tracking

---

## 3. Data Flow

### 3.1 Patient Intake Flow

```
1. Patient initiates contact
   ↓
2. GenAI Intake Agent asks structured questions
   ↓
3. Extract structured data from responses
   ↓
4. Check for critical symptoms (safety layer)
   ↓
5. If critical → immediate emergency escalation
   ↓
6. Otherwise → continue to ML prediction
```

### 3.2 ML Prediction Flow

```
1. Receive structured case data
   ↓
2. Extract features:
   - Vectorize transcript (TF-IDF)
   - Scale numerical features
   - Encode categorical features
   ↓
3. Generate prediction:
   - Risk score (0-1)
   - Confidence level
   ↓
4. Apply safety guardrails:
   - Check critical symptoms
   - Apply emergency bias if needed
   - Override if safety rules triggered
   ↓
5. Generate plain-language explanation
   ↓
6. Route to appropriate queue
```

### 3.3 Human Decision Flow

```
1. Case appears in queue (dispatcher or nurse)
   ↓
2. Human reviews:
   - Patient information
   - ML risk assessment
   - Explanation
   ↓
3. Human makes final decision:
   - Can override AI recommendation
   - Must provide reason for override
   ↓
4. Action executed:
   - Ambulance dispatched
   - Nurse callback scheduled
   - Self-care advice provided
   - Referral made
   ↓
5. Outcome logged to database
   ↓
6. Feedback used for model retraining
```

---

## 4. Safety & Compliance

### 4.1 Safety Mechanisms

**Emergency Bias:**
- Default to emergency when uncertain
- Conservative thresholds
- Multiple safety checkpoints

**Mandatory Escalation:**
- Hardcoded rules for critical symptoms
- Cannot be overridden by ML model
- Human can still make final decision

**Human Oversight:**
- No autonomous decisions
- All AI outputs are recommendations only
- Manual override always available

### 4.2 Audit Trail

Every action generates an audit log entry:
- Who (user ID or system)
- What (action type)
- When (timestamp)
- Why (reasoning/notes)
- Before/after state

Retention: 7 years (configurable for compliance)

### 4.3 Explainability

Every risk score includes:
- Plain-language explanation
- Key contributing factors
- Confidence level
- Safety overrides (if any)

No "black box" predictions.

---

## 5. Performance & Scalability

### 5.1 MVP Performance

**Hardware Requirements:**
- CPU only (no GPU needed)
- 4GB RAM minimum
- Standard web server

**Response Times:**
- Intake question: < 100ms
- ML prediction: < 500ms
- End-to-end: < 3 minutes (target)

### 5.2 Scalability Considerations

**Current Limitations (MVP):**
- Single-server deployment
- SQLite database (good for ~100K cases)
- In-memory queue management

**Production Scaling:**
- Horizontal scaling with load balancer
- PostgreSQL for larger datasets
- Redis for queue management
- Docker/Kubernetes deployment
- Microservices architecture

---

## 6. Model Training & Retraining

### 6.1 Initial Training

**Data:**
- Synthetic training data (1000 samples)
- 60% non-emergency, 30% emergency, 10% borderline

**Features:**
- Symptom keywords
- Pain levels
- Duration patterns
- Age factors
- Medical history

### 6.2 Feedback Loop

**Continuous Improvement:**
```
Human Decision → Outcome Log → Compare to ML Prediction
                                        ↓
                              Identify Discrepancies
                                        ↓
                              Accumulate Feedback Data
                                        ↓
                              Retrain Model (Monthly)
                                        ↓
                              Validate New Model
                                        ↓
                              Deploy if Improved
```

**Retraining Triggers:**
- Minimum 100 new cases with ground truth
- Monthly schedule
- After significant system changes

**Validation:**
- Must exceed 90% accuracy
- False-negative rate must be < 2%
- Human review before deployment

---

## 7. KPIs & Monitoring

### 7.1 Critical KPIs

| KPI | Target | Alerting |
|-----|--------|----------|
| False-Negative Rate | < 2% | Alert if > 3% |
| Emergency Accuracy | > 95% | Alert if < 90% |
| Non-Emergency Reduction | 30% | Monthly review |
| Avg Handling Time | < 3 min | Alert if > 5 min |
| Human Override Rate | < 10% | Review if > 15% |

### 7.2 System Health Monitoring

- Response time tracking
- Error rate monitoring
- Queue length alerts
- Database performance
- Model inference latency

---

## 8. Technology Stack

### 8.1 Core Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python 3.9+ Flask | Web framework |
| ML | scikit-learn | Classification model |
| Vector Search | FAISS (CPU) | Symptom matching |
| Orchestration | LangChain | GenAI workflow |
| LLM | Mistral-7B (GGUF) | Local inference |
| Database | SQLite → PostgreSQL | Data storage |
| Frontend | HTML/CSS/JS | User interface |

### 8.2 Key Dependencies

```
Flask==3.0.0
scikit-learn==1.4.0
faiss-cpu==1.7.4
langchain==0.1.6
numpy==1.26.3
pandas==2.2.0
SQLAlchemy==2.0.25
```

**All CPU-only, no paid APIs**

---

## 9. Deployment

### 9.1 MVP Deployment (Single Server)

```bash
# Clone repository
git clone <repo-url>
cd emergency-triage-mvp

# Install dependencies
pip install -r requirements.txt

# Run setup
python scripts/setup_system.py

# Start application
python app.py
```

### 9.2 Production Deployment (Recommended)

**Infrastructure:**
- Load balancer (NGINX)
- Application servers (3+)
- Database server (PostgreSQL with replication)
- Redis cluster (queue management)
- Monitoring (Prometheus/Grafana)

**Security:**
- HTTPS/TLS
- OAuth2 authentication
- RBAC (Role-Based Access Control)
- PII encryption
- HIPAA compliance measures

---

## 10. Future Enhancements

### Phase 2 Features

1. **Voice Integration**
   - Real-time transcription (Whisper)
   - Voice-to-text intake

2. **Multi-Language Support**
   - Translation layer
   - Multi-lingual models

3. **CAD Integration**
   - Real-time ambulance tracking
   - Automatic dispatch API

4. **Advanced Analytics**
   - Predictive wait times
   - Resource optimization
   - Geographic analysis

5. **Mobile Application**
   - Native iOS/Android apps
   - Push notifications

### Production Hardening

- Comprehensive test suite (unit + integration)
- Load testing (>1000 concurrent users)
- Disaster recovery plan
- Data backup automation
- Security audit & penetration testing
- HIPAA compliance certification

---

**Document Version:** 1.0  
**Last Updated:** February 24, 2026  
**Authors:** Senior GenAI + ML Engineering Team
