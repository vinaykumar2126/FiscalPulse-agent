#!/bin/bash

echo "🚀 Starting FiscalPulse Backend..."
echo ""
echo "⚠️  Make sure the following are running:"
echo "   - PostgreSQL database"
echo "   - Ollama with llama3 model"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

echo ""
echo "🌐 Starting API server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""

# Start the API
uvicorn api:app --reload --host 0.0.0.0 --port 8000
