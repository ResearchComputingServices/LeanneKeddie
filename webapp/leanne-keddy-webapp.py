import os
import base64
from datetime import datetime

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_pdf_viewer import pdf_viewer

import pandas as pd
import glob
from pprint import pprint
from PIL import Image

import pyperclip

from SentenceClassifier.Classifier import SentenceClassifier
from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

USER_DATA_PATH = '.user-data'
PUBLIC_DATA_PATH = os.path.join(USER_DATA_PATH, 'public')

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'


if LOGGED_IN_KEY not in st.session_state:
    st.session_state[LOGGED_IN_KEY] = False

if USER_CRED_KEY not in st.session_state:
    st.session_state[USER_CRED_KEY] = None

# if  not in st.session_state:
#     st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def check_credentials(user_creds : str) -> bool:
    user_path = os.path.join(USER_DATA_PATH, user_creds)    
    return os.path.exists(user_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Page Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def home_page():
    st.title("Keddie Tool")
    st.markdown("""This tool enables supervised topic modelling of form DEF 14A 
                (Definitive Proxy Statement) filed by S&P500 corportations between
                the years of 2016 and 2022.""")
    
    st.markdown("To gain access please contact: rcs@cunet.carleton.ca")
    
    user_creds = st.text_input(label = "User Credentials")
    
    if st.button('Sign In'):       
        if not check_credentials(user_creds) or user_creds == '':
            st.error('User Credentials not found.')
            st.session_state[LOGGED_IN_KEY] = False
        else:
            st.sidebar.success('Sign-In successful')
            st.session_state[LOGGED_IN_KEY] = True
            st.session_state[USER_CRED_KEY] = user_creds
            st.rerun()
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_data_set_page():
    uploaded_file = st.file_uploader("Choose a file")
    
    pdf_column, display_column = st.columns([2,1])
     
    if uploaded_file:
        base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
        pdf_display =   f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="2100px" type="application/pdf"></iframe>
                        """
        pdf_column.markdown(pdf_display, unsafe_allow_html=True)
            
    if display_column.button('submit'):
        display_column.markdown(str(pyperclip.paste()))
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def _page():
#     pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initialize the page
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

st.set_page_config(page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                   layout="wide")

st.sidebar.title('Navigation')
user_page_selection = st.sidebar.radio('Pages', 
                                       options=['Home', 'Create Data Set'],
                                       disabled=(not st.session_state[LOGGED_IN_KEY]))

if user_page_selection == 'Create Data Set':
    create_data_set_page()
else:
    home_page()

