import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def transcribe_audio(audio_file):
    with open(audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio,
            language="en",
            prompt="You are a helpful assistant that transcribes audio files into text. The audio is in English. Please transcribe every single sentence in the audio.",
        )
    return transcript.text
