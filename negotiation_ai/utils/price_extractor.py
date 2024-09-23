from negotiation_ai.core.llm import llm_math
from negotiation_ai.core.agents import agent_executor
from langchain.prompts import ChatPromptTemplate
import re

def extract_value(human_input, current_price):
    prompt = ChatPromptTemplate.from_messages([
        ("human", """
    Extract and convert Indian numerical values from the given text to a standard number. Return only the numerical result without any additional text. If no numerical value is found, return None.

    Conversion rules:
    - 1 lakh (or lac) = 100,000
    - 10 lakh = 1 million = 1,000,000
    - 1 crore = 10 million = 10,000,000
    - 100 lakh = 1 crore = 10,000,000
    - Handle decimal values (e.g., 1.5 lakh = 150,000)
    - For 'k' or 'thousand', multiply by 1,000

    Examples:
    - "15 lakh" -> 1500000
    - "1 crore" -> 10000000
    - "2.5 lakh" -> 250000
    - "75 thousand" -> 75000
    - "1.5 crore" -> 15000000
    - "100 lakh" -> 10000000
    - "10 crore" -> 100000000
    - "100 crore" -> 1000000000
    - "No number mentioned" -> None
    - "Hello how are you" -> None

    Text to analyze: {human_input}
     
    Important Rules:
    1. Return only the numerical result without any additional text, or None if no number is found.
    2. If there is no numerical value in the text (e.g., "Hello how are you"), the response should be None.
    3. The output should be ONLY the number or None, with no other text or explanation.
    4. Use standard notation for large numbers (e.g., 100000000 instead of 1,00,00,000).
    """)
    ])

    chain = prompt | llm_math
    response = chain.invoke({"human_input": human_input, "current_price": current_price})
    extracted_value = response.content.strip()

    if extracted_value.lower() == 'none':
        # print("No numerical value found in the text. -0=-0=0=-0=-0=")
        if "%" in human_input:
            pattern = r'\d+(\.\d+)?%'
            match = re.search(pattern, human_input)
            if match:
                discount = match.group()
                query = f"Calculate {discount} of {current_price}, subtract that amount from {current_price}, and return the final result.[only return value]."
                result = agent_executor.invoke({"input": query})
                return float(result['output'])
        return None
    else:
        try:
            return float(extracted_value)
        except ValueError:
            return None

# from negotiation_ai.core.llm import llm_math
# from negotiation_ai.core.agents import agent_executor
# from langchain.prompts import ChatPromptTemplate
# import re

# def extract_value(human_input, current_price):
#     prompt = ChatPromptTemplate.from_messages([
#         ("human", """
#     Extract and convert Indian numerical values from the given text to a standard number. Return only the numerical result without any additional text. If no numerical value is found, return None.

#     Conversion rules:
#     - 1 lakh (or lac) = 100,000
#     - 10 lakh = 1 million = 1,000,000
#     - 1 crore = 10 million = 10,000,000
#     - 100 lakh = 1 crore = 10,000,000
#     - Handle decimal values (e.g., 1.5 lakh = 150,000)
#     - For 'k' or 'thousand', multiply by 1,000

#     Examples:
#     - "15 lakh" -> 1500000
#     - "1 crore" -> 10000000
#     - "2.5 lakh" -> 250000
#     - "75 thousand" -> 75000
#     - "1.5 crore" -> 15000000
#     - "100 lakh" -> 10000000
#     - "10 crore" -> 100000000
#     - "100 crore" -> 1000000000
#     - "No number mentioned" -> None
#     - "Hello how are you" -> None

#     Text to analyze: {human_input}
     
#     Important Rules:
#     1. Return only the numerical result without any additional text, or None if no number is found.
#     2. If there is no numerical value in the text (e.g., "Hello how are you"), the response should be None.
#     3. The output should be ONLY the number or None, with no other text or explanation.
#     4. Use standard notation for large numbers (e.g., 100000000 instead of 1,00,00,000).
#     """)
#     ])

#     chain = prompt | llm_math
#     response = chain.invoke({"human_input": human_input, "current_price": current_price})
#     extracted_value = response.content.strip()

#     if extracted_value.lower() == 'none':
#         # Check for percentage discounts
#         percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
#         match = re.search(percentage_pattern, human_input)
#         if match:
#             discount_percentage = float(match.group(1))
#             query = f"Calculate {current_price} - ({discount_percentage}% of {current_price}). Return only the final numeric result."
#             result = agent_executor.invoke({"input": query})
#             try:
#                 return float(result['output'])
#             except ValueError:
#                 return None
        
#         # Check for phrases like "X% off" or "X percent off" or "X% DISCOUNT"
#         off_pattern = r'(\d+(?:\.\d+)?)\s*%?\s*(?:percent|)?\s*(?:off|discount)'
#         match = re.search(off_pattern, human_input.lower())
#         if match:
#             discount_percentage = float(match.group(1))
#             query = f"Calculate {current_price} - ({discount_percentage}% of {current_price}). Return only the final numeric result."
#             result = agent_executor.invoke({"input": query})
#             try:
#                 return float(result['output'])
#             except ValueError:
#                 return None
        
#         return None
#     else:
#         try:
#             return float(extracted_value)
#         except ValueError:
#             return None