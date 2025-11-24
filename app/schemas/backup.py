"""Pydantic schemas for backup operations"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Search Schemas
class SearchRequest(BaseModel):
    """Schema for file search request"""
    search_path: str = Field(..., description="Path to search (drive or folder)")
    file_pattern: Optional[str] = Field(default="*", description="File pattern with wildcards")
    file_extension: Optional[str] = Field(default=None, description="File extension filter (e.g., '.txt')")
    recursive: bool = Field(default=True, description="Search in subdirectories")
    max_results: Optional[int] = Field(default=None, description="Maximum results to return")
    case_sensitive: bool = Field(default=False, description="Case sensitive search")


class SearchMultipleDrivesRequest(BaseModel):
    """Schema for searching multiple drives"""
    file_pattern: Optional[str] = Field(default="*", description="File pattern with wildcards")
    file_extension: Optional[str] = Field(default=None, description="File extension filter")
    exclude_drives: Optional[List[str]] = Field(default=None, description="Drives to exclude")
    max_results_per_drive: Optional[int] = Field(default=100, description="Max results per drive")


class FileInfo(BaseModel):
    """Schema for file information"""
    path: str
    name: str
    size: int
    size_mb: float
    created: str
    modified: str
    extension: str
    drive: Optional[str] = None


class SearchResponse(BaseModel):
    """Schema for search response"""
    success: bool
    results_count: int
    files: List[FileInfo]
    search_duration_seconds: Optional[float] = None


# Backup Schemas
class BackupFileRequest(BaseModel):
    """Schema for single file backup request"""
    source_file: str = Field(..., description="Path to source file")
    destination_folder: Optional[str] = Field(default=None, description="Custom destination folder")
    preserve_structure: bool = Field(default=True, description="Preserve folder structure")
    create_checksum: bool = Field(default=True, description="Create checksum for verification")


class BackupFilesRequest(BaseModel):
    """Schema for multiple files backup request"""
    source_files: List[str] = Field(..., description="List of source file paths")
    destination_folder: Optional[str] = Field(default=None, description="Custom destination folder")
    preserve_structure: bool = Field(default=True, description="Preserve folder structure")


class BackupFolderRequest(BaseModel):
    """Schema for folder backup request"""
    source_folder: str = Field(..., description="Path to source folder")
    destination_folder: Optional[str] = Field(default=None, description="Custom destination folder")
    file_extensions: Optional[List[str]] = Field(default=None, description="Only backup these extensions")
    exclude_patterns: Optional[List[str]] = Field(default=None, description="Patterns to exclude")


class BackupFileResult(BaseModel):
    """Schema for backup file result"""
    success: bool
    source: str
    destination: Optional[str] = None
    size_mb: Optional[float] = None
    checksum: Optional[str] = None
    backed_up_at: Optional[str] = None
    error: Optional[str] = None


class BackupResponse(BaseModel):
    """Schema for backup operation response"""
    success: bool = True
    total_files: Optional[int] = None
    successful: Optional[int] = None
    failed: Optional[int] = None
    total_size_mb: Optional[float] = None
    files: Optional[List[BackupFileResult]] = None
    errors: Optional[List[BackupFileResult]] = None
    error: Optional[str] = None


class RestoreFileRequest(BaseModel):
    """Schema for file restoration request"""
    backup_file: str = Field(..., description="Path to backup file")
    destination: str = Field(..., description="Destination path for restoration")
    verify_checksum: bool = Field(default=True, description="Verify file integrity")


class BackupInfo(BaseModel):
    """Schema for backup information"""
    path: str
    name: str
    file_count: int
    size_mb: float
    created: str


class ListBackupsResponse(BaseModel):
    """Schema for list backups response"""
    success: bool
    backups: List[BackupInfo]


# Drive Information Schemas
class DriveInfo(BaseModel):
    """Schema for drive information"""
    drive: str
    available: bool


class DrivesResponse(BaseModel):
    """Schema for available drives response"""
    success: bool
    drives: List[str]


class FolderSizeResponse(BaseModel):
    """Schema for folder size response"""
    success: bool
    path: str
    total_size_mb: float
    total_size_gb: float
    file_count: int
