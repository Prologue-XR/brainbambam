from elevenlabs import set_api_key, voices, generate, play, save

set_api_key("f4ceca83f3f62f63f6274fb9bce3e267")

voices = voices()
voices_data = []

audio = generate(
    text="돌턴... 난 그냥 모든 것에 대해 사과하고 싶었어요. 형, 보고 싶어요. 그리고 우리가 문제를 해결하기를 정말 바랐어요.",
    voice="Edu",
    model="eleven_multilingual_v2",
)

play(audio)
save(audio, "test.mp3")


# with open("brainbambam_create_voices_table.sql", "w") as f:
#     for voice in voices.voices:
#         voice_dict = {
#             "voice_id": str(uuid.uuid4()),
#             "voice_name": voice.name,
#             "elevenlabs_id": voice.voice_id,
#         }
#         # save only if category is "cloned"
#         if voice.category == "premade":
#             voices_data.append(voice_dict)
#             f.write(
#                 f"INSERT INTO voices (voice_id, voice_name, elevenlabs_id) VALUES ('{voice_dict['voice_id']}', '{voice_dict['voice_name']}', '{voice_dict['elevenlabs_id']}');\n"
#             )
