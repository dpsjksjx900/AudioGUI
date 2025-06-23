@echo off
REM Automatically update repository from GitHub

REM Ensure current directory is the script's location
cd /d %~dp0

REM Prefer git if available
where git >nul 2>&1
if %errorlevel%==0 (
    echo 🔄 Updating repository via git...
    git pull
    goto :eof
)

REM Fallback to Python download
python update.py
