import os
import sys

# Ensure parent and backend directories are in Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.join(PARENT_DIR, "backend")

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.app import app
