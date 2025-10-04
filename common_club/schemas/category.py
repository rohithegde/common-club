"""
Category Schemas

Pydantic schemas for category creation and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(income|expense|general)$")
    icon: Optional[str] = None
    app_scope: str = Field(..., pattern="^(coin|care|career|campfire|all)$")
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, pattern="^(income|expense|general)$")
    icon: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    """Schema for category in responses."""
    id: int
    is_predefined: bool
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for list of categories."""
    predefined: list[CategoryResponse]
    custom: list[CategoryResponse]
