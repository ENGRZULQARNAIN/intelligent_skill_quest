# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues
############################################################################


import streamlit as st

def show_single_question(question):
    st.write("what is science")
    option = st.radio('How would you like to be contacted?',('Email', 'Home phone', 'Mobile phone'))


def all_question(questions):
    question_no=0
    