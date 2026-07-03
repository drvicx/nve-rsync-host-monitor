from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from app.models import DirectoryStats
from app.schemas import DirData, DirComparison, HistoryPoint
from datetime import datetime, timedelta
from app.config import DATA_RETENTION_DAYS
import logging

logger = logging.getLogger(__name__)

def save_stats(db: Session, server: str, timestamp: datetime, data: list[DirData]):
    """Save servers Directories statistic"""
    for item in data:
        stat = DirectoryStats(
            server=server,
            base_path=item.base_path,
            full_path=item.full_path,
            size_bytes=item.size_bytes,
            files_count=item.files_count,
            timestamp=timestamp
        )
        db.add(stat)
    db.commit()
    cleanup_old_data(db)

def cleanup_old_data(db: Session):
    """Remove data older then specific period"""
    cutoff_date = datetime.utcnow() - timedelta(days=DATA_RETENTION_DAYS)
    db.query(DirectoryStats).filter(
        DirectoryStats.timestamp < cutoff_date
    ).delete()
    db.commit()

def get_latest_comparison(db: Session) -> list[DirComparison]:
    """Get last Comparison for all Directories"""
    # Subqueries for retrieving last records from S и D servers
    subquery_s = db.query(
        DirectoryStats.base_path,
        func.max(DirectoryStats.timestamp).label('max_ts')
    ).filter(DirectoryStats.server == 'S').group_by(DirectoryStats.base_path).subquery()

    subquery_d = db.query(
        DirectoryStats.base_path,
        func.max(DirectoryStats.timestamp).label('max_ts')
    ).filter(DirectoryStats.server == 'D').group_by(DirectoryStats.base_path).subquery()

    # Data from Source (S) and Destination (D) servers
    s_data = db.query(DirectoryStats).join(
        subquery_s,
        and_(
            DirectoryStats.base_path == subquery_s.c.base_path,
            DirectoryStats.timestamp == subquery_s.c.max_ts
        )
    ).all()

    d_data = db.query(DirectoryStats).join(
        subquery_d,
        and_(
            DirectoryStats.base_path == subquery_d.c.base_path,
            DirectoryStats.timestamp == subquery_d.c.max_ts
        )
    ).all()

    # Dictionary for quic access
    s_dict = {item.base_path: item for item in s_data}
    d_dict = {item.base_path: item for item in d_data}
    all_paths = set(s_dict.keys()) | set(d_dict.keys())

    result = []
    for base_path in all_paths:
        s_item = s_dict.get(base_path)
        d_item = d_dict.get(base_path)

        comparison = DirComparison(
            base_path=base_path,
            s_full_path=s_item.full_path if s_item else None,
            d_full_path=d_item.full_path if d_item else None,
            s_size=s_item.size_bytes if s_item else 0,
            d_size=d_item.size_bytes if d_item else 0,
            s_files=s_item.files_count if s_item else 0,
            d_files=d_item.files_count if d_item else 0,
            last_update=max(
                s_item.timestamp if s_item else datetime.min,
                d_item.timestamp if d_item else datetime.min
            ),
            is_synced=(
                s_item.size_bytes == d_item.size_bytes if s_item and d_item else False
            )
        )
        result.append(comparison)

    result.sort(key=lambda x: x.base_path)
    return result

def get_history(db: Session, base_path: str, limit: int = 100) -> list[HistoryPoint]:
    """Get History for specific Directory"""
    s_history = db.query(DirectoryStats).filter(
        DirectoryStats.server == 'S',
        DirectoryStats.base_path == base_path
    ).order_by(desc(DirectoryStats.timestamp)).limit(limit).all()

    d_history = db.query(DirectoryStats).filter(
        DirectoryStats.server == 'D',
        DirectoryStats.base_path == base_path
    ).order_by(desc(DirectoryStats.timestamp)).limit(limit).all()

    s_dict = {item.timestamp: item for item in s_history}
    d_dict = {item.timestamp: item for item in d_history}

    all_timestamps = sorted(set(s_dict.keys()) | set(d_dict.keys()), reverse=True)[:limit]

    result = []
    for ts in all_timestamps:
        s_item = s_dict.get(ts)
        d_item = d_dict.get(ts)

        point = HistoryPoint(
            timestamp=ts,
            s_files=s_item.files_count if s_item else 0,
            d_files=d_item.files_count if d_item else 0,
            s_size=s_item.size_bytes if s_item else 0,
            d_size=d_item.size_bytes if d_item else 0
        )
        result.append(point)

    return result

def log_sync_event(db: Session, base_path: str, s_size: int, d_size: int, s_files: int, d_files: int):
    """Logging Sync Event"""
    logger.info(
        f"SYNC OK: {base_path} | "
        f"S: {s_files} files, {s_size/1024/1024:.2f}MB | "
        f"D: {d_files} files, {d_size/1024/1024:.2f}MB"
    )
