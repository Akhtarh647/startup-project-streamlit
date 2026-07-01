import streamlit as st
import pandas as pd
import time

st.title('startup Dashboard')
st.header('I am learning Streamlit')
st.subheader('I am loving it')
st.write("This is a normal text")
st.markdown("""
### My favourite Movies
- Race
- Hum
- Rockstar 
""")

st.code("""
def fo(int):
    return fo*2

x=fo(2)
""")

st.latex('x^2+2x+3=0')

df = pd.DataFrame({
    'name': ['ak', 'sk', 'hk'],
    'marks': [10, 20, 30],
    'package': [5, 5, 6]
})

st.dataframe(df)

st.metric('Revenue', 'RS 3L', '3%')

st.json({
    'name': ['ak', 'sk', 'hk'],
    'marks': [10, 20, 30],
    'package': [5, 5, 6]
})

st.image('OIP.jpeg')

st.sidebar.subheader('Sidebar')

col1, col2 = st.columns(2)
with col1:
    st.image('OIP.jpeg')
with col2:
    st.json({
        'name': ['ak', 'sk', 'hk'],
        'marks': [10, 20, 30],
        'package': [5, 5, 6]
    })

st.error('login failes')
st.success('login success')
st.info('login success')
st.warning('login success')

bar = st.progress(0)

for i in range(1, 101):
    bar.progress(i)

email = st.text_input('Enter your name')
number = st.number_input('Enter your number')
st.datetime_input('Enter Regis date')

###########################################################

#email = st.text_input('Enter your name')
password = st.text_input('password')
gender = st.selectbox('Select your gender',['Male','Female'])

btn=st.button('Submit')

if btn:
    if email =='ak@gmail.com' and password == '1234':
        st.success('Login Successful')
        st.balloons()
        st.write(gender)
    else:
        st.error('login failed')