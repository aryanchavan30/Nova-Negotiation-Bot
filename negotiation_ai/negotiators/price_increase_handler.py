from negotiation_ai.negotiators.base_negotiator import BaseNegotiator
from negotiation_ai.prompts.templates import price_increase_handler_prompt  
from negotiation_ai.utils.date_utils import get_delivery_date

class PriceIncreaseHandler(BaseNegotiator):
    def __init__(self):
        super().__init__(price_increase_handler_prompt)

    def negotiate(self, data, user_input, current_price, previous_price, language, session_id="demo"):
        inputs = {
            "Product": data['Product'],
            "Quantity": data['Quantity'],
            "Unit_Measure": data['Unit_Measure'],
            "delivery_date": get_delivery_date(),
            "current_price": current_price,
            "previous_price": previous_price,
            "human_input": user_input,
            "language": language
        }
        return super().negotiate(inputs, session_id)