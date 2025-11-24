"""API routes for BackupWin application"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import time
from app.schemas.backup import (
    SearchRequest, SearchResponse, FileInfo, SearchMultipleDrivesRequest,
    BackupFileRequest, BackupFilesRequest, BackupFolderRequest,
    BackupResponse, RestoreFileRequest, ListBackupsResponse, BackupInfo,
    DrivesResponse, FolderSizeResponse
)
from app.services.file_search import FileSearchService
from app.services.backup import BackupService
from app.core.logger import app_logger

router = APIRouter()

# Initialize services
file_search_service = FileSearchService()
backup_service = BackupService()


# Search Endpoints
@router.get("/drives", response_model=DrivesResponse, tags=["Search"])
async def get_available_drives():
    """Get all available drives on Windows system"""
    try:
        drives = file_search_service.get_available_drives()
        return DrivesResponse(success=True, drives=drives)
    except Exception as e:
        app_logger.error(f"Error getting drives: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_files(request: SearchRequest):
    """Search for files in specified path"""
    try:
        start_time = time.time()
        files = []

        for file_info in file_search_service.search_files(
            search_path=request.search_path,
            file_pattern=request.file_pattern,
            file_extension=request.file_extension,
            recursive=request.recursive,
            max_results=request.max_results,
            case_sensitive=request.case_sensitive
        ):
            files.append(FileInfo(**file_info))

        duration = time.time() - start_time

        return SearchResponse(
            success=True,
            results_count=len(files),
            files=files,
            search_duration_seconds=round(duration, 2)
        )
    except Exception as e:
        app_logger.error(f"Error searching files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/all-drives", response_model=SearchResponse, tags=["Search"])
async def search_in_all_drives(request: SearchMultipleDrivesRequest):
    """Search for files across all available drives"""
    try:
        start_time = time.time()
        files = []

        for file_info in file_search_service.search_in_multiple_drives(
            file_pattern=request.file_pattern,
            file_extension=request.file_extension,
            exclude_drives=request.exclude_drives,
            max_results_per_drive=request.max_results_per_drive
        ):
            files.append(FileInfo(**file_info))

        duration = time.time() - start_time

        return SearchResponse(
            success=True,
            results_count=len(files),
            files=files,
            search_duration_seconds=round(duration, 2)
        )
    except Exception as e:
        app_logger.error(f"Error searching all drives: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/folder-size", response_model=FolderSizeResponse, tags=["Search"])
async def get_folder_size(folder_path: str):
    """Calculate total size of a folder"""
    try:
        result = file_search_service.get_folder_size(folder_path)
        return FolderSizeResponse(
            success=True,
            path=result["path"],
            total_size_mb=result["total_size_mb"],
            total_size_gb=result["total_size_gb"],
            file_count=result["file_count"]
        )
    except Exception as e:
        app_logger.error(f"Error getting folder size: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Backup Endpoints
@router.post("/backup/file", response_model=BackupResponse, tags=["Backup"])
async def backup_file(request: BackupFileRequest):
    """Backup a single file"""
    try:
        result = backup_service.backup_file(
            source_file=request.source_file,
            destination_folder=request.destination_folder,
            preserve_structure=request.preserve_structure,
            create_checksum=request.create_checksum
        )

        if not result["success"]:
            return BackupResponse(success=False, error=result.get("error"))

        return BackupResponse(
            success=True,
            total_files=1,
            successful=1,
            failed=0,
            total_size_mb=result["size_mb"],
            files=[result]
        )
    except Exception as e:
        app_logger.error(f"Error backing up file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup/files", response_model=BackupResponse, tags=["Backup"])
async def backup_files(request: BackupFilesRequest, background_tasks: BackgroundTasks):
    """Backup multiple files"""
    try:
        result = backup_service.backup_files(
            source_files=request.source_files,
            destination_folder=request.destination_folder,
            preserve_structure=request.preserve_structure
        )

        return BackupResponse(**result)
    except Exception as e:
        app_logger.error(f"Error backing up files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup/folder", response_model=BackupResponse, tags=["Backup"])
async def backup_folder(request: BackupFolderRequest):
    """Backup entire folder"""
    try:
        result = backup_service.backup_folder(
            source_folder=request.source_folder,
            destination_folder=request.destination_folder,
            file_extensions=request.file_extensions,
            exclude_patterns=request.exclude_patterns
        )

        if "error" in result:
            return BackupResponse(success=False, error=result["error"])

        return BackupResponse(**result)
    except Exception as e:
        app_logger.error(f"Error backing up folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restore", response_model=BackupResponse, tags=["Backup"])
async def restore_file(request: RestoreFileRequest):
    """Restore a file from backup"""
    try:
        result = backup_service.restore_file(
            backup_file=request.backup_file,
            destination=request.destination,
            verify_checksum=request.verify_checksum
        )

        if not result["success"]:
            return BackupResponse(success=False, error=result.get("error"))

        return BackupResponse(success=True)
    except Exception as e:
        app_logger.error(f"Error restoring file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/backups", response_model=ListBackupsResponse, tags=["Backup"])
async def list_backups(backup_date: str = None):
    """List all available backups"""
    try:
        backups = backup_service.list_backups(backup_date=backup_date)
        return ListBackupsResponse(
            success=True,
            backups=[BackupInfo(**b) for b in backups]
        )
    except Exception as e:
        app_logger.error(f"Error listing backups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/backups", response_model=BackupResponse, tags=["Backup"])
async def delete_backup(backup_path: str):
    """Delete a backup folder"""
    try:
        result = backup_service.delete_backup(backup_path)

        if not result["success"]:
            return BackupResponse(success=False, error=result.get("error"))

        return BackupResponse(success=True)
    except Exception as e:
        app_logger.error(f"Error deleting backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health Check
@router.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BackupWin API",
        "version": "1.0.0"
    }
