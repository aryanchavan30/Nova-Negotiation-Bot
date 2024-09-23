from negotiation_ai.negotiators.base_negotiator import BaseNegotiator
from negotiation_ai.prompts.templates import price_reducer_prompt  
from negotiation_ai.utils.date_utils import get_delivery_date

class PriceReducer(BaseNegotiator):
    def __init__(self):
        super().__init__(price_reducer_prompt)

    def negotiate(self, data, user_input, vendor_price, language, session_id="demo"):
        inputs = {
            "Product": data['Product'],
            "Quantity": data['Quantity'],
            "Unit_Measure": data['Unit_Measure'],
            "delivery_date": get_delivery_date(),
            "predicted_value": data['predicted_value'],
            "vendor_price": vendor_price,
            "human_input": user_input,
            "language": language
        }
        return super().negotiate(inputs, session_id)