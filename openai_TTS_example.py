from pathlib import Path
from openai import OpenAI
import openai

openai.api_key = ""  # Set your API key here

# client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = openai.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(speech_file_path)