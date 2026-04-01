"""
Database Initialization Script
Sets up database tables and creates initial structure
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from database.models import DatabaseManager
import config

def main():
    print("=" * 70)
    print("EMERGENCY TRIAGE SYSTEM - DATABASE INITIALIZATION")
    print("=" * 70)
    print()
    
    # Initialize database manager
    print(f"Creating database at: {config.DATABASE_PATH}")
    db_manager = DatabaseManager()
    
    # Create all tables
    db_manager.create_tables()
    
    print()
    print("✅ Database initialized successfully!")
    print()
    print("Tables created:")
    print("  - triage_cases")
    print("  - audit_logs")
    print("  - kpi_metrics")
    print("  - system_health")
    print()
    print("=" * 70)
    print("Database is ready for use!")
    print("=" * 70)

if __name__ == "__main__":
    main()
