ALTER TABLE prompts
ADD COLUMN IF NOT EXISTS initial_message TEXT DEFAULT 'How can I help you today?',
ADD COLUMN IF NOT EXISTS question_suggestions JSONB DEFAULT '["Tell me about BrainBamBam", "What is BrainBamBam?"]';