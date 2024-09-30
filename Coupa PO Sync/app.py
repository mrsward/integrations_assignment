import os
import logging
from flask import Flask, request, jsonify, abort
import hmac
import hashlib
from field_name_mappings import PO_MAPPINGS
from coupa_integrator import create_coupa_po, update_coupa_po, cancel_coupa_po, close_coupa_po

# Initialize Constants
TOKEN = os.getenv("TOKEN")  # Retrieve the API token from environment variables
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") # Retrieve webhook secret from environment variables


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

@app.route('/po_created', methods=['POST'])
def create_po():
    # Verify signature coming from webhook
    if not verify_signature(request):
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 401
    
    # Extract purchase order id and purchase order info from webhook data
    data = request.json
    po_id = data.get('purchaseOrderId')
    new_po = data.get('newPurchaseOrder')

    # Map field names by looking up the Coupa field name corresponding to MaintainX field names
    coupa_format_po = {PO_MAPPINGS[key]: value for key, value in new_po.items() if key in PO_MAPPINGS}

     # Calculate, and assign due date to work order
    success = create_coupa_po(coupa_format_po)
    
    # Craft response based on status of success
    if success:
        response = {
            'status': 'success',
            'message': f'Purchase Order: {po_id} has been created in Coupa Successfully'
        }
        return jsonify(response), 200
    else:
        response = {
            'status': 'failure',
            'message': f'Failed to create Purchase Order: {po_id} in Coupa'
        }        
        return jsonify(response), 400

@app.route('/po_updated', methods=['POST'])
def update_po():
    # Verify signature coming from webhook
    if not verify_signature(request):
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 401
    
    # Extract purchase order id and purchase order info from webhook data
    data = request.json
    po_id = data.get('purchaseOrderId')
    new_po = data.get('newPurchaseOrder')

    # Map field names by looking up the Coupa field name corresponding to MaintainX field names
    coupa_format_po = {PO_MAPPINGS[key]: value for key, value in new_po.items() if key in PO_MAPPINGS}

     # Calculate, and assign due date to work order
    success = update_coupa_po(coupa_format_po)
    
    # Craft response based on status of success
    if success:
        response = {
            'status': 'success',
            'message': f'Purchase Order: {po_id} has been updated in Coupa Successfully'
        }
        return jsonify(response), 200
    else:
        response = {
            'status': 'failure',
            'message': f'Failed to update Purchase Order: {po_id} in Coupa'
        }        
        return jsonify(response), 400
    
@app.route('/po_canceled', methods=['POST'])
def cancel_po():
    # Verify signature coming from webhook
    if not verify_signature(request):
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 401
    
    # Extract purchase order id and purchase order info from webhook data
    data = request.json
    po_id = data.get('purchaseOrderId')
    new_po = data.get('newPurchaseOrder')

    # Map field names by looking up the Coupa field name corresponding to MaintainX field names
    coupa_format_po = {PO_MAPPINGS[key]: value for key, value in new_po.items() if key in PO_MAPPINGS}

     # Calculate, and assign due date to work order
    success = cancel_coupa_po(coupa_format_po)
    
    # Craft response based on status of success
    if success:
        response = {
            'status': 'success',
            'message': f'Purchase Order: {po_id} has been canceld in Coupa Successfully'
        }
        return jsonify(response), 200
    else:
        response = {
            'status': 'failure',
            'message': f'Failed to cancel Purchase Order: {po_id} in Coupa'
        }        
        return jsonify(response), 400
    
@app.route('/po_completed', methods=['POST'])
def close_po():
    # Verify signature coming from webhook
    if not verify_signature(request):
        return jsonify({'status': 'error', 'message': 'Invalid signature'}), 401
    
    # Extract purchase order id and purchase order info from webhook data
    data = request.json
    po_id = data.get('purchaseOrderId')
    new_po = data.get('newPurchaseOrder')

    # Map field names by looking up the Coupa field name corresponding to MaintainX field names
    coupa_format_po = {PO_MAPPINGS[key]: value for key, value in new_po.items() if key in PO_MAPPINGS}

     # Calculate, and assign due date to work order
    success = close_coupa_po(coupa_format_po)
    
    # Craft response based on status of success
    if success:
        response = {
            'status': 'success',
            'message': f'Purchase Order: {po_id} has been closed in Coupa Successfully'
        }
        return jsonify(response), 200
    else:
        response = {
            'status': 'failure',
            'message': f'Failed to close Purchase Order: {po_id} in Coupa'
        }        
        return jsonify(response), 400