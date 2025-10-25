from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


# Whisper model
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
        )
    return transcript.text
