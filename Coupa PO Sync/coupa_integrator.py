import requests
import os
import logging

# Retrieve Coupa specific fields related to auth and using API
COUPA_ID = os.getenv("COUPA_ID")
COUPA_INST_ADDR = os.getenv("COUPA_INSTANCE_ADDRESS") 
COUPA_SCOPE = os.getenv("COUPA_SCOPE")
COUPA_SECRET = os.getenv("COUPA_SECRET")

BASE_URL = f"https://{COUPA_INST_ADDR}"
AUTH_ENDPOINT = "/oauth2/token"
PO_ENDPOINT = "/api/purchase_orders"

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define log format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named app.log
        logging.StreamHandler()          # Also log to console
    ]
)
logger = logging.getLogger(__name__)  # Create a logger instance

def get_access_token():
    auth_url = f"{BASE_URL}{AUTH_ENDPOINT}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": COUPA_ID,
        "grant_type": "client_credentials",
        "scope": COUPA_SCOPE,
        "client_secret": COUPA_SECRET
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        response.raise_for_status()

def create_coupa_po(po_id, po_body) -> bool:
    # Authenticate with Coupa API
    try:
        token = get_access_token()
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return False
    
    # Define the URL for PO creation request
    url = f"{BASE_URL}{PO_ENDPOINT}"

    # Define the headers for the POST request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Make the POST request to create PO in Coupa
    try:
        response = requests.post(url, headers=headers, json=po_body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Purchase order {po_id} created successfully: {response.json()}")
        return True
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}. Could not create Purchase Order {po_id} in Coupa")
        return False
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}. Could not create Purchase Order {po_id} in Coupa")
        return False

def update_coupa_po(po_id, po_body):
     # Authenticate with Coupa API
    try:
        token = get_access_token()
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return False
    
    # Define the URL for PO update request
    url = f"{BASE_URL}{PO_ENDPOINT}/{po_id}"

    # Define the headers for the PUT request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Make the PUT request to update PO in Coupa
    try:
        response = requests.put(url, headers=headers, json=po_body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Purchase order {po_id} updated successfully: {response.json()}")
        return True
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}. Could not update Purchase Order {po_id} in Coupa")
        return False
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}. Could not update Purchase Order {po_id} in Coupa")
        return False

def cancel_coupa_po(po_id, po_body):
    # Authenticate with Coupa API
    try:
        token = get_access_token()
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return False
    
    # Define the URL for PO cancel request
    url = f"{BASE_URL}{PO_ENDPOINT}/{po_id}/cancel"

    # Define the headers for the PUT request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Make the PUT request to cancel the PO in Coupa
    try:
        response = requests.put(url, headers=headers, json=po_body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Purchase order {po_id} canceled successfully: {response.json()}")
        return True
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}. Could not cancel Purchase Order {po_id} in Coupa")
        return False
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}. Could not cancel Purchase Order {po_id} in Coupa")
        return False

def close_coupa_po(po_id, po_body):
    # Authenticate with Coupa API
    try:
        token = get_access_token()
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return False
    
    # Define the URL for PO close request
    url = f"{BASE_URL}{PO_ENDPOINT}/{po_id}/close"

    # Define the headers for the PUT request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Make the PUT request to close the PO in Coupa
    try:
        response = requests.put(url, headers=headers, json=po_body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Purchase order {po_id} closed successfully: {response.json()}")
        return True
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}. Could not close Purchase Order {po_id} in Coupa")
        return False
    except requests.RequestException as e:
        logger.error(f"Request exception occurred: {e}. Could not close Purchase Order {po_id} in Coupa")
        return False