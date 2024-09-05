import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clear_add_data_page():
    """
    Resets the session state related to the add data page in a Streamlit application.

    This function clears the session state variables associated with the add data page, effectively resetting the state of the application related to PDF selection, active label, active proxy statement, and PDF highlighter. It is typically used to clear the user's selections and inputs on the add data page, preparing the application for a new session or new data input.

    The function performs the following actions:
    - Sets the PDF_SELECTED_KEY in the session state to False, indicating that no PDF is currently selected.
    - Resets the ACTIVE_LABEL_KEY in the session state to None, clearing any active label selection.
    - Resets the ACTIVE_PROXY_STATEMENT_KEY in the session state to None, clearing any active proxy statement selection.
    - Resets the PDF_HIGHLIGHTER_KEY in the session state to None, clearing any PDF highlighter tool selection.

    This function does not return any value and solely operates on the Streamlit session state.
    """
    st.session_state[PDF_SELECTED_KEY] = False
    st.session_state[ACTIVE_LABEL_KEY] = None
    st.session_state[ACTIVE_PROXY_STATEMENT_KEY] = None
    st.session_state[PDF_HIGHLIGHTER_KEY] = None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def load_file_cb(file_name : str):
    """
    Loads a dataset file into the Streamlit session state and updates the UI to reflect the loaded dataset.

    This function attempts to load a dataset file specified by the user. It first constructs the file path based on the user's credentials and a predefined directory structure for private datasets. If the specified file does not exist in the user's private dataset directory, it falls back to a public dataset directory.

    Parameters:
        file_name (str): The name of the dataset file to be loaded.

    The function performs the following steps:
    1. Constructs the file path for the dataset within the user's private data directory using the user's credentials stored in the session state.
    2. Checks if the file exists at the constructed path. If not, constructs a new path pointing to the public dataset directory.
    3. Loads the dataset from the file into the Streamlit session state under a specific key.
    4. Displays an informational message in the Streamlit UI indicating that the dataset has been successfully loaded.
    5. Calls a function to clear the current state related to PDF selection and labeling, preparing the UI for interaction with the newly loaded dataset.

    This function is designed to handle the loading of dataset files in a multi-user environment, providing access to both private and public datasets based on the user's credentials and the availability of the requested file.
    """
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
# TODO: check if there is a data set with the same name in public or private
# data folders
def create_data_set_cb(data_set_name : str) -> None:
    """
    Creates a new dataset with the specified name and initializes it in the Streamlit session state.

    This function is designed to be used as a callback within a Streamlit application. It initializes a new dataset
    with a given name and a predefined structure, then updates the Streamlit session state with this new dataset.
    Additionally, it clears any active PDF selection and label information, preparing the application for data entry
    into the newly created dataset.

    Parameters:
        data_set_name (str): The name of the dataset to be created.

    The function performs the following steps:
    1. Initializes a new dataset dictionary with the specified name, an empty list of labels, an empty list of proxy
       statements, an empty list of labelled text, and a flag indicating that the dataset has been initialized.
    2. Updates the Streamlit session state with the newly created dataset under a specific key.
    3. Displays an informational message in the Streamlit UI indicating that the dataset has been successfully created.
    4. Calls a function to clear the current state related to PDF selection and labeling, preparing the UI for interaction
       with the newly created dataset.

    This function facilitates the creation of new datasets within the application, allowing users to start the data
    labeling and analysis process with a clean slate.
    """
    
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
    """
    Constructs the page for creating or loading a dataset within a Streamlit application.

    This function generates a user interface in the Streamlit sidebar that allows users to either create a new dataset
    by specifying a name or load an existing dataset from a list of available dataset files. It includes input fields
    and buttons for both creating and loading datasets, with appropriate callbacks for each action.

    The UI components include:
    - A text input field for the user to specify the name of a new dataset to create.
    - A 'Create' button that, when clicked, triggers the creation of a new dataset with the specified name. This button
      is disabled if no name is entered.
    - A select box for choosing an existing dataset file to load. The options for this select box are dynamically
      populated based on the available dataset files.
    - A 'Load' button that, when clicked, triggers the loading of the selected dataset file.

    The function ensures that the 'Create' button is only enabled when a dataset name is entered, and it configures
    the 'Load' button to trigger the dataset loading process with the selected file.

    This function is designed to facilitate the management of datasets within the application, allowing users to easily
    create new datasets or switch between existing datasets for analysis or labeling tasks.
    """
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