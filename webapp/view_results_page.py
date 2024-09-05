import streamlit as st

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
def view_result_cb(selected_proxy_statement_result : str,
                   view_labels : list):
    """
    Displays a table of results filtered by specified labels for a selected proxy statement result.

    This function is designed to display a subset of results from a larger dataset based on user-selected labels. It
    first checks if there are active results stored in the session state. If active results exist, it retrieves the
    specific result set associated with the selected proxy statement. If the result set is found, it filters the results
    based on the specified labels and displays them in a table format. If the specified result set is not found, it
    displays an error message in the sidebar.

    Parameters:
        selected_proxy_statement_result (str): The identifier for the proxy statement result to be displayed.
        view_labels (list): A list of labels used to filter the results to be displayed.

    """
    if st.session_state[ACTIVE_RESULTS_KEY]:
        
        display_result = get_result(selected_proxy_statement_result)
        
        if display_result:
            df = pd.DataFrame(display_result) 
            st.table(df.loc[df['label'].isin(view_labels)])    
        else:
            st.sidebar.error(f'Not Found {selected_proxy_statement_result}')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def view_results_page():
    """
    Renders a page in a Streamlit app for viewing results based on selected criteria.

    This function creates a user interface for selecting a specific set of results (identified by proxy statements)
    and filtering these results by labels. It checks if there are any results available in the session state. If not,
    it displays an error message. Otherwise, it allows the user to select a result set and labels for filtering. A
    'View' button is provided to trigger the display of the filtered results.

    The page layout includes:
    - A check for the availability of results. If no results are available, an error message is displayed.
    - A dropdown to select a proxy statement result from the available list.
    - A multi-select box to choose one or more labels for filtering the results.
    - A 'View' button to display the results based on the selected proxy statement and labels.
    """
    
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