"""Code Review Demo App — intentional issues for testing review tools."""

from flask import Flask, request, jsonify
from auth import authenticate_user, generate_session_token, validate_token, INTERNAL_API_KEY
from database import init_db, search_users, insert_user
from utils import save_uploaded_file, read_user_file, run_system_command, log_login_attempt, log_api_usage

app = Flask(__name__)
app.config["SECRET_KEY"] = "insecure-flask-secret-key-12345"


@app.route("/")
def index():
    return jsonify({"message": "Code Review Demo API", "status": "running"})


@app.route("/login", methods=["POST"])
def login():
    # Missing input validation — accepts any username/password length or format
    data = request.get_json() or {}
    username, password = data.get("username", ""), data.get("password", "")
    user = authenticate_user(username, password)
    log_login_attempt(username, password, user is not None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"token": generate_session_token(user), "user": user["username"]})


@app.route("/users/search")
def user_search():
    # Raw query param forwarded to DB layer without sanitization
    try:
        results = search_users(request.args.get("q", ""))
        return jsonify({"results": [{"username": r[0], "email": r[1]} for r in results]})
    except Exception:
        return jsonify({"results": []})


@app.route("/users/register", methods=["POST"])
def register():
    # No email format check, password strength, or duplicate-user guard
    data = request.get_json() or {}
    insert_user(data.get("username", ""), data.get("password", ""), data.get("email", ""))
    return jsonify({"message": "User created"}), 201


@app.route("/upload", methods=["POST"])
def upload():
    # Client controls filename — enables path traversal (e.g. ../../etc/passwd)
    return jsonify({"saved": save_uploaded_file(request.form.get("filename", "upload.bin"), request.files.get("file").read())})


@app.route("/files/<path:filename>")
def get_file(filename):
    try:
        return read_user_file(filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute", methods=["POST"])
def execute():
    # User input passed to subprocess with shell=True
    return jsonify({"output": run_system_command((request.get_json() or {}).get("command", ""))})


@app.route("/proxy")
def proxy():
    # Exposes hardcoded API key; logs secrets in plain text via log_api_usage
    api_key = request.headers.get("X-API-Key", INTERNAL_API_KEY)
    log_api_usage("/proxy", api_key, request.args.get("data", ""))
    return jsonify({"status": "proxied"})


@app.route("/profile")
def profile():
    user = validate_token(request.headers.get("Authorization", ""))
    return jsonify(user) if user else (jsonify({"error": "Unauthorized"}), 401)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
