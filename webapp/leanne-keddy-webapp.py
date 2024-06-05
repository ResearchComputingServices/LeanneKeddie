import os
import base64
import shutil
import json

import plotly.io as pio
import streamlit as st
import pandas as pd
import glob
from pprint import pprint

from PDFHighlighter import PDFHighlighter
from SentenceClassifier.Classifier import SentenceClassifier
from SentenceClassifier.FineTuner import fine_tune_llm, generate_interactive_plot

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
    
if TRAIN_TEST_RESULTS_KEY  not in st.session_state:
    st.session_state[TRAIN_TEST_RESULTS_KEY] = None

if TRAIN_FIGURE_KEY not in st.session_state:
    st.session_state[TRAIN_FIGURE_KEY] = None

if  ACTIVE_CLASSIFIER_KEY not in st.session_state:
    st.session_state[ACTIVE_CLASSIFIER_KEY] = None

# if  not in st.session_state:
#     st.session_state[] =

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
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

def get_data_set_path(data_set_file_name : str):
    data_set_file_path = os.path.join(  USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        data_set_file_name)
    
    if not os.path.exists(data_set_file_path):
        data_set_file_path = os.path.join(PUBLIC_DATA_PATH, data_set_file_name)
        
    return data_set_file_path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convert_2_csv(data_set_file_name : str) -> str:
    
    data_set_file_path = get_data_set_path(data_set_file_name)
    data_json_dict = json.load(open(data_set_file_path,'r',encoding='utf-8'))
    
    tmp_file_path = os.path.join(USER_DATA_PATH, 
                                 st.session_state[USER_CRED_KEY],
                                 TMP_USER_DATA_PATH,
                                 '.tmp_data_file.csv')
    
    with open(tmp_file_path,'w+') as output_file:
    
        labels_dict = data_json_dict['labels']
        for datum in data_json_dict['labelled-text']:
            text = datum['text']
            label_name = next(label['name'] for label in labels_dict if label["label-id"] == datum['label-id'])
            output_file.write(f'{label_name},\"{text}\"\n')
          
    return tmp_file_path
 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_file_from_id(file_id : int) -> dict:
        
    for file_dict in st.session_state[ACTIVE_DATA_SET_KEY]['proxy-statements']:
        if file_dict[PROXY_STATEMENT_FILE_ID] == file_id:
            return file_dict

    return {PROXY_STATEMENT_FILENAME : 'Unknown', PROXY_STATEMENT_FILE_ID : -1}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_classifiers() -> list:
    
    user_classifier_paths = os.path.join(   USER_DATA_PATH,
                                            st.session_state[USER_CRED_KEY],
                                            PRIVATE_CLASSIFIER_PATH)
    
    user_classifiers = [os.path.basename(x) for x in glob.glob(user_classifier_paths+'/*')]
    
    public_classsifiers = [os.path.basename(x) for x in glob.glob(PUBLIC_CLASSIFIER_PATH+'/*.json')]
       
    return user_classifiers + public_classsifiers

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_proxy_statement_json_files() -> list:
    return glob.glob(PROXY_STATEMENT_JSONS_PATH+'/*.json')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Call Back Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_classifier(selected_classifier : str) -> None:
    
    classifier_path = os.path.join(PUBLIC_CLASSIFIER_PATH,
                                   selected_classifier)    
    
    classifier_loaded = SentenceClassifier()   
    classifier_loaded.load(input_path=classifier_path)
    
    st.session_state[ACTIVE_CLASSIFIER_KEY] = classifier_loaded
    
    training_figure_path = os.path.join(classifier_path,'fig.json')
    
    with open(training_figure_path, 'r') as f:
        st.session_state[TRAIN_FIGURE_KEY] = pio.from_json(f.read())
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

def save_classifier_cb(classifier_name : str) -> None:
    # if the classisifer exsits
    if st.session_state[ACTIVE_CLASSIFIER_KEY]:
        
        output_file_path = os.path.join(PUBLIC_CLASSIFIER_PATH, 
                                        classifier_name)
        
        st.session_state[ACTIVE_CLASSIFIER_KEY].save(output_path=output_file_path)
        
        output_file_path = os.path.join(PUBLIC_CLASSIFIER_PATH, 
                                        classifier_name)
        
        
        st.session_state[TRAIN_FIGURE_KEY].write_json(output_file_path+'/fig.json')
        st.session_state[TRAIN_FIGURE_KEY].write_html(output_file_path+"/fig-file.html")

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

def display_button_cb() -> None:
    print('\n'*100)
    print('~'*80)
    pprint(st.session_state[ACTIVE_DATA_SET_KEY])
    print('~'*80)
    pprint(st.session_state[ACTIVTE_PROXY_STATEMENT_KEY])
    print('~'*80)
    pprint(st.session_state[ACTIVE_LABEL_KEY])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def train_classifier_cb(classifier_name : str,
                        user_selected_model : str,
                        selected_data_set_file : str,
                        train_test_fraction : float) -> None:
    
    # remember to load the data set file into the sessoin state
    load_file_cb(selected_data_set_file)
    
    fine_tuned_model_path = fine_tune_llm(  path_to_data_set=convert_2_csv(selected_data_set_file),
                                            path_to_pretrained_llm=user_selected_model,
                                            num_corrections=10)
    
    c = SentenceClassifier(name = classifier_name,
                           pretrained_transformer_path=fine_tuned_model_path,
                           verbose=True)

    c.set_train_data_path(convert_2_csv(selected_data_set_file))

    c.initialize()
    
    c.train_classifier()
    
    st.session_state[TRAIN_FIGURE_KEY] = c.generate_interactive_plot()
   
    st.session_state[TRAIN_TEST_RESULTS_KEY]  = c.test_classifier(  test_data_path = 'test.csv',
                                                                    test_label =  'COMP_CON',
                                                                    verbose = False)  
    
    st.session_state[ACTIVE_CLASSIFIER_KEY] = c
    
    st.info('Training Complete')
  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Page Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_and_review_data_set_page():
    
    if st.session_state[ACTIVE_DATA_SET_KEY] == None:
        st.error('No active Data Set')
    else:
    
        name_col, type_cal = st.sidebar.columns([2,1])
        
        file_name = name_col.text_input('Filename')
        save_type = type_cal.radio( 'Save Type',
                                    options = ['private', 'public'])
        st.sidebar.button(  'Save',
                            on_click=save_session_cb,
                            args=[file_name, save_type])
        
        data_list = []
        
        for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text']:
            
            label =  get_label_from_id(labelled_text[LABEL_ID])[LABEL_NAME]
            filename = get_file_from_id(labelled_text[PROXY_STATEMENT_FILE_ID])[PROXY_STATEMENT_FILENAME]
            
            data_list.append({'Label' : label,
                            'Filename' : filename,
                            'Text' : labelled_text['text']})        
        
        df = pd.DataFrame(data_list)
        
        edited_df = st.data_editor(df, use_container_width=True)
        
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
                                        options=get_proxy_statement_pdfs(),
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
    selected_file = st.sidebar.selectbox(   label='Data Set Files',
                                            options=get_data_set_files(),
                                            index=None)    
    st.sidebar.button(  'Load',
                        on_click=load_file_cb,
                        args=[selected_file])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def create_data_set_page():
    data_set_name = st.sidebar.text_input('Data Set Name:')
    st.sidebar.button(  'Create',
                        on_click=create_data_set_cb,
                        args=[data_set_name])
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
def train_page():
    
    pretrain_model_options = ['all-MiniLM-L6-v2',
                              'nli-distilroberta-base-v2',
                              'paraphrase-MiniLM-L6-v2']
    
    user_selected_model = st.sidebar.radio('Select Pre-Trained Model', 
                                            options=pretrain_model_options )

    selected_file = st.sidebar.selectbox(   label='Data Set Files',
                                            options=get_data_set_files(),
                                            index=None)
    
    train_test_fraction = st.sidebar.slider(label='Select Training/Testing Fraction',
                                            min_value=0.6,
                                            max_value=1.0,
                                            value = 0.7)
    
    classifier_name = st.sidebar.text_input('Classifier Name')
    
    st.sidebar.button('Train',
                      on_click=train_classifier_cb,
                      args=[classifier_name,
                            user_selected_model,
                            selected_file,
                            train_test_fraction],
                      disabled=((classifier_name == '') or (selected_file == None)))
    
    st.sidebar.button(  'Save',
                        on_click=save_classifier_cb,
                        args=[classifier_name],
                        disabled = (not st.session_state[ACTIVE_CLASSIFIER_KEY]))
    
    col_fig, col_table = st.columns([1,1])
        
    if st.session_state[TRAIN_TEST_RESULTS_KEY] != None:
        col_table.table(st.session_state[TRAIN_TEST_RESULTS_KEY])
    
    if st.session_state[TRAIN_FIGURE_KEY] != None:
        col_fig.plotly_chart(st.session_state[TRAIN_FIGURE_KEY])
 
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
    
    for page in json_dict['document_pages']:
        for text_block in page['document_text_blocks']:
            for sentence in text_block['sentences']:
                label, conf = c.classify(sentence)
                results_dict['results'].append({'sentence' : sentence,
                                                'label' : label,
                                                'conf' : conf})
    return results_dict

def analyze_proxy_statements_cb(section_types : list) -> None:
    proxy_statement_jsons = get_proxy_statement_json_files()
    
    full_results = []
    
    for file_path in proxy_statement_jsons:
        full_results.append(analyze_json_file(file_path,section_types))
        break
    
    pprint(full_results[0])
    input()
    
def classify_page():
    
    selected_classifier = st.sidebar.selectbox('Select Classifier', 
                                                options=get_classifiers())     

    st.sidebar.button('Load',
                      on_click=load_classifier,
                      args=[selected_classifier])
    
    section_types = st.sidebar.multiselect( 'Section Types',
                                            options=[   'Caption', 
                                                        'Footnote', 
                                                        # 'Formula', 
                                                        'List-Item', 
                                                        'Page-footer',
                                                        'Page-header', 
                                                        # 'Picture', 
                                                        'Section-header', 
                                                        # 'Table', 
                                                        'Text',
                                                        'Title'])
    
    st.sidebar.button('Analyze',
                      on_click=analyze_proxy_statements_cb,
                      args=[section_types])
    
    col_fig, col_table = st.columns([1,1])
        
    if st.session_state[TRAIN_TEST_RESULTS_KEY] != None:
        col_table.table(st.session_state[TRAIN_TEST_RESULTS_KEY])
    
    if st.session_state[TRAIN_FIGURE_KEY] != None:
        col_fig.plotly_chart(st.session_state[TRAIN_FIGURE_KEY])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initialize the page
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

st.set_page_config(page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                   layout="wide")

st.sidebar.title('Navigation')  

st.sidebar.button('display',
                  on_click=display_button_cb)

user_page_selection = st.sidebar.radio('Pages', 
                                       options=['Home',
                                                'Create New Data Set',
                                                'Load Data Set',
                                                'Add Data',
                                                'Save / Review',
                                                'Train',
                                                'Classify'],
                                       disabled=(not st.session_state[LOGGED_IN_KEY]))

if user_page_selection == 'Create New Data Set':
    create_data_set_page()
elif user_page_selection == 'Load Data Set':
    load_data_set_page()
elif user_page_selection == 'Add Data':
    add_data_page()
elif user_page_selection == 'Save / Review':
    save_and_review_data_set_page()
elif user_page_selection == 'Train':
    train_page()
elif user_page_selection == 'Classify':
    classify_page()
else:
    home_page()

