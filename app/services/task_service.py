from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, current_user: User) -> Task:
    """Create a new task owned by *current_user*."""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        owner_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, current_user: User) -> List[Task]:
    """Return all tasks belonging to *current_user*."""
    return db.query(Task).filter(Task.owner_id == current_user.id).all()


def get_task(db: Session, task_id: int, current_user: User) -> Task:
    """Return a single task by ID.

    Raises:
        HTTPException 404: if the task does not exist or does not belong to the user.
    """
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate, current_user: User) -> Task:
    """Update an existing task.

    Only the fields provided in *task_data* are updated (partial update).

    Raises:
        HTTPException 404: if the task does not exist or does not belong to the user.
    """
    task = get_task(db, task_id, current_user)
    update_fields = task_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, current_user: User) -> None:
    """Delete a task.

    Raises:
        HTTPException 404: if the task does not exist or does not belong to the user.
    """
    task = get_task(db, task_id, current_user)
    db.delete(task)
    db.commit()
