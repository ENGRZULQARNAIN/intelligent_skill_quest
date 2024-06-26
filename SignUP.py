# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues

##########################################################################



import streamlit as st

from auth_helpers import create_connection, create_table, create_user, authenticate_user



db_file = 'users.db'
conn = create_connection(db_file)
create_table(conn)

st.title("AI interviewer")
col1,col2=st.columns([0.2,0.8])


def load_page(page_name):
    page_path = f"{page_name}.py"
    with open(page_path, "r") as file:
        code = file.read()
        exec(code, globals())

with col2:
    

# Page title
    st.header("Sign Up")

    # Form for user sign-up
    with st.form(key='signup_form'):
        st.image("small_logo.png", width=150)
        email = st.text_input('Email', placeholder="Enter your email")
        password = st.text_input('Password', type='password', placeholder="Enter your password")
        confirm_password = st.text_input('Confirm Password', type='password', placeholder="Confirm your password")
        
        # Submit button
        submit_button = st.form_submit_button(label='Sign Up')

        # Form submission logic
        if submit_button:
            if password == confirm_password:
                create_user(conn, email, password)
                st.success(f"Account created successfully for {email}!")
                
            else:
                st.error("Passwords do not match. Please try again.")

