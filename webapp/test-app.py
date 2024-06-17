import streamlit as st



st.set_page_config(page_title="Just a Test",
                   layout="wide")

if st.button('Press Me'):
    st.info('You Pressed a Button')