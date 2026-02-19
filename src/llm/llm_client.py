import os 
import json
from groq import Groq 
from dotenv import load_dotenv
import logging 

load_dotenv()


class LLMClient:
    def __init__(self):
        api_key= os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("ROQ_API_KEY not found in environment variables.")
        
        self.client= Groq(api_key)
        