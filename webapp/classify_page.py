

import streamlit as st
import plotly.io as pio

from utils import *
from SentenceClassifier.Classifier import SentenceClassifier

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

def load_classifier_cb(selected_classifier : str) -> None:
        
    classifier_path = os.path.join(PUBLIC_CLASSIFIER_PATH,
                                   selected_classifier)    

    classifier_loaded = SentenceClassifier()   
    classifier_loaded.load(input_path=classifier_path)
    
    st.session_state[ACTIVE_CLASSIFIER_KEY] = classifier_loaded
    
    training_figure_path = os.path.join(classifier_path,'fig.json')
    with open(training_figure_path, 'r') as f:
        st.session_state[TRAIN_FIGURE_KEY] = pio.from_json(f.read())
    
    training_results_path = os.path.join(classifier_path,'train_results.json')
    with open(training_results_path, 'r') as f:
        st.session_state[TRAIN_TEST_RESULTS_KEY] = json.load(f)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def analyze_proxy_statements_cb(section_types : list) -> None:
    
    analysis_progress_bar = st.progress(0, text='Preparing Analysis')
    
    proxy_statement_jsons = get_proxy_statement_json_files()
    num_proxy_statements = float(len(proxy_statement_jsons))
    
    full_results = []
    
    for i,file_path in enumerate(proxy_statement_jsons):     
        analysis_progress_bar.progress(i/num_proxy_statements,text=file_path)
        
        results_dict = analyze_json_file(file_path,section_types)    
                    
        full_results.append(results_dict)
        
    st.session_state[ACTIVE_RESULTS_KEY] = full_results
        
    if len(full_results) == len(proxy_statement_jsons):
        st.info(f'Classification Complete.')
        analysis_progress_bar.progress(1.,text=file_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def classify_page():
    
    selected_classifier = st.sidebar.selectbox('Load Classifier', 
                                                options=get_classifiers(),
                                                index=0)     

    st.sidebar.button('Load',
                      on_click=load_classifier_cb,
                      args=[selected_classifier],
                      disabled=(not selected_classifier))
    
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
                      args=[section_types],
                      disabled=(not st.session_state[ACTIVE_CLASSIFIER_KEY] or len(section_types) ==  0))
    
    
    st.sidebar.download_button('Download CSV',
                               data=get_results_csv(),
                               disabled=(not st.session_state[ACTIVE_RESULTS_KEY]),
                               file_name='results.csv')
    
    display_classifier()