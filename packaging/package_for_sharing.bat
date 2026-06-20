@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python was not found. Please install Python 3.10 or newer from https://www.python.org/downloads/
    pause
    exit /b 1
  )
  set PYTHON_CMD=python
) else (
  set PYTHON_CMD=py -3
)

echo Creating shareable ZIP without local database, caches, or virtual environment...
%PYTHON_CMD% package_for_sharing.py
pause
