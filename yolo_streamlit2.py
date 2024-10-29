# 동영상 불러올 때 에러나긴 함, 대신 다운로드하게 하기?
# 진행 바도 만들어보기?

import streamlit as st
import os
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

# 모델 로드
@st.cache_resource
def load_model(model_name):
    return YOLO(model_name + ".pt")

HOME = os.getcwd()
# 업로드된 이미지를 저장할 디렉터리 설정
UPLOAD_DIR = os.path.join(HOME, "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 파일 업로드
st.title("이미지/동영상 업로드 및 YOLOv8 객체 탐지")

# Sidebar에서 YOLO 모델 선택, confidence 설정, 입력 유형 선택
st.sidebar.title("YOLO 모델 선택 및 입력 유형")
model_type = st.sidebar.radio("모델을 선택하세요", ("yolov8n", "yolov8s", "yolov8m"))
confidence = st.sidebar.slider("Confidence threshold", 0.0, 1.0, 0.25)
input_type = st.sidebar.radio("입력 유형 선택", ("이미지", "동영상"))

uploaded_file = st.file_uploader("파일을 업로드하세요", type=["jpg", "jpeg", "png", "mp4", "avi"])

if uploaded_file:
    # 모델 로드
    model = load_model(model_type)

    if input_type == "이미지" and uploaded_file.type in ["image/jpeg", "image/png"]:
        # 원본 이미지 표시
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        imageBGR = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 이미지 예측
        with st.spinner("Predicting on image..."):
            results = model.predict(source=imageBGR, conf=confidence)

        # 결과 이미지 저장 및 표시
        #result_img = results[0].plot(line_width=1, color=(255, 0, 0))
        result_img = results[0].plot()  # 결과 플롯 생성
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        result_image = Image.fromarray(result_img)

        # 결과 출력
        col1, col2 = st.columns(2)
        with col1:
            st.header("입력된 이미지")
            st.image(image, use_column_width=True)
        
        with col2:
            st.header("탐지 결과")
            st.image(result_image, use_column_width=True)

    elif input_type == "동영상" and uploaded_file.type == "video/mp4":
        # 동영상 예측
        st.video(uploaded_file)
        
        with st.spinner("Predicting on video..."):
            temp_video_path = os.path.join(UPLOAD_DIR, "uploaded_video.mp4")
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())
            
            results = model.predict(source=temp_video_path, conf=confidence, save=True)

        # 결과 동영상 표시
        result_video_path = os.path.join(results[0].save_dir, "uploaded_video.mp4")
        st.video(str(result_video_path))
    else:
        st.error("선택한 입력 유형과 업로드한 파일이 일치하지 않습니다.")