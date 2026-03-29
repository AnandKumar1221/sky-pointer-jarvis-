@echo off
REM Activate virtual environment
call ".venv\Scripts\activate.bat"

REM Run the Python script
python testcamera.py

REM Keep window open after exit
pause