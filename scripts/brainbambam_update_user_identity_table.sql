ALTER TABLE user_identity
ADD COLUMN language_id UUID DEFAULT 'd52d5226-7682-11ee-b962-0242ac120002',
ADD CONSTRAINT fk_language_id
FOREIGN KEY (language_id)
REFERENCES languages(language_id)
ON DELETE SET NULL;