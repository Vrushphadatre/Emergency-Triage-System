"""
ML Triage Classification Model
Binary classifier: Emergency vs Non-Emergency
Conservative thresholds with emergency bias
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
import joblib
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config


class TriageClassifier:
    """
    Emergency Triage ML Classifier
    Predicts emergency vs non-emergency with confidence scoring
    """
    
    def __init__(self):
        self.model = None
        self.text_vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 3),
            stop_words='english'
        )
        self.feature_scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, case_data):
        """
        Extract features from case data
        
        Args:
            case_data: dict or DataFrame with case information
            
        Returns:
            Feature vector for ML model
        """
        if isinstance(case_data, dict):
            df = pd.DataFrame([case_data])
        else:
            df = case_data.copy()
        
        # Ensure all required columns exist with default values
        if 'pain_level' not in df.columns:
            df['pain_level'] = 0
        if 'duration_hours' not in df.columns:
            df['duration_hours'] = 0
        if 'age' not in df.columns:
            df['age'] = 0
        if 'conscious' not in df.columns:
            df['conscious'] = 1  # Default: conscious
        if 'transcript' not in df.columns:
            df['transcript'] = ''
        
        features = []
        
        # Text features from transcript
        text_features = self.text_vectorizer.transform(df['transcript'].fillna(''))
        features.append(text_features.toarray())
        
        # Numerical features (always use all 3 to match training)
        numerical_cols = ['pain_level', 'duration_hours', 'age']
        numerical_array = df[numerical_cols].values
        numerical_scaled = self.feature_scaler.transform(numerical_array)
        features.append(numerical_scaled)
        
        # Categorical features
        conscious_feature = df['conscious'].astype(int).values.reshape(-1, 1)
        features.append(conscious_feature)
        
        # Combine all features
        X = np.hstack(features)
        
        return X
    
    def train(self, training_data_path):
        """
        Train the triage classification model
        
        Args:
            training_data_path: Path to training CSV file
        """
        print("Training Emergency Triage Classifier...")
        
        # Load training data
        df = pd.read_csv(training_data_path)
        
        # Create binary labels (1 = emergency, 0 = non-emergency)
        y = (df['outcome'] == 'emergency').astype(int)
        
        # Fit text vectorizer
        self.text_vectorizer.fit(df['transcript'])
        
        # Fit numerical scaler
        numerical_cols = ['pain_level', 'duration_hours', 'age']
        numerical_data = df[numerical_cols].values
        self.feature_scaler.fit(numerical_data)
        
        # Extract features
        X = self.extract_features(df)
        
        # Base gradient boosting classifier
        base_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            random_state=config.RANDOM_STATE,
            # Emergency bias: increase weight of emergency cases
            # This makes the model more sensitive to emergencies
            subsample=0.8,
            min_samples_split=5,
            min_samples_leaf=2,
        )
        
        # Wrap with calibration to prevent extreme probabilities
        self.model = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)
        
        # Apply class weights to bias toward emergency detection
        sample_weights = np.where(y == 1, 2.0, 1.0)  # 2x weight for emergencies
        
        self.model.fit(X, y, sample_weight=sample_weights)
        
        self.is_trained = True
        
        # Calculate training metrics
        train_accuracy = self.model.score(X, y, sample_weight=sample_weights)
        
        print(f"[OK] Model trained successfully")
        print(f"  - Training accuracy: {train_accuracy:.3f}")
        print(f"  - Feature dimensions: {X.shape[1]}")
        print(f"  - Emergency bias: Applied (2x sample weight)")
        
        return train_accuracy
    
    def predict(self, case_data):
        """
        Predict emergency likelihood for a case
        
        Args:
            case_data: Dict with case information
            
        Returns:
            dict with:
                - risk_score: 0-1 probability of emergency
                - confidence: Model confidence in prediction
                - is_emergency: Boolean recommendation
                - reasoning: Text explanation of key factors
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a saved model.")
        
        # Extract features
        X = self.extract_features(case_data)
        
        # Get probability predictions
        proba = self.model.predict_proba(X)[0]
        risk_score = float(proba[1])  # Probability of emergency class
        
        # Calculate confidence (distance from decision boundary)
        confidence = float(abs(risk_score - 0.5) * 2)  # 0 = uncertain, 1 = very confident
        
        # Check for clinical concerns in transcript
        transcript = case_data.get('transcript', '').lower()
        has_critical_symptoms = any(symptom.lower() in transcript for symptom in config.CRITICAL_SYMPTOMS)
        
        # Apply emergency bias ONLY if low confidence AND there are clinical concerns
        if confidence < config.CONFIDENCE_THRESHOLD:
            if has_critical_symptoms or case_data.get('pain_level', 0) >= 8:
                # Default to emergency when uncertain AND there are clinical concerns
                risk_score = max(risk_score, config.EMERGENCY_THRESHOLD + 0.05)
                confidence_note = "Low confidence + clinical concerns - escalating to emergency (safety first)"
            else:
                # For routine cases with missing data, don't force emergency
                confidence_note = "Low confidence - recommend human review"
        else:
            confidence_note = f"{confidence*100:.0f}% confident in assessment"
        
        # Make recommendation
        is_emergency = risk_score >= config.EMERGENCY_THRESHOLD
        
        # Generate reasoning
        reasoning = self._generate_reasoning(case_data, risk_score, confidence)
        
        result = {
            'risk_score': round(risk_score, 3),
            'confidence': round(confidence, 3),
            'confidence_note': confidence_note,
            'is_emergency': is_emergency,
            'reasoning': reasoning,
            'recommendation': 'EMERGENCY - Dispatch ambulance' if is_emergency 
                            else 'NON-EMERGENCY - Nurse review',
        }
        
        return result
    
    def _generate_reasoning(self, case_data, risk_score, confidence):
        """Generate human-readable reasoning for the prediction"""
        reasons = []
        
        # Check for critical symptoms
        transcript = case_data.get('transcript', '').lower()
        critical_found = []
        for symptom in config.CRITICAL_SYMPTOMS:
            if symptom.lower() in transcript:
                critical_found.append(symptom)
        
        if critical_found:
            reasons.append(f"Critical symptoms detected: {', '.join(critical_found[:3])}")
        
        # Pain level
        pain = case_data.get('pain_level', 0)
        if pain >= 8:
            reasons.append(f"High pain level ({pain}/10)")
        
        # Consciousness
        if not case_data.get('conscious', True):
            reasons.append("Patient unconscious - immediate attention required")
        
        # Age factors
        age = case_data.get('age', 0)
        if age < 2:
            reasons.append("Infant patient - requires careful assessment")
        elif age > 65:
            reasons.append("Elderly patient - heightened risk factors")
        
        # Duration - only flag if explicitly provided and very recent
        # To indicate duration wasn't provided, use -1 or just don't flag for duration=0
        duration = case_data.get('duration_hours', 0)
        # Only note acute onset if duration was explicitly provided and is 0 < duration < 0.5
        # Skip the check if duration is exactly 0 (not provided)
        if duration > 0 and duration < 0.5:
            reasons.append(f"Acute onset - symptoms started {duration*60:.0f} minutes ago")
        
        if not reasons:
            reasons.append("Based on overall symptom patterns and clinical indicators")
        
        reasoning_text = ". ".join(reasons) + "."
        
        return reasoning_text
    
    def save(self, model_path=None, vectorizer_path=None):
        """Save trained model and vectorizer"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_path = model_path or config.MODEL_PATH
        vectorizer_path = vectorizer_path or config.VECTORIZER_PATH
        
        # Save model
        joblib.dump(self.model, model_path)
        
        # Save vectorizer and scaler
        joblib.dump({
            'vectorizer': self.text_vectorizer,
            'scaler': self.feature_scaler,
        }, vectorizer_path)
        
        print(f"[OK] Model saved to {model_path}")
        print(f"[OK] Feature extractors saved to {vectorizer_path}")
    
    def load(self, model_path=None, vectorizer_path=None):
        """Load trained model and vectorizer"""
        model_path = model_path or config.MODEL_PATH
        vectorizer_path = vectorizer_path or config.VECTORIZER_PATH
        
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        self.model = joblib.load(model_path)
        
        feature_data = joblib.load(vectorizer_path)
        self.text_vectorizer = feature_data['vectorizer']
        self.feature_scaler = feature_data['scaler']
        
        self.is_trained = True
        
        print(f"[OK] Model loaded from {model_path}")


if __name__ == "__main__":
    # Training script
    print("=== Emergency Triage Model Training ===\n")
    
    # Check if training data exists
    training_data_path = config.DATA_DIR / "training_data.csv"
    
    if not training_data_path.exists():
        print("Generating synthetic training data...")
        import sys
        sys.path.append(str(config.DATA_DIR))
        from synthetic_training_data import generate_training_data
        generate_training_data(num_samples=1000, output_path=training_data_path)
    
    # Train model
    classifier = TriageClassifier()
    classifier.train(training_data_path)
    
    # Save model
    classifier.save()
    
    print("\n=== Training Complete ===")
