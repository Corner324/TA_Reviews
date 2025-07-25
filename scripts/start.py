#!/usr/bin/env python3
"""Start script for the reviews sentiment service."""

import subprocess
import sys
from pathlib import Path


def main():
    """Start the FastAPI server using uvicorn."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Change to project directory
    import os
    os.chdir(project_root)

    # Start the server
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ]

    print("Starting Reviews Sentiment Service...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("API documentation: http://127.0.0.1:8000/docs")
    print("Press Ctrl+C to stop the server")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
