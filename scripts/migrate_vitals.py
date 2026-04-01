"""
Migration script to add vital signs columns to triage_cases table
"""
import sqlite3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config

DATABASE_PATH = config.DATABASE_PATH

def migrate():
    """Add vital signs columns to triage_cases table"""
    conn = sqlite3.connect(str(DATABASE_PATH))
    cursor = conn.cursor()
    
    # List of columns to add
    columns_to_add = [
        ('heart_rate', 'INTEGER'),
        ('blood_pressure', 'VARCHAR(20)'),
        ('respiratory_rate', 'INTEGER'),
        ('spo2', 'INTEGER'),
        ('temperature', 'FLOAT'),
        ('consciousness_level', 'VARCHAR(50)'),
        ('symptom_duration', 'VARCHAR(100)'),
        ('patient_gender', 'VARCHAR(20)'),
    ]
    
    print("Adding vital signs columns to triage_cases table...")
    
    for col_name, col_type in columns_to_add:
        try:
            # Check if column already exists
            cursor.execute(f"PRAGMA table_info(triage_cases)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if col_name not in columns:
                cursor.execute(f"ALTER TABLE triage_cases ADD COLUMN {col_name} {col_type}")
                print(f"  [OK] Added column: {col_name}")
            else:
                print(f"  [SKIP] Column already exists: {col_name}")
        except Exception as e:
            print(f"  [ERROR] Failed to add {col_name}: {str(e)}")
    
    conn.commit()
    conn.close()
    
    print("\n[OK] Migration complete!")

if __name__ == '__main__':
    migrate()
