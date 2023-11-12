from enum import Enum
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel


class PromptStatusEnum(str, Enum):
    private = "private"
    public = "public"


class Prompt(BaseModel):
    title: str
    content: str
    status: PromptStatusEnum = PromptStatusEnum.private
    id: UUID
    initial_message: Optional[str] = "How can I help you today?"
    question_suggestions: Optional[List[str]] = [
        "Tell me about BrainBamBam",
        "What is BrainBamBam?",
    ]
