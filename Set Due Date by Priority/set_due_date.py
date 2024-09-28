import requests
import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from update_due_date import update_work_order_due_date
from priority_logic import calc_due_date

# Initialize Constants
TOKEN = os.getenv("token")  # Retrieve the API token from environment variables
BASE_URL = "https://api.sandbox.getmaintainx.com/v1"  # Base URL for the API
WORK_ORDERS = "workorders"  # Endpoint for work orders

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

# Main functionality that updates a work order due date when called
def set_due_date_by_priority(work_order_id: int, work_order_priority: str) -> Tuple[bool, Optional[datetime]]:
    logger.info(f"Setting due date for work order {work_order_id} with priority {work_order_priority}")

    # Calculate due date based on priority
    due_date = calc_due_date(work_order_priority)
    if due_date is None:
        logger.warning(f"Invalid priority '{work_order_priority}' provided for work order {work_order_id}")
        return False, None

    # Build URL for updating the work order due date
    update_url = f"{BASE_URL}/{WORK_ORDERS}/{work_order_id}"
    logger.debug(f"Update URL: {update_url}")

    # Attempt to update the work order due date
    update_success = update_work_order_due_date(work_order_id, due_date, update_url, TOKEN, logger)

    if update_success:
        logger.info(f"Successfully set due date for work order {work_order_id} to {due_date}")
        return True, due_date

    logger.error(f"Failed to set due date for work order {work_order_id}")
    return False, None