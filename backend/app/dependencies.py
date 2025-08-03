from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import decode_access_token
from app.schemas import TokenData
from app.models import Usuario

# OAuth2PasswordBearer is used for handling token-based authentication
# The "tokenUrl" argument specifies the URL where the client can obtain the token (e.g., login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to provide a database session.
    This function creates a new SQLAlchemy session for each request,
    and ensures it's closed after the request is finished.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to the calling function (FastAPI route)
    finally:
        db.close()  # Ensure the session is closed after use

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """
    Dependency to get the current authenticated user from the JWT token.
    Args:
        token: The JWT token extracted from the Authorization header (Bearer token).
        db: The database session dependency.
    Returns:
        The Usuario object corresponding to the authenticated user.
    Raises:
        HTTPException: If the token is invalid, expired, or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the access token to get the user ID
        token_data: Optional[TokenData] = decode_access_token(token)
        if token_data is None or token_data.user_id is None:
            raise credentials_exception
    except Exception as e: # Catch any exception during token decoding (e.g., JWTError)
        raise credentials_exception from e

    # Query the database to find the user by ID
    user = db.query(Usuario).filter(Usuario.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user
