"""Database models for backup operations"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class BackupStatus(str, enum.Enum):
    """Backup status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"


class BackupJob(Base):
    """Model for backup jobs"""
    __tablename__ = "backup_jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_path = Column(Text, nullable=False)
    destination_path = Column(Text, nullable=False)
    status = Column(Enum(BackupStatus), default=BackupStatus.PENDING, nullable=False)
    file_count = Column(Integer, default=0)
    total_size_bytes = Column(BigInteger, default=0)
    successful_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    checksum = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<BackupJob(id={self.id}, name='{self.name}', status='{self.status}')>"


class BackupFile(Base):
    """Model for individual backed up files"""
    __tablename__ = "backup_files"

    id = Column(Integer, primary_key=True, index=True)
    backup_job_id = Column(Integer, nullable=False, index=True)
    source_path = Column(Text, nullable=False)
    destination_path = Column(Text, nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    file_extension = Column(String(50), nullable=True)
    checksum = Column(String(64), nullable=True)
    status = Column(Enum(BackupStatus), default=BackupStatus.PENDING, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    backed_up_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<BackupFile(id={self.id}, file_name='{self.file_name}', status='{self.status}')>"


class SearchHistory(Base):
    """Model for search history"""
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    search_path = Column(Text, nullable=False)
    file_pattern = Column(String(255), nullable=True)
    file_extension = Column(String(50), nullable=True)
    recursive = Column(Boolean, default=True)
    results_count = Column(Integer, default=0)
    search_duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<SearchHistory(id={self.id}, search_path='{self.search_path}', results={self.results_count})>"


class BackupSchedule(Base):
    """Model for scheduled backups"""
    __tablename__ = "backup_schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_path = Column(Text, nullable=False)
    destination_path = Column(Text, nullable=False)
    cron_expression = Column(String(100), nullable=False)  # e.g., "0 0 * * *" for daily at midnight
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<BackupSchedule(id={self.id}, name='{self.name}', is_active={self.is_active})>"
