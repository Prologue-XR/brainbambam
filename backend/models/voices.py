from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Voice(BaseModel):
    voice_id: UUID
    voice_name: Optional[str] = None
    elevenlabs_id: Optional[str] = None
