# author: Zulqar Nain
# date: 12-june-2024
# project SkillQues

############################################################################




from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv,find_dotenv 
load_dotenv()
import streamlit as st


os.environ["GOOGLE_API_KEY"]= st.secrets['GOOGLE_API_KEY']
# os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
def create_response_schema():
     response_schemas=[]
     for i in range(10):
        response_schemas.append(ResponseSchema(name=f"Question {i+1}", description=f"its is the text Question {i+1} only"))
        response_schemas.append(ResponseSchema(name=f"Options for question {i+1}", description=f"this is the all  options for question {i+1} , please write in such format in python set format like (option1,option2,.....option)"))

     return response_schemas



llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def format_questions(questions):

    output_parser = StructuredOutputParser.from_response_schemas(create_response_schema())
    format_instructions = output_parser.get_format_instructions()
    parser_prompt = PromptTemplate(
        template=" the given is the questions with options.\n{format_instructions}\n questions:{questions}\n",
        input_variables=["questions"],
        partial_variables={"format_instructions": format_instructions},
    )
    parser_chain = parser_prompt | llm | output_parser

    questions_dict=parser_chain.invoke({"questions":questions})

    return questions_dict



template="""

As the Chief Technology Officer (CTO) of a Software Company, you have been assigned the task of recruiting candidates for the role of {role}. 
In order to evaluate the suitability of the candidates, you will be conducting interviews that focus on their skills {skills}, years of experience {experience}, and educational background {education}. 
To aid in this process, you are required to create 10 multiple-choice questions that are tailored to each candidate's profile.

These questions should directly align with the candidate's skills, experience, and education, and should avoid being theoretical in nature. Instead, the questions should be practical and relevant to the specific role the candidate is being considered for. 
For example, if a candidate possesses skills in Python, has 2 years of experience, and holds a degree in Computer Science, a suitable question could be: "What is GIL in Python? (a) I don't know (b) GIL is called Global Interpreter Lock. (c) GIL is an abbreviation for fish gills. (d) none of the above."

Please provide your responses in a structured manner, ensuring that they are clear, concise, and directly related to the candidate's qualifications. This will help to enhance readability and ensure that the questions effectively assess the candidate's suitability for the role. 
MCQs:

1. What is GIL in Python?  
   (a) I don't know  
   (b) GIL is called Global Interpreter Lock.  
   (c) GIL is an abbreviation for fish gills.  
   (d) none of the above  

2. In which year was Python 3.0 released?  
   (a) 2005  
   (b) 2008  
   (c) 2010  
   (d) 2012  

3. Which of the following data structures does Python provide?  
   (a) List  
   (b) Tuple  
   (c) Dictionary  
   (d) All of the above  

4. How do you start a function in Python?  
   (a) function functionName()  
   (b) def functionName():  
   (c) func functionName()  
   (d) define functionName()  

5. What does PEP stand for in Python?  
   (a) Python Enhancement Proposal  
   (b) Python Enrichment Proposal  
   (c) Python Extension Proposal  
   (d) Python Example Proposal  

6. What is the purpose of the "self" keyword in Python?  
   (a) It refers to the current instance of the class  
   (b) It is used to define a static method  
   (c) It is a global variable  
   (d) None of the above  

7. Which of the following is used to handle exceptions in Python?  
   (a) try and except  
   (b) catch and throw  
   (c) do and while  
   (d) if and else  

8. What is the output of the following code: print("Hello World"[::-1])?  
   (a) Hello World  
   (b) dlroW olleH  
   (c) Error  
   (d) None of the above  

9. What is a lambda function in Python?  
   (a) A function that returns a generator  
   (b) An anonymous function  
   (c) A named function  
   (d) A recursive function  

10. What is the result of the following code: len([1, 2, 3])?  
    (a) 1  
    (b) 2  
    (c) 3  
    (d) None of the above  
"""


import re

def clean_text(text):
    # Define the pattern to remove # and *
    pattern = r'[#$*]'
    
    # Use re.sub() to replace the characters with an empty string
    clean_text = re.sub(pattern, '', text)
    
    return clean_text


question_prompt=PromptTemplate(template=template,input_variables=["role","skills","experience","education"])
chain=LLMChain(prompt=question_prompt,llm=llm)


def generate_questions(role,skills,experience,education):
    ans=chain.invoke({"role":role,"skills":str(skills),"experience":str(experience),"education":str(education)})
#     ans=clean_text(ans)
    return str(ans["text"])


evaluate_template="""
As the Chief Technology Officer (CTO), your objective is to review and assess a set of 10 user-submitted questions along with their corresponding answers.
Each question is linked to the user's chosen option and the available question options. Your task is to compile a report detailing the total number of correct and incorrect answers, such as:

Total correct answers: 8 out of 10
Total incorrect answers: 2 out of 10

If the results are commendable, provide a brief appreciation. Identify any weaknesses in the candidate based on their answers.

User submitted answers: {user_answers}
Please answer in a structured way to enhance readability.

ANSWER:

Report:
Total correct answers: 8 out of 10
Total incorrect answers: 2 out of 10
Appreciation:
Great job! Your performance is impressive, with a high accuracy rate demonstrating a strong understanding of the subject matter.

Weak Points:

Review the areas where incorrect answers were given to identify specific topics that need further study.
Pay attention to the details of each question to avoid minor mistakes.

only mention the weak points not explain it in detail.
not discuss each question in the report only gives a concise report
Try to gives whole report concise and clear.

"""

eval_prompt=PromptTemplate(template=evaluate_template,input_variables=["user_answers"])
eval_chain=LLMChain(prompt=eval_prompt,llm=llm)

def generate_eval_report(user_answers):
    res=eval_chain.invoke({"user_answers":str(user_answers)})
    return res["text"]


Auth=False

def make_login(flag):
    if flag:
        Auth=True

def return_auth():
    return Auth

