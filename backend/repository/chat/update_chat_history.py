from typing import List

from fastapi import HTTPException
from models.databases.supabase.chats import CreateChatHistory
from models import ChatHistory, get_supabase_db


def update_chat_history(chat_history: CreateChatHistory) -> ChatHistory:
    supabase_db = get_supabase_db()
    response: List[ChatHistory] = (supabase_db.update_chat_history(chat_history)).data
    if len(response) == 0:
        raise HTTPException(
            status_code=500, detail="An exception occurred while updating chat history."
        )
    else:
        #update chats row with last_update timestamp from response
        chat_response = supabase_db.update_chat(chat_history.chat_id, {"last_update": ChatHistory(response[0]).message_time})
        if len(chat_response.data) == 0:
            raise HTTPException(
                status_code=500, detail="An exception occurred while updating chat history."
            )

    return ChatHistory(response[0])  # pyright: ignore reportPrivateUsage=none
