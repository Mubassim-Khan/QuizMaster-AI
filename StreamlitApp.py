import json
import pandas as pd
import traceback

from src.mcqGenerator.utils.readFiles import read_file
from src.mcqGenerator.utils.getTableData import get_table_data

import streamlit as st
from PIL import Image

from langchain_community.callbacks.manager import get_openai_callback
from src.mcqGenerator.mcqGenerator import generate_evaluate_chain

# load json response file for the response to be in that format
with open(r'response.json','r') as file:
    RESPONSE_JSON = json.load(file)

# Set the title & favicon of the tab
favicon = Image.open("data/logo.png")
st.set_page_config(page_title="QuizMaster AI", page_icon = favicon, initial_sidebar_state = 'auto')

st.write("Streamlit version:", st.__version__)

# Title for the app
st.title("QuizMaster AI")

# Cover line for the app
st.write("An AI-powered app built using GPT-4o, Langchain, Streamlit & Pandas to generate dynamic MCQs from user-provided documents.")

# Create a form using st.form
with st.form("user_inputs"):
    # file upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # subject
    subject = st.text_input("Insert Subject", max_chars=30)

    # Difficulty
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    # Add button
    button = st.form_submit_button("Generate MCQs")

    # check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(uploaded_file)

                # count token and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("An Error occured")
            
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                print(response)
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)

                    if quiz and quiz.startswith('```json\n'):
                        quiz = quiz.strip('```json\n')

                        if quiz:

                            if isinstance(quiz, str) and quiz.strip():
                                table_data = get_table_data(quiz)

                                if table_data:
                                    df = pd.DataFrame(table_data)
                                    df.index = df.index + 1
                                    st.table(df)
                                    # Formating the review text
                                    review_text = response["review"].replace("###", "").replace("**", "").replace("***", "")
                                    st.text_area(label="Review", value=review_text, height=150)
                                else:
                                    st.error("Error in the table data")
                            else:
                                st.error("Quiz is none")
                        else:
                            st.write(response)
