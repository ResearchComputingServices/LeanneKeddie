import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clear_add_data_page():
    st.session_state[PDF_SELECTED_KEY] = False
    st.session_state[ACTIVE_LABEL_KEY] = None
    st.session_state[ACTIVE_PROXY_STATEMENT_KEY] = None
    st.session_state[PDF_HIGHLIGHTER_KEY] = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_file_cb(file_name : str):
    
    data_set_file_path = os.path.join(  USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        file_name)
    
    if not os.path.exists(data_set_file_path):
        data_set_file_path = os.path.join(PUBLIC_DATA_PATH, file_name)
    
    st.session_state[ACTIVE_DATA_SET_KEY] = json.load(open(data_set_file_path))

    st.info(f'Data Set {file_name} Loaded')

    # clear the active pdf and label
    clear_add_data_page()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_data_set_cb(data_set_name : str) -> None:
    # TODO: check if there is a data set with the same name in public or private
    # data folders
    
    st.session_state[ACTIVE_DATA_SET_KEY] = {   'name' :            data_set_name,
                                                'labels' :          [],
                                                'proxy-statements': [],
                                                'labelled-text':    [],
                                                'initialized':      1}
        
    st.info(f'Data Set {data_set_name} Created')

    # clear the active pdf and label
    clear_add_data_page()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_load_data_set_page():
    
    data_set_name = st.sidebar.text_input('Data Set Name:')
    st.sidebar.button(  'Create',
                        on_click=create_data_set_cb,
                        args=[data_set_name],
                        disabled=(data_set_name == ''))
    
    selected_file = st.sidebar.selectbox(   label='Data Set Files',
                                            options=get_data_set_files(),
                                            index=None)    
    st.sidebar.button(  'Load',
                        on_click=load_file_cb,
                        args=[selected_file])