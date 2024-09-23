from langchain_groq import ChatGroq
from negotiation_ai.config.settings import GROQ_API_KEY, CHAT_MODEL, MATH_MODEL

llm_chat = ChatGroq(
    temperature=0.1,
    model=CHAT_MODEL,
    api_key=GROQ_API_KEY
)

llm_math = ChatGroq(
    temperature=0,
    model=MATH_MODEL,
    api_key=GROQ_API_KEY
)