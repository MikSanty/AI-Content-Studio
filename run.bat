@echo off
REM Quick launch script for AI-Content-Studio (Windows)

echo ===============================================
echo   AI-Content-Studio - Quick Launch
echo ===============================================
echo.

REM Activate conda env313 environment
echo Activating Anaconda environment...
call conda activate env313
if errorlevel 1 (
    echo [ERROR] Could not activate conda environment.
    echo Please run: conda activate env313
    echo Then try again.
    pause
    exit /b 1
)
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo.
    echo Running setup wizard...
    echo.
    python setup_env.py
    if errorlevel 1 (
        echo.
        echo Setup failed. Please try again.
        pause
        exit /b 1
    )
    echo.
)

REM Check if templates/manual.md has content
echo Checking if content brief is ready...
echo.

REM Run the workflow
python main.py

echo.
echo ===============================================
pause


