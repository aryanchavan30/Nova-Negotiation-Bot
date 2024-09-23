import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHAT_MODEL = "llama3-70b-8192"
MATH_MODEL = "llama3-70b-8192"

MAX_PRICE_INCREASE_RATIO = 1.35