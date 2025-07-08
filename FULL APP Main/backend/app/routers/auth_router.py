from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # For form-data login

from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UsuarioCreate, Token, UsuarioResponse # Import UsuarioResponse for registration
from app.crud import user as crud_user # Alias to avoid name conflict with 'user' variable
from app.auth import verify_password, create_access_token
from app.core.config import settings

# Create an API router specifically for authentication related endpoints
router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.
    Args:
        user: UserCreate Pydantic model containing user registration data (name, email, password, etc.).
        db: The SQLAlchemy database session dependency.
    Returns:
        The newly created user's data (excluding password hash) as a UserResponse.
    Raises:
        HTTPException 400: If a user with the provided email already exists.
    """
    # Check if a user with the provided email already exists in the database
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        # If user exists, raise a 400 Bad Request exception
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Create the user in the database using the CRUD function
    # The password will be hashed inside crud_user.create_user
    new_user = crud_user.create_user(db=db, user=user)

    # Return the created user's data
    return new_user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user and returns an access token upon successful login.
    Args:
        form_data: OAuth2PasswordRequestForm for username (email) and password.
        db: The SQLAlchemy database session dependency.
    Returns:
        A Token Pydantic model containing the access token and token type.
    Raises:
        HTTPException 401: If authentication fails (invalid credentials).
    """
    # Retrieve the user from the database by their email (username)
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user:
        # If user not found, raise 401 Unauthorized exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the provided password against the hashed password stored in the database
    if not verify_password(form_data.password, user.hashed_password):
        # If passwords do not match, raise 401 Unauthorized exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If authentication is successful, create an access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id), "email": user.email, "tipo_tier": user.tipo_tier.value}, # Include user_id and email in token
        expires_delta=access_token_expires
    )
    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}
