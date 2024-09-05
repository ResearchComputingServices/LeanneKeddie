import base64

import streamlit as st

from utils import *

from PDFHighlighter import PDFHighlighter

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
    Callback function to select a file based on its proxy statement name.

    This function updates the session state to reflect the selection of a new file by setting the active page number to 0
    and updating the active proxy statement name to the provided `proxy_statement_name`. After updating the session state,
    it calls `update_displayed_pdf()` to refresh the displayed PDF based on the new selection.

    Parameters:
        proxy_statement_name (str): The name of the proxy statement file to be selected.
    """
def select_file_cb(proxy_statement_name : str) -> None:
    
    st.session_state[ACTIVE_PAGE_NUMBER_KEY] = 0  
    st.session_state[ACTIVE_PROXY_STATEMENT_NAME_KEY] = proxy_statement_name
    
    update_displayed_pdf()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_active_proxy_statement_pdf_file_name() -> str:
    """
    Constructs and returns the file path for the currently active proxy statement PDF page.

    This function calculates the file path of the currently selected proxy statement PDF page by using the active proxy
    statement name and the current page number from the session state. It ensures that the page number in the file path
    is properly zero-padded to maintain a consistent file naming convention (e.g., page_0001.pdf for the first page).

    Returns:
        str: The file path for the currently active proxy statement PDF page.
    """
    # Calculate the number of leading zeros needed to maintain a four-character page number format.
    num_leading_zeros = 4 - len(str(st.session_state[ACTIVE_PAGE_NUMBER_KEY] + 1))
    
    # Retrieve the current page number from the session state.
    page_num = st.session_state[ACTIVE_PAGE_NUMBER_KEY]
    
    # Retrieve the active proxy statement name and its directory path from the session state.
    active_proxy_statement_name = st.session_state[ACTIVE_PROXY_STATEMENT_NAME_KEY]
    active_pdf_dir_path = st.session_state[PROXY_STATEMENTS_KEY][active_proxy_statement_name] 
    
    # Construct the file path for the current page of the active proxy statement PDF.
    active_pdf_file_path = f"{active_pdf_dir_path}/page_{'0'*num_leading_zeros}{page_num + 1}.pdf"
        
    return active_pdf_file_path

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_displayed_pdf() -> None:
    """
    Updates the displayed PDF in the session state with highlights.

    This function retrieves the file name of the currently active proxy statement PDF and attempts to create a temporary
    file for it. If the temporary file is successfully created, it initializes a PDFHighlighter object for the temporary
    file and stores it in the session state. It then checks if the PDF file has previously been highlighted. If so, it
    applies the previous highlights; otherwise, it adds the proxy statement to the dataset for highlighting. Finally, it
    sets a flag in the session state to indicate that a PDF has been selected for display. If the temporary file cannot be
    created, it displays an error message.
    """
    pdf_file_name = get_active_proxy_statement_pdf_file_name()
    
    # create a tmp file for it proxy statement which will be highlighted      
    if create_tmp_file():
    
        # create a PDFHighlighter for the temporary file
        file_path = st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY]
        st.session_state[PDF_HIGHLIGHTER_KEY] = PDFHighlighter(file_path)
        
        # if the file has previously been highlighted apply the highlights
        if check_for_previous_highlights(pdf_file_name):
            apply_previous_highlights()
        else:
            add_proxy_to_data_set(pdf_file_name)
        
        st.session_state[PDF_SELECTED_KEY] = True
    else:
        st.error('ERROR')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def back_cb() -> None:
    """
    Decrements the active page number in the session state and updates the displayed PDF.

    This callback function is designed to navigate to the previous page of the currently active proxy statement PDF.
    It checks if the current active page number is greater than 0, indicating that it's not on the first page. If so,
    it decrements the active page number by 1. If the active page number is already at 0, indicating the first page,
    it displays a warning message stating that the user is at the beginning of the document. After adjusting the page
    number, it calls `update_displayed_pdf()` to refresh the displayed PDF based on the new page number.
    """
    if st.session_state[ACTIVE_PAGE_NUMBER_KEY] > 0:
        st.session_state[ACTIVE_PAGE_NUMBER_KEY] -= 1
    else:
        st.warning('At the beginning of the document')

    update_displayed_pdf()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
def next_cb() -> None:
    """
    Increments the active page number in the session state and updates the displayed PDF.

    This callback function is designed to navigate to the next page of the currently active proxy statement PDF.
    It increments the active page number by 1, then calls `update_displayed_pdf()` to refresh the displayed PDF
    based on the new page number. This allows users to navigate through the document page by page.
    """    
    st.session_state[ACTIVE_PAGE_NUMBER_KEY] += 1
    update_displayed_pdf() 
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def select_label_cb(selected_label : str) -> None:
    """
    Updates the session state with the selected label.

    This callback function is triggered when a label is selected from the UI. It checks if a label has been selected
    (i.e., `selected_label` is not None or an empty string). If a label is selected, it retrieves the label's details
    using `get_label_from_name(selected_label)` and updates the `ACTIVE_LABEL_KEY` in the session state with these details.
    If no label is selected (i.e., `selected_label` is None or an empty string), it sets the `ACTIVE_LABEL_KEY` in the
    session state to None, effectively deselecting any previously selected label.

    Parameters:
        selected_label (str): The name of the label selected from the UI.
    """
    if selected_label:
        st.session_state[ACTIVE_LABEL_KEY] = get_label_from_name(selected_label)
    else:
        st.session_state[ACTIVE_LABEL_KEY] = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_labelled_text_cb(selected_text : str) -> None:
    """
    Adds the selected text as a labelled entry and highlights it in the PDF.

    This callback function is triggered when text is selected for labelling. It first checks if a label has been selected;
    if not, it displays an error message. It then checks if any text has been selected; if not, another error message is displayed.
    After validation, it clears the previously selected text from the text_area widget and uses the active label to highlight
    the selected text in the PDF. The highlighted text is then saved, and the labelled text, along with its metadata (label ID,
    file ID, a unique ID for the text, and the page number), is added to the session's dataset.

    Parameters:
        selected_text (str): The text selected by the user for labelling.
    """    
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
    file_id = st.session_state[ACTIVE_PROXY_STATEMENT_KEY]['file-id']
    
    page_number = st.session_state[ACTIVE_PAGE_NUMBER_KEY]
        
    st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT].append({  'text': selected_text,
                                                                            'label-id' : active_label['label-id'],
                                                                            'file-id' : file_id,
                                                                            'id' : generate_labelled_text_id(),
                                                                            'page_number' : page_number})                                            

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_label_cb(label_name : str,
                 label_colour : str) -> None:    
    """
    Adds a new label to the session's dataset with the specified name and colour.

    This function attempts to add a new label to the active dataset. It first converts the provided hex colour code
    to an RGB colour code. Then, it checks if the label name is unique within the dataset. If it is, the function
    generates a unique label ID, appends the new label (with its name, colour, and ID) to the dataset's labels list,
    and optionally displays an informational message. If the label name already exists in the dataset, it displays
    an error message indicating the duplication.

    Parameters:
        label_name (str): The name of the new label to be added.
        label_colour (str): The hex colour code for the new label.
    """
  
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
    """
    Constructs and displays the data page for a Streamlit application, facilitating the interaction with proxy statements
    and the labeling of text within those documents.

    This function dynamically generates UI components based on the session state, allowing users to:
    - Filter and select proxy statements by year.
    - Select a label for annotating text.
    - Add a new label with a specified name and color.
    - Input or paste text to be labeled and add it to the dataset.
    - Navigate through pages of the selected PDF document and view it within the application.

    The function checks for the existence of an active dataset and a selected PDF document within the session state.
    If an active dataset is present, it enables the functionality for label selection, label addition, and text labeling.
    If a PDF document is selected, it provides navigation controls and displays the document, highlighting labeled text
    if applicable.

    The UI components are primarily located within the Streamlit sidebar, with the PDF document displayed in the main page area.
    This function leverages Streamlit's session state to maintain application state across interactions.

    Raises:
        FileNotFoundError: If the highlighted PDF file path does not exist, indicating an issue with PDF document handling.
    """  
      
    if st.session_state[ACTIVE_DATA_SET_KEY]:
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        with st.sidebar.popover(f'Proxy Statements: {get_active_proxy_statement_name()}'):
            
            year_filter = st.radio('year',
                                    options=['all','2015','2016','2017','2018','2019','labelled'],)
            
            selected_file = st.selectbox(   label='Available Proxy Statements',
                                            options=get_proxy_statement_names(year_filter),
                                            index=None)    
            st.button(  'Select',
                        on_click=select_file_cb,
                        args=[selected_file],
                        disabled=(not selected_file))
        
        select_col, colour_label = st.sidebar.columns([3,1])
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        with select_col.popover(f'Select Label: {get_active_label_name()}'):
             if st.session_state[ACTIVE_DATA_SET_KEY]:
               
                selected_label = st.selectbox(  label='Select Label',
                                                options=get_active_labels(),
                                                index=None) 
                st.button(  'select',
                            on_click=select_label_cb,
                            args=[selected_label] )
        
        colour_label.image(get_active_label_colour_image())
       
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
        with st.sidebar.popover(f'Add Label'):
                
                label_col, colour_col = st.columns([3,1])
    
                picked_colour = colour_col.color_picker('Colour')
                
                label_name = label_col.text_input(  'Add Label')
                
                st.button(  'Add',
                            on_click=add_label_cb,
                            args=[label_name,picked_colour])

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        selected_text = st.sidebar.text_area(label='Selected Text',
                                             key='SELECTED_TEXT_KEY')
        
        st.sidebar.button(  'Add Text',
                            on_click=add_labelled_text_cb,
                            args=[selected_text])
       
    else:
        st.warning('No activate data set')

    # Main Page Widgets
    if st.session_state[PDF_SELECTED_KEY]:
                
        _,prev_col,page_col, next_col,_ = st.columns([5,1,1,1,5])      
               
        prev_col.button( '<-',
                        on_click=back_cb)
                
        page_col.text_input('Page #',
                            value=st.session_state[ACTIVE_PAGE_NUMBER_KEY] + 1)                            
                                     
        next_col.button( '->',
                        on_click=next_cb)
        
        try:      
            with open(str(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY]) , 'rb') as pdf_file:
                base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
                pdf_display =   f"""
                            <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1000px" type="application/pdf"></iframe>
                            """
                st.markdown(pdf_display, unsafe_allow_html=True)   
       
        except FileNotFoundError:
            st.error(f'Directory not found: {str(st.session_state[PDF_HIGHLIGHTED_FILE_PATH_KEY])}') 