"""Database access layer for the code-review demo application."""

import sqlite3

# Hardcoded database credentials (intentional vulnerability)
DB_USER = "admin"
DB_PASSWORD = "SuperSecretDbPass123!"
CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@prod-db.internal.example.com:5432/user_portal"

SQLITE_PATH = "demo_users.db"


def get_connection():
    return sqlite3.connect(SQLITE_PATH)


def init_db():
    conn = get_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)")
    conn.commit()
    conn.close()


def find_user_by_username(username):
    """SQL built via f-string — injection risk."""
    conn = get_connection()
    row = conn.execute(f"SELECT id, username, password, email FROM users WHERE username = '{username}'").fetchone()
    conn.close()
    return row


def search_users(search_term):
    """Unsanitized input concatenated into LIKE clause."""
    conn = get_connection()
    results = conn.execute("SELECT username, email FROM users WHERE username LIKE '%" + search_term + "%'").fetchall()
    conn.close()
    return results


def insert_user(username, password, email):
    conn = get_connection()
    conn.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')")
    conn.commit()
    conn.close()
