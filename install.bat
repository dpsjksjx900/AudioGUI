@echo off
SETLOCAL

REM Create venv if it doesn't exist
IF NOT EXIST venv (
    echo 🛠  Creating virtual environment…
    python -m venv venv
)

echo ⚡ Activating virtual environment…
call venv\Scripts\activate

echo ⬆️  Upgrading pip…
python -m pip install --upgrade pip

echo 📦 Installing dependencies…
pip install -r requirements.txt

echo ✅ Done!
echo To activate in future sessions, run:
echo    venv\Scripts\activate
ENDLOCAL
