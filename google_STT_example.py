# Import the Speech-to-Text client library
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient()

# The content of the audio file to transcribe
file_path = 'output.mp3'

with open(file_path, 'rb') as f:
    audio_content = f.read()

# transcribe speech
audio = speech.RecognitionAudio(content=audio_content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=24000,
    language_code="ko-KR",
    model="default",
    audio_channel_count=1,
    enable_word_confidence=True,
    enable_word_time_offsets=True,
)

# Detects speech in the audio file
operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))