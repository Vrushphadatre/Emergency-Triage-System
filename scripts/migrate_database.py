"""
Database Migration Script
Recreates database with new schema including location fields
"""

import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent))

from database.models import DatabaseManager
from dispatch.dispatch_manager import initialize_sample_ambulances
import config

def migrate_database():
    """Recreate database with updated schema"""
    
    print("=" * 70)
    print("DATABASE MIGRATION - ADDING LOCATION FIELDS")
    print("=" * 70)
    
    # Delete old database if exists
    if config.DATABASE_PATH.exists():
        print(f"\n⚠️  Deleting old database: {config.DATABASE_PATH}")
        try:
            os.remove(config.DATABASE_PATH)
            print("✓ Old database removed")
        except Exception as e:
            print(f"❌ Error removing database: {e}")
            print("Please close the application first and try again.")
            return False
    
    # Create new database with updated schema
    print("\n📦 Creating new database with updated schema...")
    db_manager = DatabaseManager()
    db_manager.create_tables()
    print(f"[OK] Database created at {config.DATABASE_PATH}")
    
    # Initialize sample ambulances
    print("\n🚑 Initializing sample ambulances...")
    session = db_manager.get_session()
    initialize_sample_ambulances(session)
    session.close()
    print("✓ Sample ambulances initialized")
    
    print("\n" + "=" * 70)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 70)
    print("\nNew schema includes:")
    print("  - patient_latitude, patient_longitude")
    print("  - patient_address, patient_city, patient_state")
    print("  - callback_phone, caller_name")
    print("  - Ambulance and DispatchAssignment tables")
    print("\nYou can now restart the application.")
    
    return True


if __name__ == '__main__':
    migrate_database()
