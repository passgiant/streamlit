from google.cloud import speech
import pyaudio
import keyboard  # keyboard 라이브러리 임포트

# Google Cloud Speech-to-Text 클라이언트 초기화
client = speech.SpeechClient()

# PyAudio 초기화
p = pyaudio.PyAudio()

# 마이크 입력 설정
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=48000,
                input=True,
                frames_per_buffer=1024)

# 음성 데이터를 담을 버퍼
audio_content = []

print("녹음 시작 (말하기 시작하세요). 'q' 키를 누르면 녹음이 종료됩니다.")

# 음성 녹음 루프
while True:
    # 마이크에서 데이터 읽기
    data = stream.read(1024)
    audio_content.append(data)

    # 'q' 키를 누르면 녹음 종료
    if keyboard.is_pressed('q'):  # keyboard 라이브러리 사용
        print("녹음 종료")
        break

# 스트림 닫기
stream.stop_stream()
stream.close()

# PyAudio 닫기
p.terminate()

# 음성 데이터를 합치기
audio_content = b''.join(audio_content)

# 음성 인식 설정
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="ko-KR",  # 한국어로 설정
    model="default",
    audio_channel_count=1,
    enable_word_confidence=True,
    enable_word_time_offsets=True,
)

# 음성 데이터를 Speech-to-Text API로 전송
audio = speech.RecognitionAudio(content=audio_content)
operation = client.long_running_recognize(config=config, audio=audio)

print("음성 인식 진행 중...")

# 인식 결과를 기다림
response = operation.result(timeout=90)

# 결과 출력
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))