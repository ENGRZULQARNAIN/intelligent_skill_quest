
# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues


# #############################################################################


import streamlit as st
import ast
import time
from chat import generate_questions,generate_eval_report,format_questions,make_login
from chat import return_auth
def add_user_answer(question_content,given_options,user_picked_option):
    dict={"question_content":question_content,"given_options":given_options,"user_chosed_option":user_picked_option}
    st.session_state.user_answers.append(dict)


def display_question():
    index = st.session_state.rolle_pointer
    try:
        question_key = st.session_state.q_keys[index]
        question_text = st.session_state.questions[question_key]
        
        st.write(question_text)
        
        options_key = st.session_state.q_keys[index + 1] 
        
        if options_key:
            options_str = st.session_state.questions[options_key]
           
            options = options_str.strip("()").replace("'", "").split(", ")
            user_selected_option = st.radio(label="Options", options=options, key=index)
            
            add_user_answer(question_text,options,user_selected_option)
            return user_selected_option
        else:
            return None
    except (IndexError, SyntaxError, ValueError) as e:
        st.error(f"Error displaying question: {e}")
        return None








def initialize_state():

    if 'rolling' not in st.session_state:
        st.session_state.rolling = [i for i in range(10,2)]
    if 'rolle_pointer' not in st.session_state:
        st.session_state.rolle_pointer = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if "user_answers" not in st.session_state:
        st.session_state.user_answers=[]    

def main():
    st.set_page_config(page_title="Home", page_icon=":memo:", layout="centered", initial_sidebar_state="collapsed")
    st.markdown("""
    <style>
    .css-1y4p8pa {
        width: 100%;
        padding: 1rem 1rem 10rem;
        max-width: 46rem;
    }
    .css-1flrh2 {
        position: relative;
        background-color: rgb(10 15 61);
        z-index: 999991;
        min-width: fit-content;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("AI Interviewer")
    st.image("small_logo.png", width=150)
    
    initialize_state()


    if return_auth:
        container = st.container()
        
        if st.session_state.submitted:
            container.header("Questions:")
            if st.session_state.rolle_pointer < len(st.session_state.q_keys) - 1:
                option = display_question()
                if st.button(label="NEXT"):
                    st.session_state.rolle_pointer += 2
                    st.experimental_rerun()
            else:
                st.header("your assesments completed. Thank you for participating!")
                # st.write(str(st.session_state.user_answers))
                st.header("Evaluate your Assesment.")
                pre_question=""
                for question in st.session_state.user_answers:
                    if pre_question!=question["question_content"]:
                        st.write("Question:")
                        st.error(question["question_content"])
                        pre_question=question["question_content"]
                        st.write("Your Answer:")
                        st.success(question["user_chosed_option"])
                eval_button=st.button(label="Evaluate")

                if eval_button:
                    st.session_state.eval_list=[]
                    pre_question1=""
                    for question in st.session_state.user_answers:
                        if pre_question1!=question["question_content"]:
                            pre_question1=question["question_content"]
                            st.session_state.eval_list.append(question)
                    report=generate_eval_report(st.session_state.eval_list)
                    st.write(report)





                    
    
                    

        else:
            container.header("Enter your Professional Information Here!")
            with container.form(key="information"):
                roles = ["Data Scientist", "Web developer", "AI Engineer","Mobile Applcation Developer"]
                skills = ["Python,Machine Learning,Deep learning ", "MERN Stack","MEAN Stack", "Data analysis,Statistics,powerbi,sql", "Django","Flutter, Dart programing language","React Native"]
                experiences = ["<1 year", "1-3 years", "3-5 years", ">5 years"]
                education_levels = ["Bachelor's Degree", "Associate's Degree","Master's Degree", "PhD"]
                
                role = st.selectbox("Role", roles)
                skill = st.selectbox("Skills", skills)
                experience = st.selectbox("Experience", experiences)
                education = st.selectbox("Education Background", education_levels)
                
                submit_button = st.form_submit_button(label="Submit Info")
                
                if submit_button:
                    questions = generate_questions(role, skill, experience, education)
                    formated = format_questions(questions)
                    st.session_state.questions = formated
                    st.session_state.q_keys = list(formated.keys())
                    st.success("Your information submitted successfully!")
                    time.sleep(2)
                    st.session_state.submitted = True
                    st.experimental_rerun()
    else:
        st.header("Login First")

if __name__ == "__main__":
    main()

