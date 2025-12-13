"""API routes for BackupWin application"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
import time
from app.schemas.backup import *
from app.services.file_search import FileSearchService
from app.services.backup import BackupService
from app.core.logger import app_logger

router = APIRouter()
file_search_service = FileSearchService()
backup_service = BackupService()


@router.get("/drives", response_model=DrivesResponse, tags=["Search"])
async def get_available_drives():
    try:
        return DrivesResponse(success=True, drives=file_search_service.get_available_drives())
    except Exception as e:
        app_logger.error(f"Get drives error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_files(request: SearchRequest):
    try:
        start = time.time()
        files = [FileInfo(**f) for f in file_search_service.search_files(
            request.search_path, request.file_pattern, request.file_extension,
            request.recursive, request.max_results, request.case_sensitive)]
        return SearchResponse(success=True, results_count=len(files), files=files, search_duration_seconds=round(time.time() - start, 2))
    except Exception as e:
        app_logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/all-drives", response_model=SearchResponse, tags=["Search"])
async def search_in_all_drives(request: SearchMultipleDrivesRequest):
    try:
        start = time.time()
        files = [FileInfo(**f) for f in file_search_service.search_in_multiple_drives(
            request.file_pattern, request.file_extension, request.exclude_drives, request.max_results_per_drive)]
        return SearchResponse(success=True, results_count=len(files), files=files, search_duration_seconds=round(time.time() - start, 2))
    except Exception as e:
        app_logger.error(f"Search all drives error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/folder-size", response_model=FolderSizeResponse, tags=["Search"])
async def get_folder_size(folder_path: str):
    try:
        r = file_search_service.get_folder_size(folder_path)
        return FolderSizeResponse(success=True, path=r["path"], total_size_mb=r["total_size_mb"], total_size_gb=r["total_size_gb"], file_count=r["file_count"])
    except Exception as e:
        app_logger.error(f"Folder size error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup/file", response_model=BackupResponse, tags=["Backup"])
async def backup_file(request: BackupFileRequest):
    try:
        r = backup_service.backup_file(request.source_file, request.destination_folder, request.preserve_structure, request.create_checksum)
        return BackupResponse(success=r["success"], total_files=1, successful=1 if r["success"] else 0, failed=0 if r["success"] else 1,
                             total_size_mb=r.get("size_mb", 0), files=[r] if r["success"] else [], error=r.get("error"))
    except Exception as e:
        app_logger.error(f"Backup file error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup/files", response_model=BackupResponse, tags=["Backup"])
async def backup_files(request: BackupFilesRequest, background_tasks: BackgroundTasks):
    try:
        return BackupResponse(**backup_service.backup_files(request.source_files, request.destination_folder, request.preserve_structure))
    except Exception as e:
        app_logger.error(f"Backup files error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup/folder", response_model=BackupResponse, tags=["Backup"])
async def backup_folder(request: BackupFolderRequest):
    try:
        r = backup_service.backup_folder(request.source_folder, request.destination_folder, request.file_extensions, request.exclude_patterns)
        return BackupResponse(**r) if "error" not in r else BackupResponse(success=False, error=r["error"])
    except Exception as e:
        app_logger.error(f"Backup folder error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restore", response_model=BackupResponse, tags=["Backup"])
async def restore_file(request: RestoreFileRequest):
    try:
        r = backup_service.restore_file(request.backup_file, request.destination, request.verify_checksum)
        return BackupResponse(success=r["success"], error=r.get("error"))
    except Exception as e:
        app_logger.error(f"Restore error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/backups", response_model=ListBackupsResponse, tags=["Backup"])
async def list_backups(backup_date: str = None):
    try:
        return ListBackupsResponse(success=True, backups=[BackupInfo(**b) for b in backup_service.list_backups(backup_date)])
    except Exception as e:
        app_logger.error(f"List backups error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/backups", response_model=BackupResponse, tags=["Backup"])
async def delete_backup(backup_path: str):
    try:
        r = backup_service.delete_backup(backup_path)
        return BackupResponse(success=r["success"], error=r.get("error"))
    except Exception as e:
        app_logger.error(f"Delete backup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "BackupWin API", "version": "1.0.0"}
