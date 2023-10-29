from uuid import UUID

from models import get_supabase_db
from models.voices import Voice


def get_voices(user_id: UUID) -> list[Voice]:
    supabase_db = get_supabase_db()
    results = supabase_db.get_voices()  # type: ignore

    return results  # type: ignore
