from typing import List

from logger import get_logger
from models.databases.repository import Repository
from models.languages import Language

logger = get_logger(__name__)


class LanguageRepository(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_languages(self) -> List[Language]:
        response = (
            self.db.from_("languages")
            .select("language_id, language_name")
            .execute()
        ).data

        if len(response) == 0:
            return []

        languages_list = [Language(**language) for language in response]
        return languages_list
