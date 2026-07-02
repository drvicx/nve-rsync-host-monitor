from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Index
from app.database import Base
from datetime import datetime

class DirectoryStats(Base):
    __tablename__ = "directory_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    server = Column(String(1), nullable=False)  # 'S' или 'D'
    base_path = Column(String(500), nullable=False)
    full_path = Column(String(500), nullable=False)
    size_bytes = Column(BigInteger, nullable=False, default=0)
    files_count = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_server_basepath', 'server', 'base_path'),
        Index('idx_timestamp', 'timestamp'),
    )
