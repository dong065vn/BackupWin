"""Pydantic schemas package"""
from app.schemas.backup import (
    SearchRequest,
    SearchMultipleDrivesRequest,
    FileInfo,
    SearchResponse,
    BackupFileRequest,
)

# TODO: Create these schema files when implementing classification feature
# from app.schemas.classification import (
#     FileClassificationCreate,
#     ...
# )

# TODO: Create these schema files when implementing tag feature
# from app.schemas.tag import (
#     FileTagCreate,
#     ...
# )

# TODO: Create these schema files when implementing organization feature
# from app.schemas.organization import (
#     OrganizationActionCreate,
#     ...
# )

__all__ = [
    # Backup schemas
    "SearchRequest",
    "SearchMultipleDrivesRequest",
    "FileInfo",
    "SearchResponse",
    "BackupFileRequest",
]
