"""
Category Model

Database model for categories shared across club applications.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from ..database.base import Base
import enum


class CategoryType(enum.Enum):
    """Category type enumeration."""
    EXPENSE = "expense"
    INCOME = "income"


class Category(Base):
    """
    Category model for shared categories across all club applications.
    
    Categories are shared across all users and applications. They can be:
    1. Predefined (is_predefined=True) - System-wide categories available to all users
    2. Custom (is_predefined=False) - User-created categories (though user_id is removed for true sharing)
    
    Categories support hierarchical structure through parent_id relationships.
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)  # income/expense
    icon = Column(String, nullable=True)   # Material Design icon name (e.g., 'mdi-cash')
    is_predefined = Column(Boolean, default=False, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, type={self.type})>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
            "icon": self.icon,
            "is_predefined": self.is_predefined,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
