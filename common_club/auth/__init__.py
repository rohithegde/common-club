"""
Authentication Module

Provides JWT token handling, password hashing, and FastAPI dependencies
for user authentication.
"""

from .jwt_handler import create_access_token, verify_token, get_user_id_from_token
from .password import hash_password, verify_password
from .dependencies import get_current_user_id, get_current_user_email

__all__ = [
    "create_access_token",
    "verify_token",
    "get_user_id_from_token",
    "hash_password",
    "verify_password",
    "get_current_user_id",
    "get_current_user_email",
]
