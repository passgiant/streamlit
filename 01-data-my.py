import streamlit as st
import pandas as pd
import numpy as np

st.title('데이터프레임 튜토리얼')

dataframe = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
})

st.dataframe(dataframe, use_container_width=False) # True or False 가능

st.table(dataframe)

st.metric(label='온도', value='10°c', delta='1.2°c')
st.metric(label='삼성전자', value='61,000 원', delta='-1,200 원')

col1, col2, col3 = st.columns(3)
col1.metric(label='달러USD', value='1,228 원', delta='-12.00 원')
col2.metric(label='일본JPY(100엔)', value='958.63 원', delta='-7.44 원')
col3.metric(label='유럽연합EUR', value='1,335.82 원', delta='11.44 원')