from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserUpdate
from app.services.auth_service import register_user, authenticate_user, password_reset, update_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2 scheme — the token URL matches the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Dependency that resolves the authenticated user from the JWT token."""
    return get_current_user(db, token)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account.

    - **username**: unique username (max 50 chars)
    - **email**: valid email address
    - **password**: plain-text password (will be hashed server-side)
    """
    return register_user(db, user_data)


@router.post(
    "/login",
    response_model=Token,
    summary="Login and receive a JWT access token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate using *username* and *password* (form data).

    Returns a Bearer token that must be sent in the `Authorization` header
    for all protected endpoints.
    """
    token = authenticate_user(db, form_data.username, form_data.password)
    return Token(access_token=token)

@router.get("/me", response_model=UserResponse, summary="Get current user info")
def read_current_user(current_user: User = Depends(_current_user)):
    """Get details of the currently authenticated user."""
    return current_user

@router.put("/me", response_model=UserResponse, summary="Update current user info")
def update_current_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(_current_user),
):
    """Update details of the currently authenticated user."""
    return update_user(db, current_user.id, user_data)

@router.put("/forgot-password", summary="Request password reset")
def forgot_password(email: str, new_password: str, db: Session = Depends(get_db)):
    """Request a password reset for the given email address."""
    return password_reset(db, email, new_password)