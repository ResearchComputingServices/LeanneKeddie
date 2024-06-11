import streamlit as st

from utils import *

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

def load_data_set_page():
    selected_file = st.sidebar.selectbox(   label='Data Set Files',
                                            options=get_data_set_files(),
                                            index=None)    
    st.sidebar.button(  'Load',
                        on_click=load_file_cb,
                        args=[selected_file])