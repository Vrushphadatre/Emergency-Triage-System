"""
Add missing call_type and dispatch columns to triage_cases table if absent.
Run: python scripts/migrate_add_calltype.py
"""
import sqlite3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
import config

DB_PATH = config.DATABASE_PATH

ALTERS = [
    ("call_type", "TEXT", "'emergency'"),
    ("dispatch_type", "TEXT", "NULL"),
    ("scheduled_dispatch_date", "TEXT", "NULL"),
    ("scheduled_dispatch_time", "TEXT", "NULL"),
]


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run scripts/migrate_database.py to recreate the DB.")
        return 1

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    for col, ctype, default in ALTERS:
        if column_exists(cur, 'triage_cases', col):
            print(f"Column '{col}' already exists — skipping")
            continue
        sql = f"ALTER TABLE triage_cases ADD COLUMN {col} {ctype} DEFAULT {default}"
        print(f"Adding column: {col}")
        try:
            cur.execute(sql)
            conn.commit()
            print(f"Added column '{col}'")
        except Exception as e:
            print(f"Failed to add column '{col}': {e}")
            conn.rollback()
            conn.close()
            return 2

    conn.close()
    print("Migration complete — missing columns added.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
