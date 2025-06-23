@echo off
REM Automatically update repository from GitHub

REM Check if git is available
where git >nul 2>&1
IF ERRORLEVEL 1 (
    echo git is not installed or not found in PATH.
    exit /b 1
)

REM Pull latest changes
echo 🔄 Updating repository...
git pull
IF ERRORLEVEL 1 (
    echo Failed to update from GitHub.
    exit /b 1
)

echo Update complete.
