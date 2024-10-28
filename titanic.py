import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DIRECT_PATH = True

# 로컬에서 테스트 할때 편리
if DIRECT_PATH:
    # 파일 경로 직접 지정하기
    HOME = os.getcwd()
    trainPath = os.path.join(HOME, 'train.csv')
    df = pd.read_csv(trainPath)
    # st.dataframe(df)

else:
    # 웹 서버에는 파일을 업로드 해줘야 함.
    # 파일 업로드 버튼 (업로드 기능)
    file = st.file_uploader("파일 선택(csv or excel)", type=['csv', 'xls', 'xlsx'])

    if file is not None:
        ext = file.name.split('.')[-1]
        if ext == 'csv':
            # 파일 읽기
            df = pd.read_csv(file)
            # 출력
        elif 'xls' in ext:
            # 엑셀 로드
            df = pd.read_excel(file, engine='openpyxl')
            # 출력
        
        st.dataframe(df)

st.header('타이타닉 생존자 예측')
st.dataframe(df, use_container_width=True)

male_num = len(df[df['Sex'] == 'male'])
female_num = len(df[df['Sex'] == 'female'])

col1, col2 = st.columns(2)
col1.metric(label='타이타닉에 승선한 남자 수', value=male_num)
col2.metric(label='타이타닉에 승선한 여자 수', value=female_num)

fig, ax = plt.subplots()
sex_counts = df['Sex'].value_counts()
ax.bar(sex_counts.index, sex_counts.values)
ax.set_xlabel('Sex')
ax.set_ylabel('Number of Passengers')
ax.set_title('Number of passengers by sex')

st.pyplot(fig)

fig, ax = plt.subplots()
ax.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90)
ax.set_title('Proportion of Passengers by Sex')
ax.axis('equal')

st.pyplot(fig)

null_check = df.isna().sum()

st.write(null_check)

df = df.drop(['Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1)
df['Age'].fillna(df['Age'].mean(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

le_sex = LabelEncoder()
le_embarked = LabelEncoder()

df['Sex'] = le_sex.fit_transform(df['Sex'])
df['Embarked'] = le_embarked.fit_transform(df['Embarked'])

X = df.drop('Survived', axis=1)
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
st.write(f'모델 정확도: {accuracy * 100:.2f}%')

pclass = st.selectbox('Pclass (객실 등급)', [1, 2, 3])
sex = st.selectbox('Sex (성별)', ['male', 'female'])
age = st.number_input('Age (나이)', min_value=0, max_value=120, value=30)
sibsp = st.number_input('Sibsp (형제자매/배우자 수)', min_value=0, max_value=10, value=0)
parch = st.number_input('Parch (부모/자녀 수)', min_value=0, max_value=10, value=0)
fare = st.number_input('Fare (운임 요금)', min_value=0.0, max_value=600.0, value=32.0)
embarked = st.selectbox('Embarked (탑승 항구)', ['C', 'Q', 'S'])

st.write(f'입력된 값: Pclass={pclass}, Sex={sex}, Age={age}, Sibsp={sibsp}, Parch={parch}, Fare={fare}, Embarked={embarked}')

sex_encoded = le_sex.transform([sex])[0]
embarked_encoded = le_embarked.transform([embarked])[0]

new_data = np.array([[pclass, sex_encoded, age, sibsp, parch, fare, embarked_encoded]])

if st.button('생존 여부 예측'):
    prediction = model.predict(new_data)
    if prediction[0] == 1:
        st.success('생존 여부 예측: ' '생존')
    else:
        st.error('생존 여부 예측: ' '사망')