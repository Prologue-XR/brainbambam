CREATE TABLE IF NOT EXISTS voices (
    voice_id UUID PRIMARY KEY,
    voice_name TEXT NOT NULL,
    elevenlabs_id TEXT NOT NULL
);