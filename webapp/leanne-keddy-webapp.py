import os
import base64
import shutil
import json

import streamlit as st

import pandas as pd
import glob
from pprint import pprint

from PDFHighlighter import PDFHighlighter
# from SentenceClassifier.Classifier import SentenceClassifier
# from ExDocGen.ExtractedDocumentGenerator import ExtractedDocumentGenerator

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Dictionary keys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PROXY_STATEMENT_FILENAME = 'filename'
PROXY_STATEMENT_FILE_ID = 'file-id'

LABEL_NAME = 'name'
LABEL_COLOUR = 'colour'
LABEL_ID = 'label-id'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PROXY_STATEMENTS_PATH = '.proxy-statements'
USER_DATA_PATH = '.user-data'
PUBLIC_DATA_PATH = '.public-data'
TMP_USER_DATA_PATH = 'tmp'
SESSION_DIR_PATH = 'session'
HIGHLIGHTED_PDF = 'highlighed_'
JSON_EXT = '.json'
PRIVATE_DATA_SET_PATH = 'data-sets'

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'
PDF_SELECTED_KEY = 'PDF_SELECTED_KEY'
PDF_HIGHLIGHTED_FILE_PATH_KEY = 'PDF_HIGHLIGHTED_FILE_PATH_KEY'
PDF_HIGHLIGHTER_KEY = 'PDF_HIGHLIGHTER_KEY'
LABELLED_SENTENCES_KEY = 'LABELLED_SENTENCES_KEY'
ACTIVE_DATA_SET_KEY = 'ACTIVE_DATA_SET_KEY'
ACTIVTE_PROXY_STATEMENT_KEY = 'PDF_ORIGINAL_FILE_PATH_KEY'
ACTIVE_LABEL_KEY = 'ACTIVE_LABEL_KEY'

if LOGGED_IN_KEY not in st.session_state:
    st.session_state[LOGGED_IN_KEY] = False

if USER_CRED_KEY not in st.session_state:
    st.session_state[USER_CRED_KEY] = None

if PDF_SELECTED_KEY not in st.session_state:
    st.session_state[PDF_SELECTED_KEY] = False

if PDF_HIGHLIGHTED_FILE_PATH_KEY not in st.session_state:
    st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY] = None
    
if PDF_HIGHLIGHTER_KEY not in st.session_state:
    st.session_state[PDF_HIGHLIGHTER_KEY] = None

if LABELLED_SENTENCES_KEY not in st.session_state:
    st.session_state[LABELLED_SENTENCES_KEY] = {}

if ACTIVE_DATA_SET_KEY not in st.session_state:
    st.session_state[ACTIVE_DATA_SET_KEY] = None

if ACTIVTE_PROXY_STATEMENT_KEY not in st.session_state:
    st.session_state[ACTIVTE_PROXY_STATEMENT_KEY] = {PROXY_STATEMENT_FILENAME : '',
                                                     PROXY_STATEMENT_FILE_ID : -1}

if ACTIVE_LABEL_KEY not in st.session_state:
    st.session_state[ACTIVE_LABEL_KEY] = {LABEL_NAME : '',
                                          LABEL_COLOUR : (0,0,0),
                                          LABEL_ID : -1}

# if  not in st.session_state:
#     st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def session_to_console() -> None:
    print(ACTIVTE_PROXY_STATEMENT_KEY,':')
    pprint(st.session_state[ACTIVTE_PROXY_STATEMENT_KEY])
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

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    colour = tuple(float(int(value[i:i + lv // 3], 16)/255.) for i in range(0, lv, lv // 3))
    
    return colour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labels() -> list:

    list_of_labels = []

    for label in st.session_state[ACTIVE_DATA_SET_KEY]['labels']:
        list_of_labels.append(label['name'])
               
    return list_of_labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_label_id() -> int:
    return len(st.session_state[ACTIVE_DATA_SET_KEY]['labels'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_file_id() -> int:
    return len(st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unique_label(label_name : str) -> bool:
    
    labels_dict = st.session_state[ACTIVE_DATA_SET_KEY]['labels']
    
    if any(label['name'] == label_name for label in labels_dict):
        return False
       
    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check_for_previous_highlights(pdf_file_name : str) -> bool:
    
    for statement in st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements']:
        if statement[PROXY_STATEMENT_FILENAME] == pdf_file_name:
            st.session_state[ACTIVTE_PROXY_STATEMENT_KEY] = statement
            return True
       
    return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_proxy_to_data_set(pdf_file_name : str) -> None:
    
    file_id = generate_file_id()
    
    new_proxy_statement_dict = {PROXY_STATEMENT_FILENAME : pdf_file_name,
                                PROXY_STATEMENT_FILE_ID : file_id}
    
    st.session_state[ACTIVTE_PROXY_STATEMENT_KEY] = new_proxy_statement_dict
    
    st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements'].append(new_proxy_statement_dict)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_label_from_name(label_name : str) -> dict:
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY]['labels']:
        if label[LABEL_NAME] == label_name:
            return label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_data_set_files():
    
    user_data_sets_path = os.path.join( USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH)
    
    
    user_data_sets = [os.path.basename(x) for x in glob.glob(user_data_sets_path+'/*.json')]
    
    public_data_sets = [os.path.basename(x) for x in glob.glob(PUBLIC_DATA_PATH+'/*.json')]
       
    return user_data_sets + public_data_sets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
def get_label_from_id(label_id : int) -> dict:
    labels_dict = st.session_state[ACTIVE_DATA_SET_KEY]['labels']

    for label in labels_dict:
        if label['label-id'] == label_id:
            return label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labelled_text_from_file_id(file_id : int) -> list:
    
    labelled_texts = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text']:
        if labelled_text['file-id'] == file_id:
            labelled_texts.append(labelled_text)
        
    return labelled_texts

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def apply_previous_highlights() -> None:
    
    file_id = st.session_state[ACTIVTE_PROXY_STATEMENT_KEY][PROXY_STATEMENT_FILE_ID]
    labelled_texts = get_labelled_text_from_file_id(file_id)
    
    for labelled_text in labelled_texts:
    
        label_colour = get_label_from_id(labelled_text['label-id'])['colour']
        text = labelled_text['text']
    
        st.session_state[PDF_HIGHLIGHTER_KEY].highlight(phrase=text,
                                                        colour=label_colour)      
    st.session_state[PDF_HIGHLIGHTER_KEY].save()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_file_from_id(file_id : int) -> dict:
        
    for file_dict in st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements']:
        if file_dict[PROXY_STATEMENT_FILE_ID] == file_id:
            return file_dict

    return {PROXY_STATEMENT_FILENAME : 'Unknown', PROXY_STATEMENT_FILE_ID : -1}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Call Back Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_file_cb(file_name : str):
    
    data_set_file_path = os.path.join(  USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        file_name)
    
    if not os.path.exists(data_set_file_path):
        data_set_file_path = os.path.join(PUBLIC_DATA_PATH, file_name)
    
    st.session_state[ACTIVE_DATA_SET_KEY] = json.load(open(data_set_file_path))

    # TODO: Clear the activate proxy statement and label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_labelled_text_cb(selected_text : str) -> None:
    # check that a label is selected if not show error msg
    if not st.session_state[ACTIVE_LABEL_KEY]:
        st.sidebar.error('No Label Selected.')
        return
    
    # check if text is available
    if len(selected_text) == 0:
        st.sidebar.error('No Text Selected.')
        return    
    # clear text selected text_area widget
    st.session_state.SELECTED_TEXT_KEY = ''

    active_label = st.session_state[ACTIVE_LABEL_KEY]

    # Highlight the text in the PDF
    st.session_state[PDF_HIGHLIGHTER_KEY].highlight(phrase=selected_text,
                                                    colour=active_label['colour'])      
    st.session_state[PDF_HIGHLIGHTER_KEY].save()   
    
    # Save the labelled sentence for the session
    file_id = st.session_state[ACTIVTE_PROXY_STATEMENT_KEY]['file-id']
    
    st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text'].append({'text': selected_text,
                                                                   'label-id' : active_label['label-id'],
                                                                   'file-id' : file_id})
                                                
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_label_cb(label_name : str,
                 label_colour : str) -> None:    
    
    colour_code = hex_to_rgb(label_colour)
    
    if unique_label(label_name):
        label_id = generate_label_id()
        
        st.session_state[ACTIVE_DATA_SET_KEY]['labels'].append({'name' : label_name, 
                                                                'colour' : colour_code,
                                                                'label-id' : label_id})
    else:
        st.sidebar.error(f'Label "{label_name}" already exists')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
def select_file_cb(pdf_file_name : str) -> None:
    
    if pdf_file_name:
        # create a tmp file for it proxy statement which will be highlighted      
        create_tmp_file(pdf_file_name)
        
        # create a PDFHighlighter for the temporary file
        st.session_state[PDF_HIGHLIGHTER_KEY] = PDFHighlighter(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY])
        
        # if the file has previously been highlighted apply the highlights
        if check_for_previous_highlights(pdf_file_name):
            apply_previous_highlights()
        else:
            add_proxy_to_data_set(pdf_file_name)
        
        st.session_state[PDF_SELECTED_KEY] = True
    else:
        st.sidebar.error('No File Selected')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def select_label_cb(selected_label : str) -> None:
    
    if selected_label:
        st.session_state[ACTIVE_LABEL_KEY] = get_label_from_name(selected_label)
    else:
        st.session_state[ACTIVE_LABEL_KEY] = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_session_cb(file_name : str,
                    save_type : str) -> None:
    
    # get the output path to save the file too
    output_file_path = os.path.join(PUBLIC_DATA_PATH, file_name+JSON_EXT)
    if save_type == 'private':
        output_file_path = os.path.join(USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        file_name+JSON_EXT)
   
    # write the activet data set to file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(st.session_state[ACTIVE_DATA_SET_KEY], f, ensure_ascii=False, indent=4)
   
    # check that the file exists
    if os.path.exists(output_file_path):
        st.sidebar.success('Save Sucessful.')
    else:
        st.sidebar.error('Unable to save Data Set.')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_data_set_cb(data_set_name : str) -> None:
    # TODO: check if there is a data set with the same name in public or private
    # data folders
    
    st.session_state[ACTIVE_DATA_SET_KEY] = {   'name' :            data_set_name,
                                                'labels' :          [],
                                                'proxy-statements': [],
                                                'labelled-text':    []}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Page Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_data_set_page():
    name_col, type_cal = st.sidebar.columns([2,1])
    
    file_name = name_col.text_input('Filename')
    save_type = type_cal.radio( 'Save Type',
                                options = ['private', 'public'])
    st.sidebar.button(  'Save',
                        on_click=save_session_cb,
                        args=[file_name, save_type])
        
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

def add_data_page():   
    
    with st.sidebar.popover(f'Select Proxy Statement: {st.session_state[ACTIVTE_PROXY_STATEMENT_KEY][PROXY_STATEMENT_FILENAME]}'):
        selected_file = st.selectbox(   label='Available Proxy Statements',
                                        options=get_proxy_statements(),
                                        index=None)    
        st.button(  'Select',
                    on_click=select_file_cb,
                    args=[selected_file])
                         
    with st.sidebar.popover(f'Label: {st.session_state[ACTIVE_LABEL_KEY][LABEL_NAME]}'):
        if st.session_state[ACTIVE_DATA_SET_KEY]:
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
        
    selected_text = st.sidebar.text_area(label='Selected Text',
                                         key='SELECTED_TEXT_KEY')
    
    st.sidebar.button('Add Text',
                      on_click=add_labelled_text_cb,
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

def load_data_set_page():
    selected_file = st.sidebar.selectbox(   label='Available Proxy Statements',
                                            options=get_data_set_files(),
                                            index=None)    
    st.sidebar.button(  'Load',
                        on_click=load_file_cb,
                        args=[selected_file])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def review_data_set_page():
    
    data_list = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text']:
        
        label =  get_label_from_id(labelled_text[LABEL_ID])[LABEL_NAME]
        filename = get_file_from_id(labelled_text[PROXY_STATEMENT_FILE_ID])[PROXY_STATEMENT_FILENAME]
        
        data_list.append({'Label' : label,
                          'Filename' : filename,
                          'Text' : labelled_text['text']})        
    
    df = pd.DataFrame(data_list)
    
    edited_df = st.data_editor(df, use_container_width=True)

    st.sidebar.button('Update')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def create_data_set_page():
    data_set_name = st.sidebar.text_input('Data Set Name:')
    st.sidebar.button(  'Create',
                        on_click=create_data_set_cb,
                        args=[data_set_name])
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initialize the page
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

st.set_page_config(page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                   layout="wide")

st.sidebar.title('Navigation')

if st.sidebar.button('display'):
    print('\n'*100)
    print('~'*80)
    pprint(st.session_state[ACTIVE_DATA_SET_KEY])
    print('~'*80)
    pprint(st.session_state[ACTIVTE_PROXY_STATEMENT_KEY])
    print('~'*80)
    pprint(st.session_state[ACTIVE_LABEL_KEY])

user_page_selection = st.sidebar.radio('Pages', 
                                       options=['Home',
                                                'Create New Data Set',
                                                'Load Data Set',
                                                'Add Data',
                                                'Review',
                                                'Save'],
                                       disabled=(not st.session_state[LOGGED_IN_KEY]))

if user_page_selection == 'Create New Data Set':
    create_data_set_page()
elif user_page_selection == 'Load Data Set':
    load_data_set_page()
elif user_page_selection == 'Add Data':
    add_data_page()
elif user_page_selection == 'Review':
    review_data_set_page()
elif user_page_selection == 'Save':
    save_data_set_page()
else:
    home_page()

