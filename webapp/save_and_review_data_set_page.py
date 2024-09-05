import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_session_cb(file_name : str,
                    save_type : str) -> None:
    """
    Saves the current session data to a JSON file based on the specified save type.

    This function allows saving the active dataset from the session state to a JSON file. The file can be saved in a
    public directory for general access or in a private directory specific to the user, based on the save type
    specified. It provides feedback through the sidebar on the success or failure of the save operation.

    Parameters:
        file_name (str): The name of the file to save the data to. If the file name is empty, a warning is shown.
        save_type (str): The type of save operation ('private' or other). If 'private', the file is saved in a user-
                         specific directory; otherwise, it is saved in a public directory.
    """
    if file_name == '':
        st.sidebar.warning(f'Filename required.')
    else:
        # get the output path to save the file too
        output_file_path = os.path.join(PUBLIC_DATA_PATH, file_name+JSON_EXT)
        if save_type == 'private':
            output_file_path = os.path.join(USER_DATA_PATH,
                                            st.session_state[USER_CRED_KEY],
                                            PRIVATE_DATA_SET_PATH,
                                            file_name+JSON_EXT)    
        # write the activet data set to file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(st.session_state[ACTIVE_DATA_SET_KEY], 
                      f, 
                      ensure_ascii=False, 
                      indent=4)
    
        # check that the file exists
        if os.path.exists(output_file_path):
            st.sidebar.success('Save Sucessful.')
        else:
            st.sidebar.error('Unable to save Data Set.')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_data_set_cb(update_data_frame : pd.DataFrame):
    """
    Updates the active dataset with new labeled texts from a given DataFrame.

    This function iterates through each row of the provided DataFrame, constructing a new list of labeled texts based
    on the data. Rows marked for deletion are skipped. Each remaining row is transformed into a dictionary containing
    the text's ID, label ID, file ID, and text content, which are then appended to a new list. This list replaces the
    existing list of labeled texts in the active dataset stored in the session state.

    Parameters:
        update_data_frame (pd.DataFrame): A DataFrame containing the updated dataset information. Expected columns
                                          include 'Delete', 'id', 'Label', 'Filename', and 'Text'. The 'Delete' column
                                          is a boolean indicating whether the row should be ignored.

    """
    new_labelled_texts = []

    for row in update_data_frame.iloc:

        if row['Delete']:
            continue
        
        new_labelled_texts.append({ 'id': int(row['id']),
                                    'label-id': get_label_id_from_name(row['Label']),
                                    'file-id': get_file_id_from_name(row['Filename']),
                                    'text': row['Text']})
        
    st.session_state[ACTIVE_DATA_SET_KEY][DATA_SET_LABELLED_TEXT] = new_labelled_texts
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_and_review_data_set_page():
    """
    Displays a page for saving and reviewing the active dataset within a Streamlit application.

    This function provides an interface for users to save the current active dataset and review its contents. It
    includes input fields for specifying the file name and save type (private or public), and displays the dataset in
    an editable table format. Users can save the dataset with the specified settings and update the dataset based on
    modifications made in the table.

    The function first checks if there is an active dataset. If not, it displays an error message. Otherwise, it
    proceeds to render the save and review interface, including:
    - A text input for the file name, pre-filled with the active dataset's name.
    - A radio button selection for the save type (private or public).
    - A 'Save' button that triggers the saving of the dataset.
    - An editable table displaying the dataset, allowing for modifications.
    - An 'Update' button to apply changes made in the table to the active dataset.
    """
    
    if st.session_state[ACTIVE_DATA_SET_KEY] == None:
        st.error('No active Data Set')
    else:
    
        name_col, type_cal = st.sidebar.columns([2,1])
        
        file_name = name_col.text_input('Filename',
                                        value=get_active_data_set_name())
        
        save_type = type_cal.radio( 'Save Type',
                                    options = ['private', 'public'])
        st.sidebar.button(  'Save',
                            on_click=save_session_cb,
                            args=[file_name, save_type])
            
        edited_df = st.data_editor(convert_2_df(), 
                                   use_container_width=True,
                                   hide_index=True,
                                   disabled=["Proxy Statement"],
                                   column_config={"Label" : st.column_config.SelectboxColumn("Label", options=get_label_names()),
                                                  'id': None,
                                                  'Filename': None})
        
        st.button(label='Update',
                  on_click=update_data_set_cb,
                  args=[edited_df])