import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def save_session_cb(file_name : str,
                    save_type : str) -> None:
    
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