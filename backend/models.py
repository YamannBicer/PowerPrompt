# backend/models.py

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ImageEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_path: str
    prompt: str
    model_type: str
    style_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
