from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()





def get_model(model="openai/gpt-oss-20b"):
    return ChatGroq(
        model=model,
        temperature=0,
        max_tokens=700,
        timeout=30,
        max_retries=1,
    )