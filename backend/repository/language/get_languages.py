from uuid import UUID

from models import get_supabase_db
from models.languages import Language


def get_languages(user_id: UUID) -> list[Language]:
    supabase_db = get_supabase_db()
    results = supabase_db.get_languages()  # type: ignore

    return results  # type: ignore
