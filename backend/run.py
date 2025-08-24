#!/usr/bin/env python3
"""
Simple startup script for the Digital Truth Scan Backend
"""

import uvicorn
import sys
import os

def main():
    """Start the FastAPI server with development configuration."""
    
    # Default configuration
    host = "0.0.0.0"
    port = 8000
    reload = True
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Usage: python run.py [port]")
            sys.exit(1)
    
    print(f"Starting Digital Truth Scan Backend...")
    print(f"Server will be available at: http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    print(f"Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
