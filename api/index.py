import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.join(PARENT_DIR, "backend")

for p in [CURRENT_DIR, PARENT_DIR, BACKEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from backend.app import app
except Exception as e1:
    try:
        from app import app
    except Exception as e2:
        from flask import Flask, jsonify
        app = Flask(__name__)

        @app.route("/api/health")
        def health_err():
            return jsonify({
                "status": "error",
                "error1": str(e1),
                "error2": str(e2),
                "cwd": os.getcwd(),
                "sys_path": sys.path
            }), 500
