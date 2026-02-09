# Online Payments Fraud Detection System

A machine learning-powered fraud detection system for online payment transactions using Random Forest classification.

## Features

- **Real-time Fraud Detection**: Analyzes transaction details and classifies them as fraud or legitimate
- **Multi-Currency Support**: USD, EUR, GBP, INR, JPY
- **Web Interface**: Easy-to-use Flask web application
- **REST API**: JSON API for programmatic access
- **High Accuracy**: 99.91% accuracy on 100,000 transactions

## Quick Start

1. **Install dependencies:**
   ``
   pip install -r requirements.txt
   ``

2. **Run the application:**
   ``
   python flask_app/app.py
   ``

3. **Open in browser:**
   http://localhost:5000

## API Usage

POST to http://localhost:5000/api/predict:

\\\json
{
  "step": 100,
  "type": "TRANSFER",
  "amount": 1500.00,
  "oldbalanceOrg": 50000.00,
  "newbalanceOrig": 48500.00,
  "oldbalanceDest": 30000.00,
  "newbalanceDest": 31500.00,
  "currency": "USD"
}
\\\

## Available Routes

- **/** - Home page
- **/predict** - Transaction input form
- **/submit** - Results page (POST)
- **/api/predict** - Fraud prediction API
- **/api/stats** - Model statistics
- **/api/health** - Health check

## Model Details

- **Algorithm:** Random Forest Classifier
- **Accuracy:** 99.91%
- **Features:** step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
- **Training Data:** 100,000 transactions

## Results

- **✅ LEGITIMATE TRANSACTION** - Transaction is classified as real
- **🚨 FRAUDULENT TRANSACTION** - Transaction is classified as fraud

Output includes complete transaction details for verification.

## Technologies

- Python 3.14+
- Flask 2.3.3
- scikit-learn 1.8.0
- pandas 3.0.0

## License

MIT
