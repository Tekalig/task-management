from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
