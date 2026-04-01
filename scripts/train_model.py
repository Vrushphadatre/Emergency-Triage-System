"""
Model Training Script
Trains the ML triage classification model
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from models.ml_model import TriageClassifier
from data.synthetic_training_data import generate_training_data
import config

def main():
    print("=" * 70)
    print("EMERGENCY TRIAGE SYSTEM - MODEL TRAINING")
    print("=" * 70)
    print()
    
    # Check if training data exists
    training_data_path = config.DATA_DIR / "training_data.csv"
    
    if not training_data_path.exists():
        print("[GENERATE] Generating synthetic training data...")
        generate_training_data(num_samples=1000, output_path=training_data_path)
        print()
    else:
        print(f"[OK] Found existing training data: {training_data_path}")
        print()
    
    # Train model
    print("[TRAIN] Training ML triage classifier...")
    print("        This may take a minute...")
    print()
    
    classifier = TriageClassifier()
    accuracy = classifier.train(training_data_path)
    
    print()
    print(f"[OK] Model trained with accuracy: {accuracy:.3f}")
    print()
    
    # Save model
    print("[SAVE] Saving trained model...")
    classifier.save()
    
    print()
    print("=" * 70)
    print("MODEL TRAINING COMPLETE!")
    print("=" * 70)
    print()
    print(f"Model saved to: {config.MODEL_PATH}")
    print(f"Vectorizer saved to: {config.VECTORIZER_PATH}")
    print()
    print("You can now start the application with: python app.py")

if __name__ == "__main__":
    main()
