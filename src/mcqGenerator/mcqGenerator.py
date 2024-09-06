# Importing base & system packages
import os
from dotenv import load_dotenv

# Importing packages from langchain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load environment var from the .env file & access it
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

# Configure all the parameters for setup of ChatOpenAI object
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

llm = ChatOpenAI(base_url=endpoint, api_key=api_key, model_name=model_name, temperature=0.8)

# 1st Template for input prompt, generating the quiz based on given parameters & instructions
TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""
# A prompt template of Quiz generation
quiz_generation_prompt = PromptTemplate(input_variables=["text", "number", "subject", "tone", "response_json"],template=TEMPLATE)

# A LLMchain to execute multiple tasks parallely. i.e: llm, prompt (quiz_generation_prompt)
quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

# 2nd Template for evaluating the quiz & its difficulty
TEMPLATE_2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a review of the quiz. Only use at max 50 words for complexity analysis. Do not include anything like corrected mcqs, quiz analysis etc. Just give complexity analysis & review.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
# A prompt template of Quiz evaluation
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE_2)

# A LLMchain to execute multiple tasks parallely. i.e: llm, prompt (quiz_evaluation_prompt)
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Using SequentialChain to run both chain sequentially
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)