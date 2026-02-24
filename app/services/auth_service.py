from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def register_user(db: Session, user_data: UserCreate) -> User:
    """Register a new user.

    Raises:
        HTTPException 400: if the username or email is already taken.
    """
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str) -> str:
    """Validate credentials and return a JWT access token.

    Raises:
        HTTPException 401: if credentials are invalid.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, getattr(user, "hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(data={"sub": user.username})


def get_current_user(db: Session, token: str) -> User:
    """Decode a JWT and return the corresponding User.

    Raises:
        HTTPException 401: if the token is invalid or the user no longer exists.
    """
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def password_reset(db: Session, email: str, password: str):
    """Handle password reset requests.

    In a real application, this would generate a reset token and send an email.
    Here we just check if the email exists and return a success message.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email address not found",
        )
    setattr(user, "hashed_password", hash_password(password))
    db.commit()
    return {"message": "Password reset successful"}

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Update user information."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user_data.username:
        setattr(user, "username", user_data.username)
    if user_data.email:
        setattr(user, "email", user_data.email)
    if user_data.password:
        setattr(user, "hashed_password", hash_password(user_data.password))
    db.commit()
    db.refresh(user)
    return user