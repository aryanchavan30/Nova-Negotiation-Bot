import streamlit as st
from negotiation_ai.negotiators.price_matcher import PriceMatcher
from negotiation_ai.negotiators.price_reducer import PriceReducer
from negotiation_ai.negotiators.high_price_handler import HighPriceHandler
from negotiation_ai.negotiators.price_increase_handler import PriceIncreaseHandler
from negotiation_ai.utils.price_extractor import extract_value 
from negotiation_ai.utils import get_delivery_date
from negotiation_ai.config.settings import MAX_PRICE_INCREASE_RATIO
import time
from datetime import datetime, timedelta

def get_delivery_date():
    return (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

st.markdown(
    """
    <style>
    /* Style the chat input box */
    input::placeholder {
        color: white;
        font-size: 16px;
    }

    div.stTextInput div[data-testid="stTextInput"] > div {
        background-color: #586e75;
        border: 1px solid #d33682;
        border-radius: 10px;
    }

    input {
        color: white;
    }

    /* Move language selector to the top left */
    .block-container {
        display: flex;
        justify-content: flex-start;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Nova: The Only Bot That Can Haggle Better Than Your Aunt!")

    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'vendor_price' not in st.session_state:
        st.session_state.vendor_price = 0
    if 'previous_price' not in st.session_state:
        st.session_state.previous_price = 0

    
    language = st.selectbox("Choose your preferred language:", ["ENGLISH", "HINDI"])

    
    products = [
        {
            'Product': 'Apple iPhone 13 128GB',
            'Quantity': 3,
            'Unit_Measure': 'EA',
            'predicted_value': 52000,
            'Delivery Date': get_delivery_date()
        },
        {
            'Product': 'Samsung Galaxy S23 128GB',
            'Quantity': 5,
            'Unit_Measure': 'EA',
            'predicted_value': 48990,
            'Delivery Date': get_delivery_date()
        },
        {
            'Product': 'Google Pixel 7 128GB',
            'Quantity': 4,
            'Unit_Measure': 'EA',
            'predicted_value': 30500,
            'Delivery Date': get_delivery_date()
        },
        {
            'Product': 'OnePlus 12R 128GB',
            'Quantity': 6,
            'Unit_Measure': 'EA',
            'predicted_value': 39999,
            'Delivery Date': get_delivery_date()
        },
        {
            'Product': 'Samsung Galaxy Z Flip 6 256GB',
            'Quantity': 8,
            'Unit_Measure': 'EA',
            'predicted_value': 109998,
            'Delivery Date': get_delivery_date()
        },
        
        {
            'Product': 'Honor 200 Pro 5G 512GB',
            'Quantity': 5,
            'Unit_Measure': 'EA',
            'predicted_value': 53999,
            'Delivery Date': get_delivery_date()
        },
        
        {
            'Product': 'Vivo X60 128GB',
            'Quantity': 4,
            'Unit_Measure': 'EA',
            'predicted_value': 28450,
            'Delivery Date': get_delivery_date()
        },
        {
            'Product': 'SAMSUNG Galaxy Z Fold6 512GB',
            'Quantity': 7,
            'Unit_Measure': 'EA',
            'predicted_value': 157999,
            'Delivery Date': get_delivery_date()
        }
    ]

    product_names = [product['Product'] for product in products]
    selected_product_name = st.selectbox("Select a product to negotiate:", product_names)


    selected_product = next(product for product in products if product['Product'] == selected_product_name)

    st.write("### Product Details")
    st.table({
        "Product": [selected_product['Product']],
        "Uom": [selected_product['Unit_Measure']],
        "Quantity": [selected_product['Quantity']],
        "Delivery Date": [selected_product['Delivery Date']]
    })

    # Initialize negotiators
    price_matcher = PriceMatcher()
    price_reducer = PriceReducer()
    high_price_handler = HighPriceHandler()
    price_increase_handler = PriceIncreaseHandler()

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for negotiation
    user_input = st.chat_input(f"Enter your offer for {selected_product['Product']}...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            if user_input.lower() in ['exit', 'quit']:
                full_response = "Exiting the negotiation. Goodbye!"
            else:
                extracted_price = extract_value(user_input, st.session_state.vendor_price)

                if extracted_price is not None:
                    st.session_state.previous_price = st.session_state.vendor_price
                    st.session_state.vendor_price = extracted_price

                vendor_price_float = float(st.session_state.vendor_price) if st.session_state.vendor_price is not None else 0
                previous_price_float = float(st.session_state.previous_price) if st.session_state.previous_price is not None else 0

                if vendor_price_float > previous_price_float and previous_price_float != 0:
                    response = price_increase_handler.negotiate(selected_product, user_input, st.session_state.vendor_price, st.session_state.previous_price, language)
                elif vendor_price_float <= float(selected_product['predicted_value']):
                    response = price_matcher.negotiate(selected_product, user_input, st.session_state.vendor_price, language)
                elif float(selected_product['predicted_value']) < vendor_price_float < float((MAX_PRICE_INCREASE_RATIO * selected_product['predicted_value'])):
                    response = price_reducer.negotiate(selected_product, user_input, st.session_state.vendor_price, language)
                elif vendor_price_float >= float((MAX_PRICE_INCREASE_RATIO * selected_product['predicted_value'])):
                    response = high_price_handler.negotiate(selected_product, user_input, st.session_state.vendor_price, language)

                # Simulate streaming effect
                for word in response.split():
                    full_response += word + " "
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)

            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

        if "Purchase Order (PO)" in full_response or "reason for not accepting" in full_response or "Purchase Team" in full_response:
            st.write("Negotiation ended. Goodbye!")
            st.stop()

if __name__ == "__main__":
    main()
