from enum import Enum
from typing import List, Union
from uuid import UUID

from models.notifications import Notification
from pydantic import BaseModel
from utils.parse_message_time import (
    parse_message_time,
)

from repository.chat.get_chat_history import GetChatHistoryOutput, get_chat_history
from repository.notification.get_chat_notifications import (
    get_chat_notifications,
)


class ChatItemType(Enum):
    MESSAGE = "MESSAGE"
    NOTIFICATION = "NOTIFICATION"


class ChatItem(BaseModel):
    item_type: ChatItemType
    body: Union[GetChatHistoryOutput, Notification]


def merge_chat_history_and_notifications(
    chat_history: List[GetChatHistoryOutput], notifications: List[Notification]
) -> List[ChatItem]:
    chat_history_and_notifications = chat_history + notifications

    chat_history_and_notifications.sort(
        key=lambda x: parse_message_time(x.message_time)
        if isinstance(x, GetChatHistoryOutput)
        else parse_message_time(x.datetime)
    )

    transformed_data = []
    for item in chat_history_and_notifications:
        if isinstance(item, GetChatHistoryOutput):
            item_type = ChatItemType.MESSAGE
            body = item
        else:
            item_type = ChatItemType.NOTIFICATION
            body = item
        transformed_item = ChatItem(item_type=item_type, body=body)
        transformed_data.append(transformed_item)

    return transformed_data


def get_chat_history_with_notifications(
    chat_id: UUID,
) -> List[ChatItem]:
    chat_history = get_chat_history(str(chat_id))
    chat_notifications = get_chat_notifications(chat_id)
    return merge_chat_history_and_notifications(chat_history, chat_notifications)


def get_specific_chat_message_with_notification(
    chat_id: UUID, message_id: UUID
) -> ChatItem:
    chat_history = get_chat_history(str(chat_id))
    chat_notifications = get_chat_notifications(chat_id)
    chat_history_and_notifications = merge_chat_history_and_notifications(
        chat_history, chat_notifications
    )
    for item in chat_history_and_notifications:
        if item.item_type == ChatItemType.MESSAGE:
            if item.body.message_id == message_id:
                return item
    return None
