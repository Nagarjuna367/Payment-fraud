#!/usr/bin/env python3
"""
Test script to demonstrate fraud detection output
Shows both legitimate and fraudulent transaction examples
"""
import json
from urllib import request
import time

# Give server a moment to start
time.sleep(2)

BASE_URL = 'http://127.0.0.1:5000/api/predict'

test_cases = [
    {
        "name": "✅ LEGITIMATE TRANSACTION (Low Amount Transfer)",
        "data": {
            "step": 100,
            "type": "TRANSFER",
            "amount": 1500.00,
            "oldbalanceOrg": 50000.00,
            "newbalanceOrig": 48500.00,
            "oldbalanceDest": 30000.00,
            "newbalanceDest": 31500.00,
            "currency": "USD"
        }
    },
    {
        "name": "⚠️ SUSPICIOUS TRANSACTION (Large Cash Out)",
        "data": {
            "step": 450,
            "type": "CASH_OUT",
            "amount": 50000.00,
            "oldbalanceOrg": 60000.00,
            "newbalanceOrig": 10000.00,
            "oldbalanceDest": 25000.00,
            "newbalanceDest": 75000.00,
            "currency": "EUR"
        }
    },
    {
        "name": "✅ LEGITIMATE TRANSACTION (Payment with GBP)",
        "data": {
            "step": 200,
            "type": "PAYMENT",
            "amount": 2500.00,
            "oldbalanceOrg": 75000.00,
            "newbalanceOrig": 72500.00,
            "oldbalanceDest": 40000.00,
            "newbalanceDest": 42500.00,
            "currency": "GBP"
        }
    }
]

print("\n" + "=" * 80)
print("FRAUD DETECTION SYSTEM - OUTPUT DEMONSTRATION")
print("=" * 80)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: {test_case['name']}")
    print(f"{'=' * 80}\n")
    
    try:
        payload = test_case['data']
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(BASE_URL, data=data, 
                            headers={'Content-Type': 'application/json'})
        
        with request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            
            # Display formatted output
            print(f"RESULT: {result['prediction']}")
            print(f"STATUS: {'🔴 FRAUD' if result['is_fraud'] else '🟢 LEGITIMATE'}")
            print(f"Fraud Probability: {result['fraud_probability']}%")
            print(f"Normal Probability: {result['normal_probability']}%")
            print(f"Currency: {result['currency']}")
            print(f"Timestamp: {result['timestamp']}")
            
            print("\nTRANSACTION DETAILS:")
            print("─" * 80)
            for key, value in result['transaction_details'].items():
                print(f"  {key.replace('_', ' ').title():25s}: {value}")
            print("─" * 80)
            
    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "=" * 80)
print("OUTPUT FORMAT SUCCESSFULLY DEMONSTRATED")
print("=" * 80)
print("\nKey Features:")
print("  • Clear FRAUD (🔴) or LEGITIMATE (🟢) classification")
print("  • All transaction details displayed in selected currency")
print("  • Probability scores for both fraud and legitimate scenarios")
print("  • Complete timestamp for audit trail")
print("=" * 80 + "\n")
