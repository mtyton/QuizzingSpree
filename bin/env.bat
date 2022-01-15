@echo off
cd %cd%\..\

set "BASE_DIR=%cd%"

REM environmental variables
CALL bin/vars.bat

CALL venv/Scripts/activate.bat



