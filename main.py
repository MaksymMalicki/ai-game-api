import uvicorn
from api.fastapi_app import app
from terminal import TerminalInterface

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "terminal":
        terminal = TerminalInterface()
        terminal.play()
    elif len(sys.argv) > 1 and sys.argv[1] == "api":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("Usage:")
        print("  python main.py terminal  # Run terminal version")
        print("  python main.py api       # Run FastAPI server")

