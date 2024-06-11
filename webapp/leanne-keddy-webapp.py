

import streamlit as st

from utils import *

from home_page import home_page
from create_data_set_page import create_data_set_page
from load_data_set_page import load_data_set_page            
from add_data_page import add_data_page
from save_and_review_data_set_page import save_and_review_data_set_page
from train_page import train_page
from classify_page import classify_page
from view_results_page import view_results_page

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# initialize the page
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

initialize_session_state()

st.set_page_config(page_title="Definitive A Corporate Proxy Statement Analysis Tool",
                   layout="wide")

st.sidebar.title('Navigation')  

st.sidebar.markdown(f'user creds: {get_user_cred()}')

st.sidebar.markdown(f'Classifier: {get_active_classifier_name()}')

user_page_selection = st.sidebar.radio('Pages', 
                                       options=['Home',
                                                'Create New Data Set',
                                                'Load Data Set',
                                                'Add Data',
                                                'Save / Review',
                                                'Train',
                                                'Classify',
                                                'View Results'],
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
elif user_page_selection == 'View Results':
    view_results_page()
else:
    home_page()

