"""
FastAPI Authentication Dependencies

Provides dependency injection for FastAPI routes to extract and verify
authenticated users from JWT tokens.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import verify_token


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    FastAPI dependency to extract and verify current user ID from JWT token.
    
    This dependency should be used on all protected routes to ensure the user
    is authenticated and to get their user ID for database queries.
    
    Args:
        credentials: HTTP Bearer credentials (automatically extracted by FastAPI)
    
    Returns:
        User ID as integer
    
    Raises:
        HTTPException: 401 if token is invalid or missing
    
    Example:
        >>> @router.get("/protected")
        >>> async def protected_route(
        >>>     current_user_id: int = Depends(get_current_user_id)
        >>> ):
        >>>     return {"user_id": current_user_id}
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = int(payload.get("sub"))
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    FastAPI dependency to extract user email from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        User email as string
    
    Raises:
        HTTPException: 401 if token is invalid
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        email = payload.get("email")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        return email
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
