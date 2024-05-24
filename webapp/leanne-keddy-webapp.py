import os
import base64
from datetime import datetime
import shutil

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
TMP_USER_DATA_PATH = 'tmp'
PUBLIC_DATA_PATH = os.path.join(USER_DATA_PATH, 'public')
PROXY_STATEMENTS_PATH = '.proxy-statements'
HIGHLIGHTED_PDF = 'highlighed_'

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'
PDF_SELECTED_KEY = 'PDF_SELECTED_KEY'
PDF_FILE_PATH_KEY = 'PDF_FILE_PATH_KEY'
LABELS_KEY = 'LABELS_KEY'
ACTIVE_LABEL_KEY = 'ACTIVE_LABEL_KEY'

if LOGGED_IN_KEY not in st.session_state:
    st.session_state[LOGGED_IN_KEY] = False

if USER_CRED_KEY not in st.session_state:
    st.session_state[USER_CRED_KEY] = None

if PDF_SELECTED_KEY not in st.session_state:
    st.session_state[PDF_SELECTED_KEY] = False

if PDF_FILE_PATH_KEY not in st.session_state:
    st.session_state[PDF_FILE_PATH_KEY] = None

if LABELS_KEY not in st.session_state:
    st.session_state[LABELS_KEY] = []

if ACTIVE_LABEL_KEY not in st.session_state:
    st.session_state[ACTIVE_LABEL_KEY] = None

# if  not in st.session_state:
#     st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def check_credentials(user_creds : str) -> bool:
    user_path = os.path.join(USER_DATA_PATH, user_creds)    
    return os.path.exists(user_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statements() -> list:
    return [os.path.basename(x) for x in glob.glob(PROXY_STATEMENTS_PATH+'/*.pdf')]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labels() -> list:

    list_of_labels = []

    for label in st.session_state[LABELS_KEY]:
        list_of_labels.append(label['name'])
               
    return list_of_labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Call Back Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_text_cb(selected_text : str) -> None:
    print(selected_text)
    st.session_state.SELECTED_TEXT_KEY = ''    

def add_label_cb(label_name : str,
                 label_colour : str) -> None:    
    st.session_state[LABELS_KEY].append({'name' : label_name, 'colour' : label_colour})

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

def create_tmp_file(pdf_file_name : str):
    # build src and dst paths
    src_path = os.path.join(PROXY_STATEMENTS_PATH, pdf_file_name)
    
    dst_path = os.path.join(USER_DATA_PATH, st.session_state[USER_CRED_KEY])
    dst_path = os.path.join(dst_path, TMP_USER_DATA_PATH)
    dst_path = os.path.join(dst_path,HIGHLIGHTED_PDF+pdf_file_name)
    
    # copy file to tmp
    shutil.copy(src_path, dst_path)
    st.session_state[PDF_FILE_PATH_KEY] = dst_path


def create_data_set_page():   
    
    selected_file = st.sidebar.selectbox(   label='Available Proxy Statements',
                                            options=get_proxy_statements(),
                                            index=None)    
    
    select_file_button = st.sidebar.button('Select')
    
    if select_file_button and selected_file:
        #st.session_state[PDF_FILE_PATH_KEY] = os.path.join(PROXY_STATEMENTS_PATH, selected_file)
        create_tmp_file(selected_file)
        st.session_state[PDF_SELECTED_KEY] = True
        print(st.session_state[PDF_FILE_PATH_KEY])
           
    if st.session_state[PDF_SELECTED_KEY]:
                
        with open(str(st.session_state[PDF_FILE_PATH_KEY]) , 'rb') as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
            pdf_display =   f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
                        """
            st.markdown(pdf_display, unsafe_allow_html=True)   
    
    label_col, colour_col = st.sidebar.columns([3,1])
    
    picked_colour = colour_col.color_picker('Colour')  
    label_name = label_col.text_input('Label')
    st.sidebar.button(  'Add Label',
                        on_click=add_label_cb,
                        args=[label_name,picked_colour])
    
    st.session_state[ACTIVE_LABEL_KEY] = st.sidebar.selectbox(  label='Select Label',
                                                                options=get_labels(),
                                                                index=None) 

    
    selected_text = st.sidebar.text_area(label='Selected Text',
                                         key='SELECTED_TEXT_KEY')
    
    st.sidebar.button('Add Text',
                      on_click=add_text_cb, 
                      args=[selected_text])
       
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

