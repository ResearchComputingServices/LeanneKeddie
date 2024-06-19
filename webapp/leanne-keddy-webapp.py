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

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

streamlit_root_logger = logging.getLogger(__name__)
streamlit_root_logger.log(level=logging.INFO, msg=f'name: {__name__}')

streamlit_root_logger = logging.getLogger(st.__name__)
if not streamlit_root_logger.hasHandlers():
     streamlit_root_logger.log(level=logging.INFO, msg='App (re)started!')


initialize_session_state()

st.set_page_config(page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                   layout="wide")

st.sidebar.title('Navigation')  

st.sidebar.markdown(f'user creds: {get_user_cred()}')

st.sidebar.markdown(f'Classifier: {get_active_classifier_name()}')

st.sidebar.markdown(f'Data Set: {get_active_data_set_name()}')

user_page_selection = st.sidebar.radio('Pages', 
                                       options=['Home',
                                                'Create/Load Data Set',
                                                'Add Data',
                                                'Save / Review',
                                                'Train',
                                                'Classify',
                                                'View Results'],
                                       disabled=(not st.session_state[LOGGED_IN_KEY]))

if user_page_selection == 'Create/Load Data Set':
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

