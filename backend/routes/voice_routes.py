from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from models import UserIdentity, Voice
from repository.voice.get_voices import get_voices

voice_router = APIRouter()

@voice_router.get(
    "/voice/voices",
    dependencies=[Depends(AuthBearer())],
    tags=["Voice"],
)
def get_voices_route(
    current_user: UserIdentity = Depends(get_current_user),
) -> list[Voice]:
    """
    Get all voices.
    """
    return get_voices(current_user.id)
