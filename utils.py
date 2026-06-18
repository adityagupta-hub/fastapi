"""Utility functions: file handling, logging, and system helpers."""

import logging
import os
import subprocess

logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(message)s")
logger = logging.getLogger(__name__)

SENDGRID_API_KEY = "SG.xK9mN2pQ4rS6tU8vW0yZ1aB3cD5eF7gH9iJ1kL3mN5oP7qR9sT1uV3wX5yZ7"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
UPLOAD_DIR = "uploads"


def save_uploaded_file(filename, content):
    """No path traversal checks on client-supplied filename."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    return filepath


def read_user_file(filename):
    with open(os.path.join(UPLOAD_DIR, filename), "r") as f:
        return f.read()


def run_system_command(user_input):
    """shell=True with user-controlled input — command injection."""
    result = subprocess.run(f"echo Processing: {user_input}", shell=True, capture_output=True, text=True)
    return result.stdout


def log_login_attempt(username, password, success):
    logger.warning(f"Login {'OK' if success else 'FAIL'} | user={username} | password={password}")


def log_api_usage(endpoint, api_key, payload):
    logger.debug(f"API {endpoint} | key={api_key} | body={payload}")
