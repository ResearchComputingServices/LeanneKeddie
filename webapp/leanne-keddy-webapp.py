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

from PDFHighlighter import PDFHighlighter
# from SentenceClassifier.Classifier import SentenceClassifier
# from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

USER_DATA_PATH = '.user-data'
TMP_USER_DATA_PATH = 'tmp'
SESSION_DIR_PATH = 'session'
PUBLIC_DATA_PATH = os.path.join(USER_DATA_PATH, 'public')
PROXY_STATEMENTS_PATH = '.proxy-statements'
HIGHLIGHTED_PDF = 'highlighed_'

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'
PDF_SELECTED_KEY = 'PDF_SELECTED_KEY'
PDF_HIGHLIGHTED_FILE_PATH_KEY = 'PDF_HIGHLIGHTED_FILE_PATH_KEY'
PDF_ORIGINAL_FILE_PATH_KEY = 'PDF_ORIGINAL_FILE_PATH_KEY'
LABELS_KEY = 'LABELS_KEY'
ACTIVE_LABEL_KEY = 'ACTIVE_LABEL_KEY'
PDF_HIGHLIGHTER_KEY = 'PDF_HIGHLIGHTER_KEY'
LABELLED_SENTENCES_KEY = 'LABELLED_SENTENCES_KEY'

if LOGGED_IN_KEY not in st.session_state:
    st.session_state[LOGGED_IN_KEY] = False

if USER_CRED_KEY not in st.session_state:
    st.session_state[USER_CRED_KEY] = None

if PDF_SELECTED_KEY not in st.session_state:
    st.session_state[PDF_SELECTED_KEY] = False

if PDF_HIGHLIGHTED_FILE_PATH_KEY not in st.session_state:
    st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY] = None
    
if PDF_ORIGINAL_FILE_PATH_KEY not in st.session_state:
    st.session_state[PDF_ORIGINAL_FILE_PATH_KEY] = None

if LABELS_KEY not in st.session_state:
    st.session_state[LABELS_KEY] = []

if ACTIVE_LABEL_KEY not in st.session_state:
    st.session_state[ACTIVE_LABEL_KEY] = None

if PDF_HIGHLIGHTER_KEY not in st.session_state:
    st.session_state[PDF_HIGHLIGHTER_KEY] = None

if LABELLED_SENTENCES_KEY not in st.session_state:
    st.session_state[LABELLED_SENTENCES_KEY] = {}

# if  not in st.session_state:
#     st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def session_to_console() -> None:
    print(PDF_ORIGINAL_FILE_PATH_KEY,': ',st.session_state[PDF_ORIGINAL_FILE_PATH_KEY])
    print(LABELS_KEY,': ')
    pprint(st.session_state[LABELS_KEY])
    print(LABELLED_SENTENCES_KEY,': ')
    pprint(st.session_state[LABELLED_SENTENCES_KEY])
    print('~'*80)

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

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    colour = tuple(float(int(value[i:i + lv // 3], 16)/255.) for i in range(0, lv, lv // 3))
    
    return colour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_tmp_file(pdf_file_name : str):
    # build src and dst paths
    src_path = os.path.join(PROXY_STATEMENTS_PATH, pdf_file_name)
    
    dst_path = os.path.join(USER_DATA_PATH, st.session_state[USER_CRED_KEY])
    dst_path = os.path.join(dst_path, TMP_USER_DATA_PATH)
    dst_path = os.path.join(dst_path,HIGHLIGHTED_PDF+pdf_file_name)
    
    # copy file to tmp
    shutil.copy(src_path, dst_path)
    st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY] = dst_path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_label():
    
    for label in st.session_state[LABELS_KEY]:
        if label['name'] == st.session_state[ACTIVE_LABEL_KEY]:
            return label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unique_label(label_name : str) -> bool:
     
    for label in st.session_state[LABELS_KEY]:
        if label['name'] ==label_name:
            return False
        
    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Call Back Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_text_cb(selected_text : str) -> None:
    # check that a label is selected if not show error msg
    if not st.session_state[ACTIVE_LABEL_KEY]:
        st.sidebar.error('No Label Selected.')
        return
    
    # check if text is available
    if len(selected_text) == 0:
        st.sidebar.error('No Text Selected.')
        return
    
    active_label = get_active_label()
    
    # clear text selected text_area widget
    st.session_state.SELECTED_TEXT_KEY = ''

    # Highlight the text in the PDF
    st.session_state[PDF_HIGHLIGHTER_KEY].highlight(phrase=selected_text,
                                                    colour=active_label['colour'])      
    st.session_state[PDF_HIGHLIGHTER_KEY].save()   
    
    # Save the labelled sentence for the session
    if active_label['name'] in st.session_state[LABELLED_SENTENCES_KEY].keys():  
        st.session_state[LABELLED_SENTENCES_KEY][active_label['name']].append(selected_text)
    else:
        st.session_state[LABELLED_SENTENCES_KEY][active_label['name']] = [selected_text]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_label_cb(label_name : str,
                 label_colour : str) -> None:    
    
    colour_code = hex_to_rgb(label_colour)
    
    if unique_label(label_name):
        st.session_state[LABELS_KEY].append({'name' : label_name, 'colour' : colour_code})
    else:
        st.sidebar.error(f'Label "{label_name}" already exists')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_session_cb():
    output_path = os.path.join(USER_DATA_PATH,USER_CRED_KEY,SESSION_DIR_PATH)
    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_session_cb():
    pass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def export_session_cb():
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clear_session_cb():
    session_to_console()
    pass

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
def select_file_cb(pdf_file_name : str) -> None:
    if pdf_file_name:
        st.session_state[PDF_ORIGINAL_FILE_PATH_KEY] = pdf_file_name
        create_tmp_file(pdf_file_name)
        st.session_state[PDF_HIGHLIGHTER_KEY] = PDFHighlighter(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY])
        st.session_state[PDF_SELECTED_KEY] = True 

def select_label_cb(selected_label : str) -> None:
    if selected_label:
        st.session_state[ACTIVE_LABEL_KEY] = selected_label
    else:
        st.session_state[ACTIVE_LABEL_KEY] = ''

def create_data_set_page():   
    
    with st.sidebar.popover(f'Select Proxy Statement: {st.session_state[PDF_ORIGINAL_FILE_PATH_KEY]}'):
        selected_file = st.selectbox(   label='Available Proxy Statements',
                                        options=get_proxy_statements(),
                                        index=None)    
        st.button(  'Select',
                    on_click=select_file_cb,
                    args=[selected_file])
        
            
                    
    with st.sidebar.popover(f'Label: {st.session_state[ACTIVE_LABEL_KEY]}'):
        label_col, colour_col = st.columns([3,1])
        
        picked_colour = colour_col.color_picker('Colour')  
        label_name = label_col.text_input('Add Label')
        st.button(  'Add',
                    on_click=add_label_cb,
                    args=[label_name,picked_colour])
        
        selected_label = st.selectbox(  label='Select Label',
                                        options=get_labels(),
                                        index=None) 
        st.button('select',
                  on_click=select_label_cb,
                  args=[selected_label] )
        
    with st.sidebar.popover('Options'):
        save_col, load_col = st.columns(2)
        save_col.button('Save',on_click=save_session_cb)
        load_col.button('Load',on_click=load_session_cb)
        
        export_col, clear_col = st.columns(2)
        export_col.button('Export',on_click=export_session_cb)
        clear_col.button('Clear',on_click=clear_session_cb)
   
    
    selected_text = st.sidebar.text_area(label='Selected Text',
                                         key='SELECTED_TEXT_KEY')
    
    st.sidebar.button('Add Text',
                      on_click=add_text_cb, 
                      args=[selected_text])
    
   
       
    # Main Page Widgets
       
    if st.session_state[PDF_SELECTED_KEY]:
                
        with open(str(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY]) , 'rb') as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
            pdf_display =   f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
                        """
            st.markdown(pdf_display, unsafe_allow_html=True)   
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

