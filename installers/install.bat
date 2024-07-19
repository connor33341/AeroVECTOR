@echo off
setlocal

:: Variables - modify these as needed
set "REPO_URL=https://github.com/connor33341/aerovector/archive/refs/heads/master.zip"
set "ZIP_FILE=repo.zip"
set "EXTRACT_DIR=repo"
set "SCRIPT_TO_RUN=aerovector-master\installers\configure.bat"

:: Download the repository
echo "Downloading AeroVector"
curl -L -o "%ZIP_FILE%" "%REPO_URL%"
if %ERRORLEVEL% neq 0 (
    echo Failed to download the repository.
    exit /b 1
)

:: Unzip the repository
echo "Unziping AeroVector"
tar -xf "%ZIP_FILE%"
if %ERRORLEVEL% neq 0 (
    echo Failed to unzip the repository.
    exit /b 1
)

:: Run the batch file located in the repository
echo "Running configure.bat"
call "%SCRIPT_TO_RUN%"
if %ERRORLEVEL% neq 0 (
    echo Failed to run the script.
    exit /b 1
)

:: Clean up
echo "Cleaning up"
del "%ZIP_FILE%"
rd /s /q "%EXTRACT_DIR%"

echo "Done"
endlocal
pause
