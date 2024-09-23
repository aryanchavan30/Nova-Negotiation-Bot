from datetime import datetime, timedelta

def get_delivery_date():
    return (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")