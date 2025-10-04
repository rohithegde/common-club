"""
JWT Token Handler

Handles creation and verification of JWT tokens for user authentication.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os


# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_access_token(user_id: int, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: User's database ID
        email: User's email address
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    
    Example:
        >>> token = create_access_token(user_id=1, email="user@example.com")
        >>> print(token)
        'eyJ0eXAiOiJKV1QiLC...'
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload containing user_id and email
    
    Raises:
        ValueError: If token is invalid or expired
    
    Example:
        >>> payload = verify_token(token)
        >>> print(payload)
        {'sub': '1', 'email': 'user@example.com', 'exp': 1234567890}
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise ValueError("Invalid token: missing user ID")
        
        return payload
        
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def get_user_id_from_token(token: str) -> int:
    """
    Extract user ID from token.
    
    Args:
        token: JWT token string
    
    Returns:
        User ID as integer
    
    Raises:
        ValueError: If token is invalid
    """
    payload = verify_token(token)
    return int(payload.get("sub"))
