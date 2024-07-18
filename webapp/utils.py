import os
import shutil
import json

import streamlit as st

import pandas as pd
import glob
from pprint import pprint

from SentenceClassifier.DataSet import DataSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Dictionary keys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Active Data Set Dict Keys
DATA_SET_PROXY_STATEMENTS = 'proxy-statements'
PROXY_STATEMENT_FILENAME = 'filename'
PROXY_STATEMENT_FILE_ID = 'file-id'

DATA_SET_LABELS = 'labels'
LABEL_NAME = 'name'
LABEL_COLOUR = 'colour'
LABEL_ID = 'label-id'

DATA_SET_LABELLED_TEXT = 'labelled-text'
LABELLED_TEXT_TEXT = "text"
LABELLED_TEXT_FILE_ID = PROXY_STATEMENT_FILE_ID
LABELLED_TEXT_LABEL_ID = LABEL_ID
LABELLED_TEXT_ID = 'id'
DATA_SET_INITIALIZED = 'initialized'

# ExtractedDocument Dict Keys
EXTRACTED_DOCUMENT_FILE_PATH = 'file_path'
EXTRACTED_DOCUMENT_PAGES = 'document_pages'
EXTRACTED_DOCUMENT_TEXT_BLOCKS = 'document_text_blocks'
EXTRACTED_DOCUMENT_TEXT_BLOCK_LABEL = 'label'
EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES = 'sentences'
EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES_TEXT = 'text'

# Results Dict Keys
RESULTS_DICT_FILENAME = 'filename'
RESULTS_DICT_RESULTS = 'results'

# Result Dict Keys
RESULT_TEXT = 'text'
RESULT_LABEL = 'label'
RESULT_CONF = 'conf'

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

#LIST_OF_PROXY_STATEMEMT_YEARS = ['2016','2017','2018','2019','2020','2021','2022']
LIST_OF_PROXY_STATEMEMT_YEARS = ['test']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Session State Keys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOGGED_IN_KEY = 'LOGGED_IN_KEY'
USER_CRED_KEY = 'USER_CRED_KEY'
PDF_SELECTED_KEY = 'PDF_SELECTED_KEY'
PDF_HIGHLIGHTED_FILE_PATH_KEY = 'PDF_HIGHLIGHTED_FILE_PATH_KEY'
PDF_HIGHLIGHTER_KEY = 'PDF_HIGHLIGHTER_KEY'
LABELLED_SENTENCES_KEY = 'LABELLED_SENTENCES_KEY'
TRAIN_TEST_RESULTS_KEY = 'TRAIN_TEST_RESULTS_KEY'
TRAIN_FIGURE_KEY = 'TRAIN_FIGURE_KEY'

# dictionary of proxy statements {base-name : paths}
PROXY_STATEMENTS_KEY = 'PROXY_STATEMENTS_KEY'                   
# dictionary of active data set
ACTIVE_DATA_SET_KEY = 'ACTIVE_DATA_SET_KEY'                     

ACTIVE_PROXY_STATEMENT_KEY = 'PDF_ORIGINAL_FILE_PATH_KEY'
ACTIVE_PAGE_NUMBER_KEY = 'ACTIVE_PAGE_NUMBER_KEY'
ACTIVE_LABEL_KEY = 'ACTIVE_LABEL_KEY'
ACTIVE_CLASSIFIER_KEY = 'ACTIVE_CLASSIFIER_KEY'
ACTIVE_RESULTS_KEY = 'ACTIVE_RESULTS_KEY'
ACTIVE_PROXY_STATEMENT_NAME_KEY = 'ACTIVE_PROXY_STATEMENT_NAME_KEY'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        st.session_state[ACTIVE_DATA_SET_KEY] = None

    if ACTIVE_PROXY_STATEMENT_KEY not in st.session_state:
        st.session_state[ACTIVE_PROXY_STATEMENT_KEY] = {PROXY_STATEMENT_FILENAME : '',
                                                        PROXY_STATEMENT_FILE_ID : -1}

    if ACTIVE_LABEL_KEY not in st.session_state:
        st.session_state[ACTIVE_LABEL_KEY] = None
        
    if TRAIN_TEST_RESULTS_KEY  not in st.session_state:
        st.session_state[TRAIN_TEST_RESULTS_KEY] = None

    if TRAIN_FIGURE_KEY not in st.session_state:
        st.session_state[TRAIN_FIGURE_KEY] = None

    if  ACTIVE_CLASSIFIER_KEY not in st.session_state:
        st.session_state[ACTIVE_CLASSIFIER_KEY] = None

    if ACTIVE_RESULTS_KEY not in st.session_state:
        st.session_state[ACTIVE_RESULTS_KEY] = None

    if PROXY_STATEMENTS_KEY not in st.session_state:
        st.session_state[PROXY_STATEMENTS_KEY] = None

    if ACTIVE_PAGE_NUMBER_KEY not in st.session_state:
        st.session_state[ACTIVE_PAGE_NUMBER_KEY] = 0

    if ACTIVE_PROXY_STATEMENT_NAME_KEY not in st.session_state:
        st.session_state[ACTIVE_PROXY_STATEMENT_NAME_KEY] = None

# if  not in st.session_state:
#   st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                          
def generate_proxy_statement_manifest():
    
    if not st.session_state[PROXY_STATEMENTS_KEY]:
        
        st.session_state[PROXY_STATEMENTS_KEY] = {}
                
        for year in LIST_OF_PROXY_STATEMEMT_YEARS:
            
            dir_path = os.path.join(PROXY_STATEMENT_PDFS_PATH, year)
            list_of_proxy_names = get_proxy_statements_in_dir(dir_path)
            
            for base_name in list_of_proxy_names:          
                proxy_dir_path = os.path.join(dir_path, base_name)
                if base_name not in st.session_state[PROXY_STATEMENTS_KEY]:
                    st.session_state[PROXY_STATEMENTS_KEY][base_name] = proxy_dir_path
                else:
                    print(f'Duplicate Proxy statement found: {proxy_dir_path}')                      
           
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
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

def get_active_label_name():
    active_name = 'None'
    
    if st.session_state[ACTIVE_LABEL_KEY]:
       active_name = st.session_state[ACTIVE_LABEL_KEY][LABEL_NAME]
        
    return active_name  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_label_colour():
    active_colour = '#000000'
    
    if st.session_state[ACTIVE_LABEL_KEY]:
        active_colour = rgb_to_hex(st.session_state[ACTIVE_LABEL_KEY][LABEL_COLOUR])
        
    return active_colour       

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_label_names() -> list:
    
    labels =  []
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        labels.append(label[LABEL_NAME])

    return labels

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_label_from_name(selected_label) -> dict:
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        if label[LABEL_NAME] == selected_label:
            return label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_label_id_from_name(label_name : str) -> int:
    
    label_id = -1
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        if label[LABEL_NAME] == label_name:
            label_id = label[LABEL_ID]

    return label_id

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
def get_label_from_id(label_id : int) -> dict:
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        if label[LABEL_ID] == label_id:
            return label

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def get_label_name_from_id(label_id : int) -> dict:
    
    label_name = 'UNKNOWN'
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        if label[LABEL_ID] == label_id:
            label_name = label[LABEL_NAME]

    return label_name

  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_data_set_name() -> str:
    active_data_set_name = 'None'
    
    if st.session_state[ACTIVE_DATA_SET_KEY]:
        active_data_set_name = st.session_state[ACTIVE_DATA_SET_KEY][LABEL_NAME]
    
    return active_data_set_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_proxy_statement_name() -> str:
    active_proxy_statement_name = 'None'
    
    if st.session_state[ACTIVE_PROXY_STATEMENT_KEY]:
        active_proxy_statement_name = st.session_state[ACTIVE_PROXY_STATEMENT_KEY][PROXY_STATEMENT_FILENAME]
    
    return active_proxy_statement_name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_file_id_from_name(filename : str) -> int:
    
    for file in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_PROXY_STATEMENTS]:
        if file[PROXY_STATEMENT_FILENAME] == filename:
            return file[PROXY_STATEMENT_FILE_ID]
    
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
    
    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        data_set.labels[label[LABEL_NAME]] = label[LABEL_ID]
    
    data_list = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT]:
            
            label =  get_label_from_id(labelled_text[LABEL_ID])[LABEL_NAME]            
            data_list.append([label,labelled_text[LABELLED_TEXT_TEXT]])
    
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

    for label in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]:
        list_of_labels.append(label[LABEL_NAME])
               
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

def get_labelled_proxy_statements() -> list:
    return []

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statements_in_dir(directory_path : str) -> list:
    
    directory_names = []

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            directory_names.append(item)

    return directory_names
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statements_by_years(year_list : list) -> list:
    
    proxy_statements = []
    
    for year in year_list:
        dir_path = os.path.join(PROXY_STATEMENT_PDFS_PATH, year)

        if os.path.exists(dir_path):
            proxy_statements.extend(get_proxy_statements_in_dir(dir_path))

    return proxy_statements

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statement_names(requested_filter : str) -> list:
    
    proxy_statements = []
    
    if requested_filter == 'labelled':
        proxy_statements =  get_labelled_proxy_statements()
    else:
        year_list = [requested_filter]
        if requested_filter == 'all':
            year_list = LIST_OF_PROXY_STATEMEMT_YEARS

        proxy_statements = get_proxy_statements_by_years(year_list)
        
    return proxy_statements
    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_tmp_file():
    
    num_leading_zeros = 4 - len(str(st.session_state[ACTIVE_PAGE_NUMBER_KEY] + 1))
    page_num = st.session_state[ACTIVE_PAGE_NUMBER_KEY]
   
    active_proxy_statement_name = st.session_state[ACTIVE_PROXY_STATEMENT_NAME_KEY]
    active_pdf_dir_path = st.session_state[PROXY_STATEMENTS_KEY][active_proxy_statement_name] 
    
    active_pdf_file_path = f"{active_pdf_dir_path}/page_{'0'*num_leading_zeros}{page_num + 1}.pdf"
 
    # build src and dst paths
    src_path = active_pdf_file_path
    dst_path = os.path.join(get_user_tmp_highlighted_path(),HIGHLIGHTED_PDF+active_proxy_statement_name)
    
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

def rgb_to_hex(rgb_vals):
    r = int(256*rgb_vals[0])
    g = int(256*rgb_vals[1])
    b = int(256*rgb_vals[2])
        
    return '#%02x%02x%02x' % (r,g,b)

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

def generate_labelled_text_id():
    return len(st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT])+1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_label_id() -> int:
    return len(st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_file_id() -> int:
    return len(st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_PROXY_STATEMENTS])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convert_2_df() -> pd.DataFrame:
    data_list = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT]:
                    
        label =  get_label_name_from_id(labelled_text[LABEL_ID])
        filename = get_file_from_id(labelled_text[PROXY_STATEMENT_FILE_ID])[PROXY_STATEMENT_FILENAME]
        
        data_list.append({  'Label' : label,
                            'Filename' : filename,
                            'Text' : labelled_text[LABELLED_TEXT_TEXT],
                            'Delete' : False,
                            'id': labelled_text[LABELLED_TEXT_ID]})        
    
    return pd.DataFrame(data_list)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def unique_label(label_name : str) -> bool:
    
    labels_dict = st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELS]
    
    if any(label[LABEL_NAME] == label_name for label in labels_dict):
        return False
       
    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check_for_previous_highlights(pdf_file_name : str) -> bool:
    
    for statement in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_PROXY_STATEMENTS]:
        if statement[PROXY_STATEMENT_FILENAME] == pdf_file_name:
            st.session_state[ACTIVE_PROXY_STATEMENT_KEY] = statement
            return True
       
    return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_proxy_to_data_set(pdf_file_name : str) -> None:
    
    file_id = generate_file_id()
    
    new_proxy_statement_dict = {PROXY_STATEMENT_FILENAME : pdf_file_name,
                                PROXY_STATEMENT_FILE_ID : file_id}
    
    st.session_state[ACTIVE_PROXY_STATEMENT_KEY] = new_proxy_statement_dict
    
    st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_PROXY_STATEMENTS].append(new_proxy_statement_dict)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_data_set_files():
    
    user_data_sets_path = os.path.join( USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH)
    
    user_data_sets = [os.path.basename(x) for x in glob.glob(user_data_sets_path+'/*.json')]
    
    public_data_sets = [os.path.basename(x) for x in glob.glob(PUBLIC_DATA_PATH+'/*.json')]
       
    return user_data_sets + public_data_sets



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_labelled_text_from_file_id(file_id : int) -> list:
    
    labelled_texts = []
    
    for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT]:
        if labelled_text[PROXY_STATEMENT_FILE_ID] == file_id:
            labelled_texts.append(labelled_text)
        
    return labelled_texts

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def apply_previous_highlights() -> None:
    
    file_id = st.session_state[ACTIVE_PROXY_STATEMENT_KEY][PROXY_STATEMENT_FILE_ID]
    labelled_texts = get_labelled_text_from_file_id(file_id)
    
    for labelled_text in labelled_texts:
    
        label_colour = get_label_from_id(labelled_text[LABELLED_TEXT_LABEL_ID])[LABEL_COLOUR]
        text = labelled_text[LABELLED_TEXT_TEXT]
    
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
        
    for file_dict in st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_PROXY_STATEMENTS]:
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
    
    extract_doc_dict = json.load(open(json_file_path))
    
    results_dict[RESULTS_DICT_FILENAME] = os.path.basename(extract_doc_dict[EXTRACTED_DOCUMENT_FILE_PATH])
    results_dict[RESULTS_DICT_RESULTS] = []
    
    # extract all the text from the given json that needs to be analyzed
    data_list = []
    for page in extract_doc_dict[EXTRACTED_DOCUMENT_PAGES]:
        for text_block in page[EXTRACTED_DOCUMENT_TEXT_BLOCKS]:
            if text_block[EXTRACTED_DOCUMENT_TEXT_BLOCK_LABEL] in section_types:
                for sentence in text_block[EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES]:
                    data_list.append(['UNKNOWN',sentence[EXTRACTED_DOCUMENT_TEXT_BLOCKS_SENTENCES_TEXT]])
    
    # run the analysis
    if len(data_list) > 0:
        results_dict[RESULTS_DICT_RESULTS] = c.classify_list(data_list)
        
    return results_dict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def search_active_data_set(list_name,key, value):
    
    search_results = []
    
    if st.session_state[ACTIVE_DATA_SET_KEY]:    
        search_results= [item for item in st.session_state[ACTIVE_DATA_SET_KEY][list_name] if item.get(key) == value]
        
    return search_results

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_result(selected_proxy_statement_result : str) -> dict:
        
    for item in st.session_state[ACTIVE_RESULTS_KEY]:

        if item['filename'] == selected_proxy_statement_result:
            return item['results']
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def display_classifier() -> None:
    col_fig, col_table = st.columns([1,1])
        
    if st.session_state[TRAIN_TEST_RESULTS_KEY] != None:    
        col_table.table(pd.DataFrame(st.session_state[TRAIN_TEST_RESULTS_KEY]).transpose())
    else:
        st.error('No training results to display')
    
    if st.session_state[TRAIN_FIGURE_KEY] != None:
        col_fig.plotly_chart(st.session_state[TRAIN_FIGURE_KEY]) 
    else:
        st.error('No training figure to display') 
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
