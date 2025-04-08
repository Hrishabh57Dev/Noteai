import os
import sys
import subprocess
from dotenv import load_dotenv

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """
    Ensure all dependencies are installed.
    """
    try:
        subprocess.check_call(["python3", "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        exit(1)

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Check and install dependencies
    check_dependencies()

    # Ensure necessary directories exist
    os.system("python3 backend/setup_directories.py")

    # Get the port from environment variables or default to 5000
    port = os.getenv("PORT", 5000)

    # Start the Flask app
    os.system(f"flask --app backend/app.py run --host=0.0.0.0 --port={port}")
