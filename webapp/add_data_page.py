import base64

import streamlit as st

from utils import *

from PDFHighlighter import PDFHighlighter

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def select_file_cb(pdf_file_name : str) -> None:

    # create a tmp file for it proxy statement which will be highlighted      
    if create_tmp_file(pdf_file_name):
    
        # create a PDFHighlighter for the temporary file
        st.session_state[PDF_HIGHLIGHTER_KEY] = PDFHighlighter(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY])
        
        # if the file has previously been highlighted apply the highlights
        if check_for_previous_highlights(pdf_file_name):
            apply_previous_highlights()
        else:
            add_proxy_to_data_set(pdf_file_name)
        
        st.session_state[PDF_SELECTED_KEY] = True
    else:
        st.error('ERROR')
       
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def select_label_cb(selected_label : str) -> None:
    
    if selected_label:
        st.session_state[ACTIVE_LABEL_KEY] = get_label_from_name(selected_label)
    else:
        st.session_state[ACTIVE_LABEL_KEY] = None

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
                                                                   'file-id' : file_id,
                                                                   'id' : generate_labelled_text_id()})                                            

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_label_cb(label_name : str,
                 label_colour : str) -> None:    
    
    colour_code = hex_to_rgb(label_colour)
    
    if unique_label(label_name):
        label_id = generate_label_id()
        
        st.session_state[ACTIVE_DATA_SET_KEY]['labels'].append({'name' : label_name, 
                                                                'colour' : colour_code,
                                                                'label-id' : label_id})
        # st.sidebar.info(f'Label "{label_name}" added')
    else:
        st.sidebar.error(f'Label "{label_name}" already exists')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_data_page():   
        
    if st.session_state[ACTIVE_DATA_SET_KEY]:
        with st.sidebar.popover(f'Proxy Statements'):
            
            year_filter = st.radio('year',
                                    options=['all','2015','2016','2017','2018','2019'])
            
            selected_file = st.selectbox(   label='Available Proxy Statements',
                                            options=get_proxy_statement_pdfs(year_filter),
                                            index=None)    
            st.button(  'Select',
                        on_click=select_file_cb,
                        args=[selected_file],
                        disabled=(not selected_file))
        
        with st.sidebar.popover(f'Select Label'):
             if st.session_state[ACTIVE_DATA_SET_KEY]:
               
                selected_label = st.selectbox(  label='Select Label',
                                                options=get_active_labels(),
                                                index=None) 
                st.button(  'select',
                            on_click=select_label_cb,
                            args=[selected_label] )
       
        with st.sidebar.popover(f'Add Label'):
                
                label_col, colour_col = st.columns([3,1])
    
                picked_colour = colour_col.color_picker('Colour')
                
                label_name = label_col.text_input(  'Add Label')
                
                st.button(  'Add',
                            on_click=add_label_cb,
                            args=[label_name,picked_colour])

        selected_text = st.sidebar.text_area(label='Selected Text',
                                             key='SELECTED_TEXT_KEY')
        
        st.sidebar.button(  'Add Text',
                            on_click=add_labelled_text_cb,
                            args=[selected_text])
       
    else:
        st.warning('No activate data set')
    
    # TODO: move this to another function
    # Main Page Widgets
    if st.session_state[PDF_SELECTED_KEY]:
        st.markdown(f'Selected Proxy Statement: {st.session_state[ACTIVTE_PROXY_STATEMENT_KEY][PROXY_STATEMENT_FILENAME]}')
        
        label_col,_ = st.columns([1,10])        
        label_col.color_picker(f'Active Label: {get_active_label_name()}',
                                value=get_active_label_colour(),
                                disabled=True)        
        try:      
            with open(str(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY]) , 'rb') as pdf_file:
                base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
                pdf_display =   f"""
                            <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
                            """
                st.markdown(pdf_display, unsafe_allow_html=True)   
        except FileNotFoundError:
            st.error(f'Directory not found: {str(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY])}') 