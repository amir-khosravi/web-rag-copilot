import subprocess
import time
import threading
import sys
from app.common.logger import get_logger

logger = get_logger(__name__)

def run_backend():
    try:
        logger.info("Starting Backend Service (FastAPI)...")
        # specific host 127.0.0.1 and port 8000 to match our config
        subprocess.run(
            ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], 
            check=True
        )
    except Exception as e:
        logger.error(f"Backend failed: {e}")
        sys.exit(1)

def run_frontend():
    try:
        time.sleep(3) # Wait for backend to start
        logger.info("Starting Frontend Service (Streamlit)...")
        subprocess.run(
            ["streamlit", "run", "app/frontend/ui.py"], 
            check=True
        )
    except Exception as e:
        logger.error(f"Frontend failed: {e}")

if __name__ == "__main__":
    # Run backend in a separate thread so they run together
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.start()
    
    run_frontend()