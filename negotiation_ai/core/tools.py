from langchain.tools import Tool

def simple_calculator(query: str) -> str:
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

tools = [
    Tool(
        name="Calculator",
        func=simple_calculator,
        description="Use this tool to perform basic mathematical calculations."
    )
]