import os
import subprocess
import sys

VENV_DIR = 'venv'
REQUIREMENTS = 'requirements.txt'

if not os.path.isdir(VENV_DIR):
    print("\U0001F6E0  Creating virtual environment...")
    subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])

# Paths to Python/pip inside the venv
bin_dir = 'Scripts' if os.name == 'nt' else 'bin'
python_exe = os.path.join(VENV_DIR, bin_dir, 'python')
pip_exe = os.path.join(VENV_DIR, bin_dir, 'pip')

print("\u26A1  Upgrading pip...")
subprocess.check_call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])

if os.path.isfile(REQUIREMENTS):
    print("\U0001F4E6  Installing dependencies...")
    subprocess.check_call([python_exe, '-m', 'pip', 'install', '-r', REQUIREMENTS])
else:
    print(f"Warning: {REQUIREMENTS} not found; skipping dependency install")

print("\u2705  Done!")
