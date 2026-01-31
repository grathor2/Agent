"""Main entry point to run the system."""
import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 70)
    print("Starting Collaborative Agent System")
    print("=" * 70)
    print("Server will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    uvicorn.run(
        "ui.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
