import streamlit as st

st.title('이것은 타이틀입니다.')

st.title('거울 :mirror:')

st.header('헤더 입력 가능 :knot:')

st.subheader('이것은 subheader')

st.caption('캡션을 한번 넣어 봤습니다.')

sample_code = '''
print('hello world')
'''
st.code(sample_code, language='python')

st.text('일반적인 텍스트를 입력해 봄')

st.markdown('streamlit은 **마크다운 문법을 지원**합니다.')

st.markdown('텍스트의 색상을 :green[초록색]으로, 그리고 **:blue[파란색]** 볼드체로 설정할 수 있습니다.')
st.markdown(':green[$\sqrt{x^2+y^2}=1$]와 같이 latex 문법의 수식 표현도 가능합니다 :pencil:')

st.latex(r'\sqrt{x^2+y^2}=1')