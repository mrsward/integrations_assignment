import requests
import os
import sys
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, abort
import hmac
import hashlib
from set_due_date import set_due_date_by_priority

# Initialize Constants
TOKEN = os.getenv("TOKEN")  # Retrieve the API token from environment variables
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET') # Retrieve webhook sectret from environment variables

app = Flask(__name__)

# This function verifies the signature in the webhook request
def verify_signature(request):
    # Extract the timestamp and signatures from the header
    signature_header = request.headers.get('X-Signature')
    if not signature_header:
        logging.error("Missing signature header")
        return False

    elements = dict(item.split('=') for item in signature_header.split(','))
    timestamp = elements.get('t')
    signature = elements.get('v1')

    if not timestamp or not signature:
        logging.error("Missing timestamp or signature in header")
        return False

    # Prepare the signed_payload string
    signed_payload = f"{timestamp}.{request.get_data(as_text=True)}"

    # Compute the expected signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Compare the signatures
    if hmac.compare_digest(expected_signature, signature):
        return True
    else:
        logging.error("Signature mismatch")
        return False

@app.route('/set_priority', methods=['POST'])
def set_priority():
    # Verify signature coming from webhook
    if not verify_signature(request):
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 401

    # Extract work order id and priority from webhook data
    data = request.json
    work_order_id = data.get('workOrderId')
    new_work_order = data.get('newWorkOrder')

    if not work_order_id and not new_work_order:
        abort(400, description="Work Order ID and New Work Order Information must be provided.")

    priority = new_work_order.get("priority")

    if not priority:
        abort(400, description="No Priority could be found in newly created work order. Cannot assign due date.")

    # Log the received data
    logging.info(f"Received Work Order with ID: {work_order_id} and priority: {priority}")

    # Calculate, and assign due date to work order
    success, due_date = set_due_date_by_priority(work_order_id, priority)
    
    # Craft response based on status of success
    if success:
        response = {
            'status': 'success',
            'message': f'Work Order: {work_order_id} due date has been set to {due_date}'
        }
        return jsonify(response), 200
    else:
        response = {
            'status': 'failure',
            'message': f'Failed to set due date for Work Order: {work_order_id}'
        }        
        return jsonify(response), 400

if __name__ == '__main__':
    app.run(debug=True)