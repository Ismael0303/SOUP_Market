from sqlalchemy.orm import Session
from app.models import Usuario, UserTier
from app.schemas import UserCreate, UserResponse, UserLogin # Import schemas
from app.auth import get_password_hash # Import password hashing utility
import uuid # For UUID generation

# CRUD (Create, Read, Update, Delete) operations for Usuario (User) model

def get_user_by_email(db: Session, email: str) -> Usuario | None:
    """
    Retrieves a user from the database by their email address.
    Args:
        db: The SQLAlchemy database session.
        email: The email address of the user to retrieve.
    Returns:
        The Usuario object if found, otherwise None.
    """
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_user_by_id(db: Session, user_id: uuid.UUID) -> Usuario | None:
    """
    Retrieves a user from the database by their ID.
    Args:
        db: The SQLAlchemy database session.
        user_id: The UUID of the user to retrieve.
    Returns:
        The Usuario object if found, otherwise None.
    """
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> Usuario:
    """
    Creates a new user in the database.
    Args:
        db: The SQLAlchemy database session.
        user: A Pydantic UserCreate schema containing user registration data.
    Returns:
        The newly created Usuario object.
    """
    # Hash the plain password before storing it
    hashed_password = get_password_hash(user.password)
    # Create a new Usuario instance with the hashed password and other data
    db_user = Usuario(
        email=user.email,
        nombre=user.nombre,
        password_hash=hashed_password,
        localizacion=user.localizacion,
        info_contacto=user.info_contacto,
        tipo_tier=user.tipo_tier
    )
    db.add(db_user)  # Add the new user to the session
    db.commit()      # Commit the transaction to save to the database
    db.refresh(db_user) # Refresh the instance to get any auto-generated fields (like ID)
    return db_user

def update_user_profile(db: Session, user_id: uuid.UUID, user_data: dict) -> Usuario | None:
    """
    Updates a user's profile information.
    Args:
        db: The SQLAlchemy database session.
        user_id: The UUID of the user to update.
        user_data: A dictionary containing the fields to update.
    Returns:
        The updated Usuario object if found and updated, otherwise None.
    """
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user:
        for key, value in user_data.items():
            # Special handling for password: hash if provided
            if key == "password" and value:
                db_user.password_hash = get_password_hash(value)
            elif hasattr(db_user, key):
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_user_cv(db: Session, user_id: uuid.UUID, cv_data: dict) -> Usuario | None:
    """
    Updates a freelancer's curriculum vitae.
    Args:
        db: The SQLAlchemy database session.
        user_id: The UUID of the freelancer.
        cv_data: A dictionary containing CV details.
    Returns:
        The updated Usuario object if found and updated, otherwise None.
    """
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user:
        # Ensure the user is a freelancer before updating CV
        if db_user.tipo_tier != UserTier.FREELANCER:
            return None # Or raise an exception, depending on desired behavior

        db_user.curriculum_vitae = cv_data
        db.commit()
        db.refresh(db_user)
        return db_user
    return None
