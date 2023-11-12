CREATE TABLE IF NOT EXISTS chat_tts (
    message_id UUID,
    chat_id UUID,
    voice_id UUID REFERENCES voices(voice_id),
    mp3_url TEXT NOT NULL,
    PRIMARY KEY (message_id, voice_id),
    FOREIGN KEY (message_id, chat_id) REFERENCES chat_history(message_id, chat_id)
);