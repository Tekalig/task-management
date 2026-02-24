from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.auth_service import get_current_user
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# OAuth2 scheme — the token URL matches the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Dependency that resolves the authenticated user from the JWT token."""
    return get_current_user(db, token)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List all tasks for the current user",
)
def list_tasks(current_user: User = Depends(_current_user), db: Session = Depends(get_db)):
    """Return every task owned by the authenticated user."""
    return get_tasks(db, current_user)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create(
    task_data: TaskCreate,
    current_user: User = Depends(_current_user),
    db: Session = Depends(get_db),
):
    """Create a task for the authenticated user."""
    return create_task(db, task_data, current_user)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
)
def read_task(
    task_id: int,
    current_user: User = Depends(_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a specific task by its ID (must belong to the current user)."""
    return get_task(db, task_id, current_user)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(_current_user),
    db: Session = Depends(get_db),
):
    """Partially update a task (only provided fields are changed)."""
    return update_task(db, task_id, task_data, current_user)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete(
    task_id: int,
    current_user: User = Depends(_current_user),
    db: Session = Depends(get_db),
):
    """Permanently delete a task owned by the current user."""
    delete_task(db, task_id, current_user)
