import sqlite3
import psycopg
import os
import bcrypt
from psycopg.rows import dict_row

from config import DATABASE_URL, SQLITE_DB_PATH

def get_connection():
    if DATABASE_URL:
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)
    else:
        # detect_types allows SQLite to parse TIMESTAMP correctly
        conn = sqlite3.connect(SQLITE_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Read schema
    with open("database/schema.sql", "r") as f:
        schema_sql = f.read()

    # SQLite compatibility for SERIAL and ON CONFLICT
    if not DATABASE_URL:
        schema_sql = schema_sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        schema_sql = schema_sql.replace("ON CONFLICT(key_name) DO NOTHING", "ON CONFLICT(key_name) DO NOTHING")

    try:
        if DATABASE_URL:
            # psycopg executes multiple statements
            cursor.execute(schema_sql)
        else:
            # sqlite3 executes script
            cursor.executescript(schema_sql)
        conn.commit()

        # Check if admin exists
        if DATABASE_URL:
            cursor.execute("SELECT * FROM users WHERE username = %s", ('admin',))
        else:
            cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))

        admin = cursor.fetchone()

        if not admin:
            # Hash password 'unad2026'
            password = b"unad2026"
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt).decode('utf-8')

            if DATABASE_URL:
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, username, email, password_hash, role, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    ('Admin', 'User', 'admin', 'admin@pollamundial.com', hashed, 'admin', 'aprobado')
                )
            else:
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, username, email, password_hash, role, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ('Admin', 'User', 'admin', 'admin@pollamundial.com', hashed, 'admin', 'aprobado')
                )
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
