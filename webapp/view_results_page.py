import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
def view_result_cb(selected_proxy_statement_result : str,
                   view_labels : list):
    
    if st.session_state[ACTIVE_RESULTS_KEY]:
        
        display_result = get_result(selected_proxy_statement_result)
        
        if display_result:
            df = pd.DataFrame(display_result) 
            st.table(df.loc[df['label'].isin(view_labels)])    
        else:
            st.sidebar.error(f'Not Found {selected_proxy_statement_result}')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def view_results_page():
    
    if st.session_state[ACTIVE_RESULTS_KEY] == None:
        st.error('No Results available')
    
    selected_proxy_statement_result = st.sidebar.selectbox( 'Proxy Statement Results',
                                                            options=get_results_list(),
                                                            index=None) 
    
    view_labels = st.sidebar.multiselect(   'Labels',
                                            options=get_labels())
    
    st.sidebar.button('View',
                      on_click=view_result_cb,
                      args=[selected_proxy_statement_result,view_labels])  