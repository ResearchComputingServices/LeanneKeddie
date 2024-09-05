

import streamlit as st
import plotly.io as pio

from utils import *
from SentenceClassifier.Classifier import SentenceClassifier

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

def load_classifier_cb(selected_classifier : str) -> None:
    """
    Loads a specified classifier and its associated training data into the Streamlit session state.

    This function is designed to be used as a callback within a Streamlit application. It loads a classifier model
    from a specified path and updates the Streamlit session state with the loaded classifier and its training data.
    The training data includes both a figure representing the training process and the training results.

    Parameters:
        selected_classifier (str): The name of the classifier to be loaded. This name is used to locate the classifier
        and its associated data within a predefined directory structure.

    The function performs the following steps:
    1. Constructs the path to the selected classifier based on a predefined base path and the name of the classifier.
    2. Initializes a new SentenceClassifier instance and loads the classifier from the constructed path.
    3. Updates the Streamlit session state with the loaded classifier.
    4. Loads the training figure and training results from their respective JSON files located in the classifier's directory.
    5. Updates the Streamlit session state with the loaded training figure and training results.

    The loaded classifier, training figure, and training results are stored in the session state under specific keys,
    allowing other parts of the Streamlit application to access and display this information.
    """
        
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
    """
    Analyzes proxy statement documents based on specified section types and updates the Streamlit session state with the results.

    This function iterates over a collection of proxy statement JSON files, analyzes each based on the provided section types,
    and aggregates the results. It utilizes a progress bar to visually indicate the progress of the analysis to the user.

    Parameters:
        section_types (list): A list of section types to analyze within the proxy statements. These types guide the analysis
        process, determining which sections of each document are analyzed.

    The function performs the following steps:
    1. Initializes a progress bar in the Streamlit UI to indicate the start of the analysis process.
    2. Retrieves a list of file paths for the proxy statement JSON files to be analyzed.
    3. Iterates over each file path, updating the progress bar with the current progress and the file being analyzed.
    4. For each file, calls a function to analyze the document based on the specified section types and collects the results.
    5. Updates the Streamlit session state with the aggregated results of the analysis.
    6. Upon completion of the analysis for all documents, displays a completion message and sets the progress bar to 100%.

    The aggregated results of the analysis are stored in the Streamlit session state under a specific key, allowing other
    parts of the application to access and display the analysis results.
    """
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
    """
    Constructs the classification page for a Streamlit application, enabling users to load classifiers, select section types for analysis, and analyze proxy statements.

    This function generates a user interface in the Streamlit sidebar that allows users to:
    - Load a classifier from a list of available classifiers.
    - Select multiple section types that will be considered during the analysis of proxy statements.
    - Initiate the analysis of proxy statements based on the selected classifier and section types.
    - Download the results of the analysis as a CSV file.

    The function also displays the currently loaded classifier's information on the main page.

    The UI components include:
    - A select box for choosing a classifier to load.
    - A button to load the selected classifier, which triggers a callback function to handle the loading process.
    - A multi-select box for users to choose which section types of the proxy statements they want to analyze.
    - An 'Analyze' button that, when clicked, triggers the analysis of proxy statements based on the selected section types and loaded classifier.
    - A 'Download CSV' button that allows users to download the results of the analysis.

    The function ensures that the 'Load' and 'Analyze' buttons are only enabled when appropriate selections have been made by the user. It also conditionally enables the 'Download CSV' button based on whether analysis results are available in the session state.

    This function is designed to facilitate the interaction between the user and the application, streamlining the process of classifier selection, section type specification, document analysis, and result retrieval.
    """
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