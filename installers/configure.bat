@echo off
rem Check if python is available
echo "Configuring AeroVector"
where python >nul 2>nul
if %errorlevel%==0 (
    echo "Running Python3 as Python"
    python -m pip install -r requirements.txt
    exit /b 0
)

rem Check if py is available
where py >nul 2>nul
if %errorlevel%==0 (
    echo "Running Python3 as Py"
    py -m pip install -r requirements.txt
    exit /b 0
)

rem No python
echo "Check if python3 is installed, or check if python is in path. To download python visit https://python.org"
pause
exit /b 1
