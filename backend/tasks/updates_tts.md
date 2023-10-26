1. Database Scripts:
- create voices table sql: A script to create a new table in Supabase for storing voice IDs from ElevenLabs.
- create languages table sql: A script to create a new table in Supabase for storing language IDs.
- update brains table sql: A script to update the brains table to include a new field for storing the voice ID associated with each brain.
- update user settings table sql: A script to update the user_settings table to include a new field for storing the language ID associated with each user.

2. API Route Scripts:
A) Updates on brain_routes.py
- get_voices: A script for the GET /voices route to fetch all available voice IDs from the voices table in Supabase.
- update_brain_voice: A script for the PUT /brains/{brain_id}/voice route to update the voice ID associated with a specific brain.
- get_brain_voice: A script for the GET /brains/{brain_id}/voice route to fetch the voice ID associated with a specific brain. If no voice ID is associated with the brain, it will set a default one.
B) Updates on user_settings_routes.py
- get_languages: A script for the GET /languages route to fetch all available language IDs from the languages table in Supabase.
- update_user_language: A script for the PUT /users/{user_id}/language route to update the language ID associated with a specific user.
- get_user_language: A script for the GET /users/{user_id}/language route to fetch the language ID associated with a specific user. If no language ID is associated with the user, it will set a default one.

3. Environment Variable Scripts:
- .env: Update this file to include the ELEVENLABS_API_KEY environment variable.

4. Text-to-Speech Integration Scripts:
- elevenlabs_service.py: A script to handle the integration with the ElevenLabs Text-to-Speech service. This involves sending a request to the service with the text, voice model ID, and language output, and receiving an MP3 file with the generated audio of the text.

5. Supabase Client Scripts:
- supabase_client.py: Update this script to include methods for interacting with the new voices and languages tables, and for updating the new fields in the brains and user_settings tables.

6. Model Scripts:
- voices.py: A script to define the data model for the voices.
- languages.py: A script to define the data model for the languages.
- brains.py: Update this script to include the new voice ID field in the brain model.
- user_settings.py: Update this script to include the new language ID field in the user settings model.