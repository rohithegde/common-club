"""
Common Club - Shared services for club applications

Provides authentication, database utilities, and common models
for all club apps (coin-club, care-club, career-club, campfire-club).
"""

__version__ = "0.1.0"

from .auth.jwt_handler import create_access_token, verify_token
from .auth.dependencies import get_current_user_id
from .database.connection import get_common_db, get_app_db

__all__ = [
    "create_access_token",
    "verify_token",
    "get_current_user_id",
    "get_common_db",
    "get_app_db",
]
