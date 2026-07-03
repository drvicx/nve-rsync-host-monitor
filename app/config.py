import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database Connection string
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/monitor.db"

# Logs
LOG_FILE = BASE_DIR / "logs" / "sync.log"

# Current Service settings (prod)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8010))

# Max history records for chart
MAX_HISTORY_POINTS = 1000

# Data store period (days)
DATA_RETENTION_DAYS = 30
