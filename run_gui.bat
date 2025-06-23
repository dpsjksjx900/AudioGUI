@echo off
REM 1) bootstrap environment & deps
python install.py

REM 2) launch the GUI using the venv’s Python
IF EXIST venv\Scripts\python.exe (
    call venv\Scripts\python.exe syllable_segmenter_gui.py %*
) ELSE (
    echo ⚠️  Could not find venv\Scripts\python.exe; running system Python
    python syllable_segmenter_gui.py %*
)
