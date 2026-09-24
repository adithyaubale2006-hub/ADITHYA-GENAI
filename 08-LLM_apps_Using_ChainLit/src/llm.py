from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

# 1. Import the function instead of the variable
from src.prompt import system_prompt 

def llm_model():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash", 
        api_key=os.environ.get("GEMINI_API_KEY"),
        max_tokens=1000,
        temperature=0.3
    )
    return llm

def ask_order(user_message):
    llm = llm_model()
    
    # 2. Call the function to get the string
    instruction_string = system_prompt()

    # 3. Pass the resulting string into the prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", instruction_string),
        ("human", "{user_input}")
    ])

    chain = prompt_template | llm
    response = chain.invoke({"user_input": user_message})

    return response.content

# --- Example of how it works ---
if __name__ == "__main__":
    reply = ask_order("Hi, I want a pepperoni pizza and some buffalo wings.")
    print(reply)