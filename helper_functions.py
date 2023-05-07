from credentials import USERNAMES, API_KEY
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI

import os
import time

os.environ["OPENAI_API_KEY"] = API_KEY

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index


def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="default") # default, compact, and tree_summarize
    return response.response


def add_document(user_name, document_name, document_content):
    print(user_name, document_name, document_content)
    # if user_name is empty or not in USERNAMES, return "You are not authorized to add documents!"
    # else, write the document_content to a file in the docs directory
    # then, construct the index
    # finally, return "Document added successfully!"
    if not user_name or user_name not in USERNAMES:
        return "You are not authorized to add documents!"
    else:
        with open(f"docs/{document_name}.txt", "w") as f:
            f.write(document_content)
        construct_index("docs")
        return "Document added successfully!"
    

def delete_document(user_name, document_name):          

    if user_name not in USERNAMES:
        return "You are not authorized to delete documents!"
    else:
        try:
            os.remove(f"docs/{document_name}.txt")
            return "Document deleted successfully!"
        except:
            return "Document does not exist!"
        

def update_document_list():
    document_list = []
    for document in os.listdir("docs"):
        document_list.append(document)
    return document_list