from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Language(BaseModel):
    language_id: UUID
    language_name: Optional[str] = None
