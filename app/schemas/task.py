from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Schema for task creation requests."""

    title: str
    description: Optional[str] = None
    is_completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for task update requests (all fields are optional)."""

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Schema for task data returned in responses."""

    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
