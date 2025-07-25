#!/bin/bash

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting Reviews Sentiment Service..."
echo "Server will be available at: http://127.0.0.1:8000"
echo "API documentation: http://127.0.0.1:8000/docs"
echo "Press Ctrl+C to stop the server"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload