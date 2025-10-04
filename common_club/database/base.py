"""
SQLAlchemy Base Configuration

Provides base classes and configuration for SQLAlchemy ORM models.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os


# Declarative base for all models
Base = declarative_base()


def get_database_url(db_path: str) -> str:
    """
    Get SQLite database URL from file path.
    
    Args:
        db_path: Path to SQLite database file
    
    Returns:
        SQLAlchemy database URL
    
    Example:
        >>> url = get_database_url("./myapp.db")
        >>> print(url)
        'sqlite:///./myapp.db'
    """
    # Expand user home directory if present
    db_path = os.path.expanduser(db_path)
    
    # Convert to absolute path if relative
    if not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)
    
    return f"sqlite:///{db_path}"


def create_database_engine(db_path: str, **kwargs):
    """
    Create SQLAlchemy engine for SQLite database.
    
    Args:
        db_path: Path to SQLite database file
        **kwargs: Additional engine configuration
    
    Returns:
        SQLAlchemy engine
    """
    database_url = get_database_url(db_path)
    
    # SQLite specific configuration
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        **kwargs
    )
    
    return engine


def create_session_maker(engine):
    """
    Create SQLAlchemy session maker.
    
    Args:
        engine: SQLAlchemy engine
    
    Returns:
        Session maker factory
    """
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_database_session(session_maker) -> Generator:
    """
    Get database session with automatic cleanup.
    
    This is a generator function to be used with FastAPI Depends().
    
    Args:
        session_maker: SQLAlchemy session maker
    
    Yields:
        Database session
    
    Example:
        >>> SessionLocal = create_session_maker(engine)
        >>> def get_db():
        >>>     return get_database_session(SessionLocal)
        >>> 
        >>> @app.get("/items")
        >>> def read_items(db = Depends(get_db)):
        >>>     return db.query(Item).all()
    """
    db = session_maker()
    try:
        yield db
    finally:
        db.close()
