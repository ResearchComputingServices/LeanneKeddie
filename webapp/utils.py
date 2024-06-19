import os
import shutil
import json

import streamlit as st

import pandas as pd
import glob

from SentenceClassifier.DataSet import DataSet

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
PROXY_STATEMENTS_BASE_PATH = '.proxy-statements'
PROXY_STATEMENT_PDFS_PATH = os.path.join(PROXY_STATEMENTS_BASE_PATH, 'pdfs')
PROXY_STATEMENT_JSONS_PATH = os.path.join(PROXY_STATEMENTS_BASE_PATH, 'json')

USER_DATA_PATH = '.user-data'
PRIVATE_DATA_SET_PATH = 'data-sets'
PRIVATE_CLASSIFIER_PATH = 'classifier'

PUBLIC_DATA_PATH = '.public-data'
PUBLIC_CLASSIFIER_PATH = os.path.join(PUBLIC_DATA_PATH,
                                     'classifier')
PUBLIC_DATA_SET_PATH = os.path.join(PUBLIC_DATA_PATH,
                                    'data-set')

TMP_USER_DATA_PATH = 'tmp'
HIGHLIGHTED_PDF = 'highlighed_'
JSON_EXT = '.json'

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'
PDF_SELECTED_KEY = 'PDF_SELECTED_KEY'
PDF_HIGHLIGHTED_FILE_PATH_KEY = 'PDF_HIGHLIGHTED_FILE_PATH_KEY'
PDF_HIGHLIGHTER_KEY = 'PDF_HIGHLIGHTER_KEY'
LABELLED_SENTENCES_KEY = 'LABELLED_SENTENCES_KEY'
TRAIN_TEST_RESULTS_KEY = 'TRAIN_TEST_RESULTS_KEY'
TRAIN_FIGURE_KEY = 'TRAIN_FIGURE_KEY'
ACTIVE_DATA_SET_KEY = 'ACTIVE_DATA_SET_KEY'
ACTIVTE_PROXY_STATEMENT_KEY = 'PDF_ORIGINAL_FILE_PATH_KEY'
ACTIVE_LABEL_KEY = 'ACTIVE_LABEL_KEY'
ACTIVE_CLASSIFIER_KEY = 'ACTIVE_CLASSIFIER_KEY'
ACTIVE_RESULTS_KEY = 'ACTIVE_RESULTS_KEY'
RESULTS_CSV_KEY = 'RESULTS_CSV_KEY'

def initialize_session_state():

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
        # st.session_state[ACTIVE_DATA_SET_KEY] =  {  'name' :           'None',
        #                                             'labels' :          [],
        #                                             'proxy-statements': [],
        #                                             'labelled-text':    [],
        #                                             'initialized':      0}
        st.session_state[ACTIVE_DATA_SET_KEY] = None

    if ACTIVTE_PROXY_STATEMENT_KEY not in st.session_state:
        st.session_state[ACTIVTE_PROXY_STATEMENT_KEY] = {PROXY_STATEMENT_FILENAME : '',
                                                        PROXY_STATEMENT_FILE_ID : -1}

    if ACTIVE_LABEL_KEY not in st.session_state:
        st.session_state[ACTIVE_LABEL_KEY] = {LABEL_NAME : '',
                                            LABEL_COLOUR : (0,0,0),
                                            LABEL_ID : -1}
        
    if TRAIN_TEST_RESULTS_KEY  not in st.session_state:
        st.session_state[TRAIN_TEST_RESULTS_KEY] = None

    if TRAIN_FIGURE_KEY not in st.session_state:
        st.session_state[TRAIN_FIGURE_KEY] = None

    if  ACTIVE_CLASSIFIER_KEY not in st.session_state:
        st.session_state[ACTIVE_CLASSIFIER_KEY] = None

    if ACTIVE_RESULTS_KEY not in st.session_state:
        st.session_state[ACTIVE_RESULTS_KEY] = None

    if RESULTS_CSV_KEY not in st.session_state:
        st.session_state[RESULTS_CSV_KEY] = None

# if  not in st.session_state:
#     st.session_state[] =
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def display_classifier() -> None:
    col_fig, col_table = st.columns([1,1])
        
    if st.session_state[TRAIN_TEST_RESULTS_KEY] != None:    
        col_table.table(pd.DataFrame(st.session_state[TRAIN_TEST_RESULTS_KEY]).transpose())
    
    if st.session_state[TRAIN_FIGURE_KEY] != None:
        col_fig.plotly_chart(st.session_state[TRAIN_FIGURE_KEY])  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user_tmp_data_path() -> str:
    return os.path.join(USER_DATA_PATH, st.session_state[USER_CRED_KEY],TMP_USER_DATA_PATH)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user_tmp_classifier_path() -> str:
    return os.path.join(get_user_tmp_data_path(), 'trained-classifier')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user_tmp_highlighted_path() -> str:
    return os.path.join(get_user_tmp_data_path(), 'highlighted')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_data_set() -> str:
    active_data_set_name = 'None'
    
    if st.session_state[ACTIVE_DATA_SET_KEY]:
        active_data_set_name = st.session_state[ACTIVE_DATA_SET_KEY]['name']
    
    return active_data_set_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_classifier_name():
    active_classifier_name = 'None'
    if st.session_state[ACTIVE_CLASSIFIER_KEY]:
        active_classifier_name = st.session_state[ACTIVE_CLASSIFIER_KEY].name
    return active_classifier_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user_cred() -> str:
    if st.session_state[USER_CRED_KEY]:
        return st.session_state[USER_CRED_KEY]
    
    return 'None'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convert_2_data_set() -> DataSet:
    
    data_set = DataSet()
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY]['labels']:
        data_set.labels[label['name']] = label['label-id']
    
    data_list = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text']:
            
            label =  get_label_from_id(labelled_text[LABEL_ID])[LABEL_NAME]            
            data_list.append([label,labelled_text['text']])
    
    data_set.read_data_list(data_list)
            
    return  data_set

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labels() -> list:
    labels = []
    if st.session_state[ACTIVE_CLASSIFIER_KEY]:
        labels = st.session_state[ACTIVE_CLASSIFIER_KEY].get_labels()
        
    return labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_labels() -> list:

    list_of_labels = []

    for label in st.session_state[ACTIVE_DATA_SET_KEY]['labels']:
        list_of_labels.append(label['name'])
               
    return list_of_labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_results(selected_label : str):
    
    for result_dict in st.session_state[TRAIN_TEST_RESULTS_KEY]:
        if result_dict['Label'] == selected_label:
            return result_dict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check_credentials(user_creds : str) -> bool:
    user_path = os.path.join(USER_DATA_PATH, user_creds)    
    return os.path.exists(user_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statement_pdfs() -> list:
    return [os.path.basename(x) for x in glob.glob(PROXY_STATEMENT_PDFS_PATH+'/*.pdf')]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_tmp_file(pdf_file_name : str):
    # build src and dst paths
    src_path = os.path.join(PROXY_STATEMENT_PDFS_PATH, pdf_file_name)
    dst_path = os.path.join(get_user_tmp_highlighted_path(),HIGHLIGHTED_PDF+pdf_file_name)
    
    st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY] = dst_path
    
    # copy file to tmp
    
    try:
        shutil.copy(src_path, dst_path)
        return True
    except FileNotFoundError:        
        st.error(f'[ERRC1] Unable to create tmp files at path: {dst_path}')
        return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    colour = tuple(float(int(value[i:i + lv // 3], 16)/255.) for i in range(0, lv, lv // 3))
    
    return colour

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
def get_results_csv():
    
    result_str = ''
    
    if st.session_state[ACTIVE_RESULTS_KEY]:
        for item in st.session_state[ACTIVE_RESULTS_KEY]:
            file_name = item['filename']
            
            for result in item['results']:
                conf = result['conf'][0]
                label = result['label']
                text = result['text']
                result_str += f'{file_name},{label},{conf},\"{text}\"\n'

    return result_str.encode("utf-8")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



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

def get_data_set_path(data_set_file_name : str):
    data_set_file_path = os.path.join(  USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        data_set_file_name)
    
    if not os.path.exists(data_set_file_path):
        data_set_file_path = os.path.join(PUBLIC_DATA_PATH, data_set_file_name)
        
    return data_set_file_path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_file_from_id(file_id : int) -> dict:
        
    for file_dict in st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements']:
        if file_dict[PROXY_STATEMENT_FILE_ID] == file_id:
            return file_dict

    return {PROXY_STATEMENT_FILENAME : 'Unknown', PROXY_STATEMENT_FILE_ID : -1}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_results_list() -> list:
    
    results_list = []
    
    if st.session_state[ACTIVE_RESULTS_KEY]:
        for item in st.session_state[ACTIVE_RESULTS_KEY]:
            results_list.append(item['filename'])
    
    return results_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_classifiers() -> list:
    
    user_classifier_paths = os.path.join(   USER_DATA_PATH,
                                            st.session_state[USER_CRED_KEY],
                                            PRIVATE_CLASSIFIER_PATH)
    
    user_classifiers = [os.path.basename(x) for x in glob.glob(user_classifier_paths+'/*')]
    
    public_classsifiers = [os.path.basename(x) for x in glob.glob(PUBLIC_CLASSIFIER_PATH+'/*')]
           
    return user_classifiers + public_classsifiers

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statement_json_files() -> list:
    return glob.glob(PROXY_STATEMENT_JSONS_PATH+'/*.json')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def analyze_json_file(json_file_path : str,
                      section_types : list) -> dict:
    
    # get the load classifier
    c = st.session_state[ACTIVE_CLASSIFIER_KEY]
    
    # results of classification will be stored in this dict
    results_dict = {}
    
    json_dict = json.load(open(json_file_path))
    
    results_dict['filename'] = os.path.basename(json_dict['file_path'])
    results_dict['results'] = []
    
    # extract all the text from the given json that needs to be analyzed
    data_list = []
    for page in json_dict['document_pages']:
        for text_block in page['document_text_blocks']:
            if text_block['label'] in section_types:
                for sentence in text_block['sentences']:
                    data_list.append(['UNKNOWN',sentence['text']])
    
    # run the analysis
    if len(data_list) > 0:
        results_dict['results'] = c.classify_list(data_list)
        
    return results_dict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_result(selected_proxy_statement_result : str) -> dict:
        
    for item in st.session_state[ACTIVE_RESULTS_KEY]:

        if item['filename'] == selected_proxy_statement_result:
            return item['results']
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def display_tabs():
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)