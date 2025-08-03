from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas import TokenData # Import the Pydantic schema for TokenData

# Password hashing context (for bcrypt algorithm)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Hashing Functions ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches a hashed password.
    Args:
        plain_password: The password in plain text.
        hashed_password: The hashed password from the database.
    Returns:
        True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    Args:
        password: The password in plain text.
    Returns:
        The hashed password string.
    """
    return pwd_context.hash(password)

# --- JWT Token Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    Args:
        data: Dictionary containing claims to be encoded in the token (e.g., user_id, email).
        expires_delta: Optional timedelta for token expiration. If None, uses default from settings.
    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use timezone.utc for consistency and to avoid naive datetime warnings
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # Add expiration time to claims
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decodes a JWT access token and returns the payload data.
    Args:
        token: The JWT string to decode.
    Returns:
        TokenData object if decoding is successful and not expired, None otherwise.
    Raises:
        JWTError: If the token is invalid or decoding fails.
    """
    try:
        # Decode the token using the secret key and algorithm from settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Validate the payload against the TokenData schema
        token_data = TokenData(**payload)
        return token_data
    except JWTError:
        # If decoding fails or token is invalid, raise JWTError (handled by FastAPI dependencies)
        return None
