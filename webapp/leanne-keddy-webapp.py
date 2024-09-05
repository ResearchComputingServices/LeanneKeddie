import logging
import sys

import streamlit as st

from utils import *

from home_page import home_page
from create_load_data_set_page import create_load_data_set_page            
from add_data_page import add_data_page
from save_and_review_data_set_page import save_and_review_data_set_page
from train_page import train_page
from classify_page import classify_page
from view_results_page import view_results_page

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initialize the page
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """
    The main entry point for the Definitive A Corporate Proxy Statement Analysis Tool.

    This function initializes the session state, generates a proxy statement manifest, and sets up the Streamlit page
    configuration. It then constructs the sidebar for navigation, displaying the current user credentials, the active
    classifier name, and the active dataset name. The user can navigate through different pages of the application
    depending on their selection from the sidebar radio buttons.

    The function performs the following actions:
    1. Initializes the session state to store application-wide data.
    2. Generates a manifest of proxy statements for analysis.
    3. Sets the Streamlit page configuration with a title and layout.
    4. Constructs the sidebar for navigation, including:
       - Display of the current user credentials.
       - Display of the active classifier name.
       - Display of the active dataset name.
       - A radio button selection for navigating to different pages of the application.
    5. Based on the user's page selection, renders the corresponding page. The options include:
       - 'Home': Renders the home page of the application.
       - 'Create / Load Data Set': Allows the user to create a new dataset or load an existing one.
       - 'Add Data': Provides an interface for adding new data to the dataset.
       - 'Save / Review': Enables saving the current dataset and reviewing saved datasets.
       - 'Train': Offers tools for training the classifier on the dataset.
       - 'Classify': Allows for the classification of new data using the trained classifier.
       - 'View Results': Displays the results of data classification.
    6. Ensures that navigation beyond the home page is disabled unless the user is logged in.

    This function orchestrates the overall flow of the application, ensuring that users can navigate through different
    functionalities based on their authentication status and their intended actions within the tool.
    """
    initialize_session_state()
    generate_proxy_statement_manifest()
    
    st.set_page_config( page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                        layout="wide")

    st.sidebar.title('Navigation')  

    st.sidebar.markdown(f'user creds: {get_user_cred()}')

    st.sidebar.markdown(f'Classifier: {get_active_classifier_name()}')

    st.sidebar.markdown(f'Data Set: {get_active_data_set_name()}')

    user_page_selection = st.sidebar.radio('Pages', 
                                        options=['Home',
                                                    'Create / Load Data Set',
                                                    'Add Data',
                                                    'Save / Review',
                                                    'Train',
                                                    'Classify',
                                                    'View Results'],
                                        disabled=(not st.session_state[LOGGED_IN_KEY]))

    if user_page_selection == 'Create / Load Data Set':
        create_load_data_set_page()
    elif user_page_selection == 'Add Data':
        add_data_page()
    elif user_page_selection == 'Save / Review':
        save_and_review_data_set_page()
    elif user_page_selection == 'Train':
        train_page()
    elif user_page_selection == 'Classify':
        classify_page()
    elif user_page_selection == 'View Results':
        view_results_page()
    else:
        home_page()

if __name__=='__main__':
   
    main()