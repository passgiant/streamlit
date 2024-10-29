import streamlit as st
import os

# upload 시에 'upload'라는 폴더를 생성하고 그곳에 파일을 보관
# 폴더 생성
# 파일 저장

HOME = os.getcwd()
UPLOAD_DIR = os.path.join(HOME, 'uploads')

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

uploaded_files = st.file_uploader(
    "이미지 파일 선택", accept_multiple_files=True
)

# 파일을 동시에 여러 개 업로드시에는 for를 활용
for uploaded_file in uploaded_files:
    # 업로드된 데이터를 image 변수에 저장
    # read() 함수의 의미는 네트워크를 통해 데이터를 가져온다.
    image = uploaded_file.read()
    st.image(image, caption=uploaded_file.name)

    # 파일 uploads 폴더에 저장
    # 이미지는 binary
    with open(os.path.join(UPLOAD_DIR, uploaded_file.name), 'wb') as f:
        f.write(image)
        f.close()
        st.success(f'{uploaded_file.name} 저장 완료!')