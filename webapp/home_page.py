
import streamlit as st

import utils

def home_page():
    """
    Renders the home page of the Keddie Tool application in a Streamlit interface.

    This function sets up the home page for the Keddie Tool, a web application designed for supervised topic modeling
    of DEF 14A documents filed by S&P 500 corporations from 2016 to 2022. It provides a brief description of the tool,
    displays contact information for access requests, and implements a sign-in mechanism for user authentication.

    The function performs the following actions:
    1. Displays the title of the application ("Keddie Tool") at the top of the page.
    2. Provides a markdown description of the tool's purpose and its specific focus on DEF 14A documents.
    3. Displays contact information for users to request access to the tool.
    4. Includes a text input field for users to enter their credentials.
    5. Implements a 'Sign In' button that triggers a credential check when clicked:
       - If the credentials are invalid or the input field is empty, it displays an error message and sets a session state
         variable to indicate that the user is not logged in.
       - If the credentials are valid, it displays a success message in the sidebar, updates the session state to reflect
         that the user is logged in, stores the user's credentials in the session state, and triggers a rerun of the
         Streamlit app to reflect the user's logged-in status.

    This home page serves as the entry point to the application, ensuring that only users with valid credentials can
    access the tool's features.
    """
    st.title("Keddie Tool")
    st.markdown("""This tool enables supervised topic modelling of form DEF 14A 
                (Definitive Proxy Statement) filed by S&P500 corportations between
                the years of 2016 and 2022.""")
    
    st.markdown("To gain access please contact: rcs@cunet.carleton.ca")
    
    user_creds = st.text_input(label = "User Credentials")
    
    if st.button('Sign In'):       
        if not check_credentials(user_creds) or user_creds == '':
            st.error('User Credentials not found.')
            st.session_state[LOGGED_IN_KEY] = False
        else:
            st.sidebar.success('Sign-In successful')
            st.session_state[LOGGED_IN_KEY] = True
            st.session_state[USER_CRED_KEY] = user_creds
            st.rerun()