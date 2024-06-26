# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues

############################################################################
import streamlit as st
from auth_helpers import create_connection, create_table, create_user, authenticate_user
# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Set up page
st.set_page_config(page_title="Sign Up", page_icon=":memo:", layout="centered")
st.title("AI Interviewer")

# Set up database
db_file = 'users.db'
conn = create_connection(db_file)
create_table(conn)
from chat import make_login
def main():
    # Create columns for centering the content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Login")
        with st.form(key="login"):
            st.image("small_logo.png", width=300)

            # Input fields for username and password
            username = st.text_input("Email or Username")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button(label='Log In')

            # Login button
            if submit_button:
                if authenticate_user(conn, username, password):
                    st.session_state.username = username
                    st.session_state.authenticated = True
                    make_login(True)
                    st.success("Logged in successfully!")
                else:
                    st.error("Incorrect Username or Password")

if __name__ == "__main__":
    main()

def is_authenticated():
    return st.session_state.authenticated
