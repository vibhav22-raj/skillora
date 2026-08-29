"""Helper to run the backend uvicorn server from the backend/ folder.

This script ensures the repository root is on sys.path so `import backend` works
when running from the backend folder (common when using a local virtualenv).

Usage (from backend/):
  python run_uvicorn.py

Or without the script, in PowerShell you can do:
  $env:PYTHONPATH = (Get-Item ..).FullName; uvicorn app.main:app

The script below starts uvicorn programmatically.
"""
import os
import sys

# Ensure project root (parent of backend/) is on sys.path so `import backend` works
HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from uvicorn import run

if __name__ == '__main__':
    # Use same module path the project expects
    run('app.main:app', host='127.0.0.1', port=8000, reload=True)
