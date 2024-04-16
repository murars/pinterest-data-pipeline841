import random
import requests
import json
import logging
from database_utils import AWSDBConnector, just_keep_running
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

new_connector = AWSDBConnector()

@just_keep_running
def start_receiving_post_data_batch():
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    invoke_subdir = "https://ib9giyafm5.execute-api.us-east-1.amazonaws.com/prod/topics/"
    pin_invoke_url = f"{invoke_subdir}0ecac53030fd.pin/"
    geo_invoke_url = f"{invoke_subdir}0ecac53030fd.geo/"
    user_invoke_url = f"{invoke_subdir}0ecac53030fd.user/"
    
    random_row = random.randint(0, 11000) 
    pin_data = new_connector.get_records("pinterest_data", random_row)
    geo_data = new_connector.get_records("geolocation_data", random_row)
    user_data = new_connector.get_records("user_data", random_row)
        
    pin_payload = json.dumps({"records": [{"value": pin_data}]}, default=str)
    pin_response = requests.post(pin_invoke_url, headers=headers, data=pin_payload)
    print('PIN Response:', pin_response.status_code, pin_response.text)

    geo_payload = json.dumps({"records": [{"value": geo_data}]}, default=str)
    geo_response = requests.post(geo_invoke_url, headers=headers, data=geo_payload)
    print('GEO Response:', geo_response.status_code, geo_response.text)

    user_payload = json.dumps({"records": [{"value": user_data}]}, default=str)
    user_response = requests.post(user_invoke_url, headers=headers, data=user_payload)
    print('USER Response:', user_response.status_code, user_response.text)

if __name__ == "__main__":
    print('Working...')
    start_receiving_post_data_batch()