#!/bin/bash

# Script to run tests locally (same as CI)

set -e  # Exit on error

echo "🧪 Running tests..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run tests
echo "🚀 Running pytest..."
pytest tests/ -v --tb=short

# Run tests with coverage
echo "📊 Running tests with coverage..."
pytest tests/ --cov=app --cov-report=term-missing

echo "✅ All tests passed!"

