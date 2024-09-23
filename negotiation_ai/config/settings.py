import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHAT_MODEL = "llama-3.1-70b-versatile"
MATH_MODEL = "llama-3.1-70b-versatile"

MAX_PRICE_INCREASE_RATIO = 1.35