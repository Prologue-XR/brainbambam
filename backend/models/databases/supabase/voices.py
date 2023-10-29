from typing import List

from logger import get_logger
from models.databases.repository import Repository
from models.voices import Voice

logger = get_logger(__name__)


class VoiceRepository(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_voices(self) -> List[Voice]:
        response = (
            self.db.from_("voices")
            .select("voice_id, voice_name, elevenlabs_id")
            .execute()
        ).data

        if len(response) == 0:
            return []

        voices_list = [Voice(**voice) for voice in response]
        return voices_list
