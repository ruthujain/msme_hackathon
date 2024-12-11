from flask import Flask, request, jsonify, Blueprint
import logging
from werkzeug.exceptions import BadRequest
from hsn_classifier import classify_hsn
from compliance import validate_compliance
from blockchain_handler import deposit_funds, release_payment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Define API Blueprints for better organization
api_bp = Blueprint('api', __name__)

# Utility function for error handling
def handle_error(e):
    logger.error(f"Error: {e}")
    return jsonify({"error": str(e)}), 400

# HSN Classification Endpoint
@api_bp.route('/hsn_classify', methods=['POST'])
def classify_hsn_endpoint():
    try:
        data = request.get_json()
        if not data or 'description' not in data:
            raise BadRequest("Missing 'description' in the request body")
        
        description = data['description']
        
        # Validate and classify HSN code
        hsn_code = classify_hsn(description)
        
        if not hsn_code:
            raise BadRequest("Unable to classify HSN code")
        
        return jsonify({"hsnCode": hsn_code}), 200

    except Exception as e:
        return handle_error(e)

# Deposit Funds Endpoint
@api_bp.route('/deposit_funds', methods=['POST'])
def deposit_funds_endpoint():
    try:
        data = request.get_json()
        if not data or 'amount' not in data:
            raise BadRequest("Missing 'amount' in the request body")
        
        amount = data['amount']
        
        # Deposit funds to blockchain
        response = deposit_funds(amount)
        
        if 'error' in response:
            raise BadRequest(f"Failed to deposit funds: {response['error']}")
        
        return jsonify(response), 200

    except Exception as e:
        return handle_error(e)

# Release Payment Endpoint
@api_bp.route('/release_payment', methods=['POST'])
def release_payment_endpoint():
    try:
        data = request.get_json()
        if not data or 'shipment_id' not in data:
            raise BadRequest("Missing 'shipment_id' in the request body")
        
        shipment_id = data['shipment_id']
        
        # Release payment based on shipment ID
        response = release_payment(shipment_id)
        
        if 'error' in response:
            raise BadRequest(f"Failed to release payment: {response['error']}")
        
        return jsonify(response), 200

    except Exception as e:
        return handle_error(e)

# Register API Blueprint with the Flask app
app.register_blueprint(api_bp, url_prefix='/api')

# Custom error handler for BadRequest and internal errors
@app.errorhandler(BadRequest)
def handle_bad_request_error(error):
    logger.error(f"Bad Request: {error}")
    return jsonify({"error": str(error)}), 400

@app.errorhandler(Exception)
def handle_internal_error(error):
    logger.error(f"Internal Error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
