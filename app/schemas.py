from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DirData(BaseModel):
    full_path: str
    base_path: str
    size_bytes: int = 0
    files_count: int = 0

class MonitoringData(BaseModel):
    server: str  # 'S' или 'D'
    timestamp: datetime
    data: List[DirData]

class DirComparison(BaseModel):
    base_path: str
    s_full_path: Optional[str] = None
    d_full_path: Optional[str] = None
    s_size: int = 0
    d_size: int = 0
    s_files: int = 0
    d_files: int = 0
    last_update: Optional[datetime] = None
    is_synced: bool = False

class HistoryPoint(BaseModel):
    timestamp: datetime
    s_files: int
    d_files: int
    s_size: int
    d_size: int
