import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_data_set_cb(data_set_name : str) -> None:
    # TODO: check if there is a data set with the same name in public or private
    # data folders
    
    st.session_state[ACTIVE_DATA_SET_KEY] = {   'name' :            data_set_name,
                                                'labels' :          [],
                                                'proxy-statements': [],
                                                'labelled-text':    [],
                                                'initialized':      1}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pprint import pprint

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
  
    st.session_state.label_key = ''
        
    pprint( st.session_state[ACTIVE_DATA_SET_KEY]['labels'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_data_set_page():
    data_set_name = st.sidebar.text_input('Data Set Name:')
    st.sidebar.button(  'Create',
                        on_click=create_data_set_cb,
                        args=[data_set_name])
                
    if st.session_state[ACTIVE_DATA_SET_KEY]:
        label_col, colour_col = st.sidebar.columns([3,1])
        
        picked_colour = colour_col.color_picker('Colour')  
        label_name = label_col.text_input('Add Label',key='label_key')
        st.sidebar.button(  'Add',
                            on_click=add_label_cb,
                            args=[label_name,picked_colour])
    
    