from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from pathlib import Path

from app.database import get_db, engine, Base
from app import crud, schemas
from app.config import LOG_FILE, BASE_DIR

# Logging Settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Init FastAPI app
app = FastAPI(title="Directory Monitoring System", version="1.0.0")

# Statics and Templates settings
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
(static_dir / "css").mkdir(exist_ok=True, parents=True)
(static_dir / "js").mkdir(exist_ok=True, parents=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = BASE_DIR / "app" / "templates"
templates_dir.mkdir(exist_ok=True, parents=True)
templates = Jinja2Templates(directory=str(templates_dir))

# ==================== API ENDPOINTS ====================

@app.post("/api/data")
async def receive_data(data: schemas.MonitoringData, db: Session = Depends(get_db)):
    """Resieve data from Source (S) and Destunation(D) servers"""
    if data.server not in ['S', 'D']:
        raise HTTPException(status_code=400, detail="Invalid server type")

    crud.save_stats(db, data.server, data.timestamp, data.data)
    logger.info(f"Received data from server {data.server}: {len(data.data)} directories")

    # Checking Sync
    if data.server == 'S':
        comparisons = crud.get_latest_comparison(db)
        for comp in comparisons:
            if comp.is_synced and comp.s_size > 0 and comp.d_size > 0:
                crud.log_sync_event(
                    db, comp.base_path,
                    comp.s_size, comp.d_size,
                    comp.s_files, comp.d_files
                )

    return {"status": "success", "message": f"Data from {data.server} saved"}

@app.get("/api/comparison")
async def get_comparison(db: Session = Depends(get_db)):
    """Get current comparison state: all directories"""
    return crud.get_latest_comparison(db)

@app.get("/api/history/{base_path:path}")
async def get_history(base_path: str, limit: int = 100, db: Session = Depends(get_db)):
    """Get specific directory history"""
    return crud.get_history(db, base_path, limit)

@app.get("/api/status")
async def get_status(db: Session = Depends(get_db)):
    """Get Service status"""
    from app.models import DirectoryStats
    count = db.query(DirectoryStats).count()
    last_s = db.query(DirectoryStats).filter(
        DirectoryStats.server == 'S'
    ).order_by(DirectoryStats.timestamp.desc()).first()

    last_d = db.query(DirectoryStats).filter(
        DirectoryStats.server == 'D'
    ).order_by(DirectoryStats.timestamp.desc()).first()

    # Retrieves current Date and Time in ISO format
    current_time = datetime.now().isoformat()

    return {
        "serverDateTime": current_time,
        "status": "running",
        "status_code": 200,

        "total_records": count,
        "last_update_s": last_s.timestamp if last_s else None,
        "last_update_d": last_d.timestamp if last_d else None,

        "debugMessage": "test_20260704_1",
    }

# ==================== WEB INTERFACE ====================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with Table data"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chart/{base_path:path}", response_class=HTMLResponse)
async def chart_page(request: Request, base_path: str):
    """Page with Chart data for a specific Directory"""
    return templates.TemplateResponse(
        "chart.html",
        {"request": request, "base_path": base_path}
    )
