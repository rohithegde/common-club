"""
Shared Category Model

Database model for categories shared across club applications.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..database.base import Base


class SharedCategory(Base):
    """
    Shared category model.
    
    Categories can be:
    1. Predefined (user_id=NULL, is_predefined=True) - Available to all users
    2. User-specific (user_id=X, is_predefined=False) - Only for that user
    
    Categories can be scoped to specific apps or available to all apps.
    """
    __tablename__ = "shared_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # income/expense/general
    icon = Column(String, nullable=True)   # Material Design icon name (e.g., 'mdi-cash')
    app_scope = Column(String, nullable=False)  # coin/care/career/campfire/all
    is_predefined = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    parent_id = Column(Integer, ForeignKey('shared_categories.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SharedCategory(id={self.id}, name={self.name}, type={self.type}, app_scope={self.app_scope})>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "icon": self.icon,
            "app_scope": self.app_scope,
            "is_predefined": self.is_predefined,
            "user_id": self.user_id,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class AppSettings(Base):
    """
    App-specific settings model.
    
    Stores user preferences and settings for each club application.
    """
    __tablename__ = "app_settings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    app_name = Column(String, nullable=False)  # coin/care/career/campfire
    key = Column(String, nullable=False)
    value = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<AppSettings(user_id={self.user_id}, app_name={self.app_name}, key={self.key})>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "app_name": self.app_name,
            "key": self.key,
            "value": self.value,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
