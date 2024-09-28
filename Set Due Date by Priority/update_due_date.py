import requests
from datetime import datetime

# Function to update work order due date via MaintainX API
# Returns True if successfully updated, False otherwise
def update_work_order_due_date(work_order_id: int, new_due_date: datetime, update_url: str, token: str, logger) -> bool: 
    headers = {
        'Accept': 'application/json',  # Accept JSON response
        'Authorization': f'Bearer {token}',  # Authorization header with Bearer token
        'Content-Type': 'application/json'  # Content type is JSON
    }
    payload = {
        "dueDate": new_due_date  # Payload with the new due date
    }
    try:
        response = requests.request("PATCH", update_url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Successfully updated work order {work_order_id} with new due date {new_due_date}")
        return True
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
    return False