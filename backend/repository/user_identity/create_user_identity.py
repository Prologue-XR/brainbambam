from typing import Optional
from uuid import UUID

from models import UserIdentity, get_supabase_client


def create_user_identity(
    id: UUID, openai_api_key: Optional[str], language_id: Optional[UUID] = None
) -> UserIdentity:
    supabase_client = get_supabase_client()

    user_identity_data = {
        "user_id": str(id),
        "openai_api_key": openai_api_key,
    }
    if language_id is not None:
        user_identity_data["language_id"] = str(language_id)

    response = (
        supabase_client.from_("user_identity").insert(user_identity_data).execute()
    )
    user_identity = response.data[0]
    return UserIdentity(
        id=user_identity.get("user_id"), openai_api_key=user_identity.get("openai_api_key"), language_id=user_identity.get("language_id")  # type: ignore
    )
