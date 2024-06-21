import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_session_cb(file_name : str,
                    save_type : str) -> None:
    
    # get the output path to save the file too
    output_file_path = os.path.join(PUBLIC_DATA_PATH, file_name+JSON_EXT)
    if save_type == 'private':
        output_file_path = os.path.join(USER_DATA_PATH,
                                        st.session_state[USER_CRED_KEY],
                                        PRIVATE_DATA_SET_PATH,
                                        file_name+JSON_EXT)
   
    # write the activet data set to file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(st.session_state[ACTIVE_DATA_SET_KEY], f, ensure_ascii=False, indent=4)
   
    # check that the file exists
    if os.path.exists(output_file_path):
        st.sidebar.success('Save Sucessful.')
    else:
        st.sidebar.error('Unable to save Data Set.')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_and_review_data_set_page():
    
    if st.session_state[ACTIVE_DATA_SET_KEY] == None:
        st.error('No active Data Set')
    else:
    
        name_col, type_cal = st.sidebar.columns([2,1])
        
        file_name = name_col.text_input('Filename')
        save_type = type_cal.radio( 'Save Type',
                                    options = ['private', 'public'])
        st.sidebar.button(  'Save',
                            on_click=save_session_cb,
                            args=[file_name, save_type])
        
        data_list = []
        
        for labelled_text in st.session_state[ACTIVE_DATA_SET_KEY]['labelled-text']:
            
            label =  get_label_from_id(labelled_text[LABEL_ID])[LABEL_NAME]
            filename = get_file_from_id(labelled_text[PROXY_STATEMENT_FILE_ID])[PROXY_STATEMENT_FILENAME]
            
            data_list.append({  'Label' : label,
                                'Filename' : filename,
                                'Text' : labelled_text['text']})        
        
        df = pd.DataFrame(data_list)
        
        edited_df = st.data_editor(df, use_container_width=True)