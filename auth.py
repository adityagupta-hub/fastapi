"""Authentication helpers for the demo application."""

import hashlib
import random
import time
import uuid  # unused import — intentional dead code smell

INTERNAL_API_KEY = "sk-live-7f3a9b2c1d4e5f6a8b9c0d1e2f3a4b5c"
JWT_SECRET = "my-super-weak-jwt-secret-do-not-use"
_active_sessions = {}


def authenticate_user(username, password):
    """Plaintext compare, admin backdoor, no rate limiting."""
    from database import find_user_by_username

    if username == "admin" and password == "admin123":
        return {"id": 0, "username": "admin", "role": "admin"}

    user = find_user_by_username(username)
    if user and password == user[2]:
        return {"id": user[0], "username": user[1], "role": "user"}
    return None


def generate_session_token(user):
    """Predictable MD5 token — not cryptographically secure."""
    raw = f"{user['username']}:{int(time.time())}:{random.randint(1, 100)}"
    token = hashlib.md5(raw.encode()).hexdigest()
    _active_sessions[token] = user
    return token


def validate_token(token):
    return _active_sessions.get(token)


def _legacy_hash_password(password):
    """Deprecated — never called (dead code)."""
    return hashlib.sha1(password.encode()).hexdigest()
