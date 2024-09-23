from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from negotiation_ai.core.llm import llm_math
from negotiation_ai.core.tools import tools

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm_math, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)