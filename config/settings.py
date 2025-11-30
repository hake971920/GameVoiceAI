import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# AI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# Screen Capture Configuration
MONITOR_INDEX = int(os.getenv("MONITOR_INDEX", 1))
CAPTURE_FPS = float(os.getenv("CAPTURE_FPS", 1.0))
SCREENSHOT_DIR = BASE_DIR / "temp" / "screenshots"

# Create necessary directories
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
