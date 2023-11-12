from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Response, HTTPException
from models import UserIdentity, Voice
from repository.voice.get_voices import get_voices
from repository.chat.get_chat_history_with_notifications import (
    get_specific_chat_message_with_notification,
    ChatItemType,
)
from elevenlabs import set_api_key, generate
from uuid import UUID

set_api_key("f4ceca83f3f62f63f6274fb9bce3e267")

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


@voice_router.get(
    "/voice/generate/{chat_id}/{message_id}",
    dependencies=[Depends(AuthBearer())],
    tags=["Voice"],
)
async def generate_voice(
    chat_id: UUID,
    message_id: UUID,
    voice="Edu",
    model="eleven_multilingual_v2",
    current_user: UserIdentity = Depends(get_current_user),
) -> Response:
    """
    Generate voice from a specific chat message.
    """
    chat_item = get_specific_chat_message_with_notification(chat_id, message_id)
    if chat_item.item_type != ChatItemType.MESSAGE:
        raise HTTPException(status_code=400, detail="Invalid message type")
    text = chat_item.body.assistant
    audio = generate(text=text, voice=voice, model=model)
    return Response(content=audio, media_type="audio/mp3")
