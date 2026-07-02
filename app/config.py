import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database Connection string
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/monitoring.db"

# Logs
LOG_FILE = BASE_DIR / "logs" / "sync.log"

# Current Service settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Max history records for chart
MAX_HISTORY_POINTS = 1000

# Data store period (days)
DATA_RETENTION_DAYS = 30
