"""
Database Connection Utilities

Provides connection management for common-club.db and app-specific databases.
"""

from typing import Generator
import os
from .base import create_database_engine, create_session_maker, get_database_session


# Global engine and session maker instances
_common_engine = None
_common_session_maker = None
_app_engine = None
_app_session_maker = None


def init_common_db(db_path: str = None):
    """
    Initialize connection to common-club.db database.
    
    Args:
        db_path: Path to common-club.db file.
                 Defaults to ../common-club/common-club.db or from env COMMON_DB_PATH
    """
    global _common_engine, _common_session_maker
    
    if db_path is None:
        db_path = os.getenv("COMMON_DB_PATH", "../common-club/common-club.db")
    
    _common_engine = create_database_engine(db_path)
    _common_session_maker = create_session_maker(_common_engine)
    
    return _common_engine


def init_app_db(db_path: str = None):
    """
    Initialize connection to app-specific database (e.g., coin-club.db).
    
    Args:
        db_path: Path to app database file.
                 Defaults to from env APP_DB_PATH
    """
    global _app_engine, _app_session_maker
    
    if db_path is None:
        db_path = os.getenv("APP_DB_PATH")
        if not db_path:
            raise ValueError(
                "APP_DB_PATH environment variable must be set. "
                "Example: APP_DB_PATH=./coin-club.db"
            )
    
    _app_engine = create_database_engine(db_path)
    _app_session_maker = create_session_maker(_app_engine)
    
    return _app_engine


def get_common_db() -> Generator:
    """
    Get database session for common-club.db.
    
    Use this dependency in FastAPI routes to access shared data
    like users and categories.
    
    Yields:
        Database session for common-club.db
    
    Example:
        >>> from fastapi import Depends
        >>> from common_club.database import get_common_db
        >>> from common_club.models import User
        >>> 
        >>> @router.get("/users")
        >>> async def get_users(db = Depends(get_common_db)):
        >>>     return db.query(User).all()
    """
    global _common_session_maker
    
    if _common_session_maker is None:
        init_common_db()
    
    return get_database_session(_common_session_maker)


def get_app_db() -> Generator:
    """
    Get database session for app-specific database.
    
    Use this dependency in FastAPI routes to access app-specific data
    like transactions, bills, etc.
    
    Yields:
        Database session for app database
    
    Example:
        >>> from fastapi import Depends
        >>> from common_club.database import get_app_db
        >>> 
        >>> @router.get("/transactions")
        >>> async def get_transactions(db = Depends(get_app_db)):
        >>>     return db.query(Transaction).all()
    """
    global _app_session_maker
    
    if _app_session_maker is None:
        init_app_db()
    
    return get_database_session(_app_session_maker)


def get_common_engine():
    """Get the common database engine (for migrations, etc.)."""
    global _common_engine
    if _common_engine is None:
        init_common_db()
    return _common_engine


def get_app_engine():
    """Get the app database engine (for migrations, etc.)."""
    global _app_engine
    if _app_engine is None:
        init_app_db()
    return _app_engine
