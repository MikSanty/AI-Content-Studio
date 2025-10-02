#!/bin/bash
# Quick launch script for AI-Content-Studio (Linux/Mac)

echo "==============================================="
echo "  AI-Content-Studio - Quick Launch"
echo "==============================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo ""
    echo "Running setup wizard..."
    echo ""
    python3 setup_env.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "Setup failed. Please try again."
        exit 1
    fi
    echo ""
fi

# Check if templates directory exists
if [ ! -d "templates" ]; then
    echo "[ERROR] templates/ directory not found!"
    echo "Are you in the correct directory?"
    exit 1
fi

echo "Checking if content brief is ready..."
echo ""

# Run the workflow
python3 main.py

echo ""
echo "==============================================="


