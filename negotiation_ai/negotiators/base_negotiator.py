from langchain_core.runnables.history import RunnableWithMessageHistory
from negotiation_ai.core.llm import llm_chat
from negotiation_ai.utils.session_manager import get_session_history

class BaseNegotiator:
    def __init__(self, prompt_template):
        self.chain = prompt_template | llm_chat
        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,
            get_session_history,
            input_messages_key="human_input",
            history_messages_key="history",
        )

    def negotiate(self, inputs, session_id="demo"):
        response = self.runnable_with_history.invoke(
            inputs,
            config={"configurable": {"session_id": session_id}}
        )
        return response.content