"""
System Setup Script
One-command setup for the entire Emergency Triage MVP
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def main():
    print_header("EMERGENCY TRIAGE SYSTEM - SETUP")
    
    print("This script will:")
    print("  1. Generate synthetic training data")
    print("  2. Initialize the database")
    print("  3. Train the ML model")
    print("  4. Verify all components")
    print()
    
    input("Press Enter to continue...")
    
    # Step 1: Generate training data
    print_header("Step 1: Generating Training Data")
    try:
        from data.synthetic_training_data import generate_training_data
        import config
        
        training_path = config.DATA_DIR / "training_data.csv"
        generate_training_data(num_samples=1000, output_path=training_path)
        print("✅ Training data generated")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Initialize database
    print_header("Step 2: Initializing Database")
    try:
        from database.models import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.create_tables()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 3: Train model
    print_header("Step 3: Training ML Model")
    try:
        from models.ml_model import TriageClassifier
        classifier = TriageClassifier()
        accuracy = classifier.train(training_path)
        classifier.save()
        print(f"✅ Model trained (accuracy: {accuracy:.3f})")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 4: Verify components
    print_header("Step 4: Verifying Components")
    
    checks = []
    
    # Check database
    import config
    if config.DATABASE_PATH.exists():
        checks.append(("Database", True))
    else:
        checks.append(("Database", False))
    
    # Check model
    if config.MODEL_PATH.exists():
        checks.append(("ML Model", True))
    else:
        checks.append(("ML Model", False))
    
    # Check training data
    if training_path.exists():
        checks.append(("Training Data", True))
    else:
        checks.append(("Training Data", False))
    
    # Print results
    all_passed = True
    for component, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component}")
        if not status:
            all_passed = False
    
    print()
    
    if all_passed:
        print_header("✅ SETUP COMPLETE!")
        print("The Emergency Triage System is ready to use.")
        print()
        print("To start the application, run:")
        print("  python app.py")
        print()
        print("Then access the system at:")
        print(f"  http://localhost:{config.FLASK_PORT}")
        print()
        print("Available interfaces:")
        print("  - Patient Intake:      http://localhost:5000/")
        print("  - Dispatcher Console:  http://localhost:5000/dispatcher")
        print("  - Nurse Queue:         http://localhost:5000/nurse")
        print("  - KPI Dashboard:       http://localhost:5000/dashboard")
        print()
    else:
        print_header("❌ SETUP FAILED")
        print("Some components failed to initialize. Please check the errors above.")

if __name__ == "__main__":
    main()
