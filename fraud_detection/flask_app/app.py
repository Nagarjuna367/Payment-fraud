"""
Fraud Detection Web Application - Flask Backend
This application provides a web interface for real-time fraud detection predictions
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime
import socket

# Initialize Flask app
app = Flask(__name__)
app.config['DEBUG'] = True

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Resolve project root and load the trained model and label encoder
# This ensures the paths work regardless of the current working directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'model.pkl')
ENCODER_PATH = os.path.join(PROJECT_ROOT, 'models', 'label_encoder.pkl')

model = None
label_encoder = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info(f"✓ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logger.error(f"✗ Error loading model from {MODEL_PATH}: {e}")

try:
    with open(ENCODER_PATH, 'rb') as f:
        label_encoder = pickle.load(f)
    logger.info(f"✓ Label encoder loaded successfully from {ENCODER_PATH}")
except Exception as e:
    logger.error(f"✗ Error loading encoder from {ENCODER_PATH}: {e}")

# Feature names used during training
FEATURE_NAMES = ['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
                 'oldbalanceDest', 'newbalanceDest']

# Currency symbols mapping for display
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'JPY': '¥'
}

def format_currency(amount, currency='USD'):
    try:
        symbol = CURRENCY_SYMBOLS.get(currency.upper(), '')
        if symbol:
            return f"{symbol}{float(amount):,.2f}"
        else:
            return f"{float(amount):,.2f} {currency}"
    except Exception:
        try:
            return f"{float(amount):,.2f}"
        except Exception:
            return str(amount)

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    """Prediction form page"""
    return render_template('predict.html', 
                         transaction_types=['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
                          'oldbalanceDest', 'newbalanceDest', 'step']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'success': False
                }), 400

        # Optional currency (default USD)
        currency = data.get('currency', 'USD')

        # Prepare input data
        try:
            # Encode transaction type
            trans_type = data['type']
            if trans_type not in label_encoder.classes_:
                return jsonify({
                    'error': f'Invalid transaction type: {trans_type}',
                    'success': False
                }), 400
            
            encoded_type = label_encoder.transform([trans_type])[0]
            
            # Create feature vector
            features = np.array([
                int(data['step']),
                encoded_type,
                float(data['amount']),
                float(data['oldbalanceOrg']),
                float(data['newbalanceOrig']),
                float(data['oldbalanceDest']),
                float(data['newbalanceDest'])
            ]).reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]
            
            # Prepare response with currency-formatted amounts
            is_fraud = bool(prediction)
            fraud_probability = float(probability[1])
            normal_probability = float(probability[0])

            amt = float(data['amount'])
            obs = float(data['oldbalanceOrg'])
            nos = float(data['newbalanceOrig'])
            obd = float(data['oldbalanceDest'])
            nbd = float(data['newbalanceDest'])

            result = {
                'success': True,
                'is_fraud': is_fraud,
                'fraud_probability': round(fraud_probability * 100, 2),
                'normal_probability': round(normal_probability * 100, 2),
                'prediction': 'FRAUDULENT' if is_fraud else 'NORMAL',
                'confidence': round(max(fraud_probability, normal_probability) * 100, 2),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'currency': currency,
                'transaction_details': {
                    'type': trans_type,
                    'amount': format_currency(amt, currency),
                    'step': int(data['step']),
                    'oldbalanceOrg': format_currency(obs, currency),
                    'newbalanceOrig': format_currency(nos, currency),
                    'oldbalanceDest': format_currency(obd, currency),
                    'newbalanceDest': format_currency(nbd, currency)
                }
            }

            logger.info(f"Prediction made: {result['prediction']} (confidence: {result['confidence']}%)")
            return jsonify(result), 200
            
        except ValueError as ve:
            return jsonify({
                'error': f'Invalid input values: {str(ve)}',
                'success': False
            }), 400
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({
            'error': f'Server error during prediction: {str(e)}',
            'success': False
        }), 500

@app.route('/submit', methods=['POST'])
def submit():
    """Form submission handler"""
    try:
        # Get form data
        form_data = {
            'step': request.form.get('step'),
            'type': request.form.get('type'),
            'amount': request.form.get('amount'),
            'oldbalanceOrg': request.form.get('oldbalanceOrg'),
            'newbalanceOrig': request.form.get('newbalanceOrig'),
            'oldbalanceDest': request.form.get('oldbalanceDest'),
            'newbalanceDest': request.form.get('newbalanceDest'),
            'currency': request.form.get('currency', 'USD')
        }
        
        # Validate and convert types
        try:
            features_dict = {
                'step': int(form_data['step']),
                'type': form_data['type'],
                'amount': float(form_data['amount']),
                'oldbalanceOrg': float(form_data['oldbalanceOrg']),
                'newbalanceOrig': float(form_data['newbalanceOrig']),
                'oldbalanceDest': float(form_data['oldbalanceDest']),
                'newbalanceDest': float(form_data['newbalanceDest'])
            }
        except (ValueError, TypeError) as e:
            return render_template('submit.html', 
                                 error=f'Invalid input: {str(e)}',
                                 success=False)
        
        # Get predictions using the API
        features = np.array([
            features_dict['step'],
            label_encoder.transform([features_dict['type']])[0],
            features_dict['amount'],
            features_dict['oldbalanceOrg'],
            features_dict['newbalanceOrig'],
            features_dict['oldbalanceDest'],
            features_dict['newbalanceDest']
        ]).reshape(1, -1)
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        is_fraud = bool(prediction)
        fraud_prob = round(float(probability[1]) * 100, 2)
        normal_prob = round(float(probability[0]) * 100, 2)
        confidence = round(max(probability) * 100, 2)
        
        # Format amounts using selected currency
        currency = form_data.get('currency', 'USD')
        amt_fmt = format_currency(features_dict['amount'], currency)
        obs_fmt = format_currency(features_dict['oldbalanceOrg'], currency)
        nos_fmt = format_currency(features_dict['newbalanceOrig'], currency)
        obd_fmt = format_currency(features_dict['oldbalanceDest'], currency)
        nbd_fmt = format_currency(features_dict['newbalanceDest'], currency)

        # Build detailed transaction summary
        details_html = f"""
        <div class="detail-item">
            <span class="detail-label">Transaction Type:</span>
            <span class="detail-value">{features_dict['type']}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Amount:</span>
            <span class="detail-value">{amt_fmt}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Step:</span>
            <span class="detail-value">{features_dict['step']}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Origin Balance (Before):</span>
            <span class="detail-value">{obs_fmt}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Origin Balance (After):</span>
            <span class="detail-value">{nos_fmt}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Destination Balance (Before):</span>
            <span class="detail-value">{obd_fmt}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Destination Balance (After):</span>
            <span class="detail-value">{nbd_fmt}</span>
        </div>
        """

        result = {
            'success': True,
            'is_fraud': is_fraud,
            'prediction': 'FRAUDULENT TRANSACTION DETECTED!' if is_fraud else 'LEGITIMATE TRANSACTION',
            'fraud_probability': fraud_prob,
            'normal_probability': normal_prob,
            'confidence': confidence,
            'details': details_html
        }
        
        return render_template('submit.html', **result)
        
    except Exception as e:
        logger.error(f"Form submission error: {str(e)}")
        return render_template('submit.html', 
                             error=f'Error processing form: {str(e)}',
                             success=False)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint for model statistics"""
    stats = {
        'model_type': 'Random Forest Classifier',
        'accuracy': 0.9991,
        'precision': 0.8000,
        'recall': 0.1905,
        'f1_score': 0.3077,
        'auc_roc': 0.7140,
        'features': FEATURE_NAMES,
        'training_date': '2026-02-09',
        'dataset_size': '100,000 transactions',
        'fraud_cases': '106 (0.11%)',
        'model_status': 'Ready for production'
    }
    return jsonify(stats), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoder_loaded': label_encoder is not None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Page not found',
        'success': False
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500


if __name__ == '__main__':
    print("\n" + "="*80)
    print("FRAUD DETECTION FLASK APPLICATION")
    print("="*80)
    
    # Check if model and encoder are loaded
    if model is None or label_encoder is None:
        print("✗ ERROR: Model or Encoder failed to load!")
        print("  Please ensure model.pkl and label_encoder.pkl exist in ../models/")
        exit(1)
    
    print("\n✓ Model loaded successfully")
    print("✓ Label encoder loaded successfully")
    print("\n" + "="*80)
    print("Starting Flask Application...")
    print("="*80)
    
    # Get local machine IP address
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "localhost"
    
    print("\n📍 ACCESS POINTS:")
    print(f"\n  • Local Machine (this device):")
    print(f"    http://127.0.0.1:5000")
    print(f"    http://localhost:5000")
    print(f"\n  • From Other Devices on Network:")
    print(f"    http://{local_ip}:5000")
    
    print(f"\n🏠 Home Page: http://{local_ip}:5000/")
    print(f"📝 Prediction Form: http://{local_ip}:5000/predict")
    print(f"🔍 API Health: http://{local_ip}:5000/api/health")
    print(f"📊 API Stats: http://{local_ip}:5000/api/stats")
    
    print("\n" + "="*80)
    print("Listening on all network interfaces (0.0.0.0:5000)")
    print("Press CTRL+C to stop the server")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
