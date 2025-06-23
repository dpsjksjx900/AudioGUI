import os
import subprocess
import sys

VENV_DIR = 'venv'
REQUIREMENTS = 'requirements.txt'

if not os.path.isdir(VENV_DIR):
    print("\U0001F6E0  Creating virtual environment...")
    subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])

# Activate pip from venv
pip_exe = os.path.join(VENV_DIR, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
print("\u26A1  Upgrading pip...")
subprocess.check_call([pip_exe, 'install', '--upgrade', 'pip'])

if os.path.isfile(REQUIREMENTS):
    print("\U0001F4E6  Installing dependencies...")
    subprocess.check_call([pip_exe, 'install', '-r', REQUIREMENTS])
else:
    print(f"Warning: {REQUIREMENTS} not found; skipping dependency install")

print("\u2705  Done!")
