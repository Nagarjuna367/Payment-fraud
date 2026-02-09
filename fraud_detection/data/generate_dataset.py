import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic fraud detection dataset
n_samples = 100000

# Generate timestamps
start_date = datetime(2017, 4, 1)
timestamps = [start_date + timedelta(seconds=int(x)) for x in np.random.uniform(0, 365*24*3600, n_samples)]

# Create base features
data = {
    'step': np.random.randint(1, 745, n_samples),
    'type': np.random.choice(['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'], n_samples),
    'amount': np.abs(np.random.gamma(2, 2, n_samples) * 1000),
    'nameOrig': [f'C{i}' for i in range(n_samples)],
    'oldbalanceOrg': np.abs(np.random.normal(50000, 30000, n_samples)),
    'newbalanceOrig': np.abs(np.random.normal(50000, 30000, n_samples)),
    'nameDest': [f'M{i}' for i in range(n_samples)],
    'oldbalanceDest': np.abs(np.random.normal(60000, 40000, n_samples)),
    'newbalanceDest': np.abs(np.random.normal(60000, 40000, n_samples)),
}

# Create fraud label with class imbalance (typical in fraud detection)
fraud_ratio = 0.001  # 0.1% fraud rate
fraud_labels = np.random.binomial(1, fraud_ratio, n_samples)

# Make frauds more likely for certain features
fraud_indices = np.where(fraud_labels == 1)[0]
for idx in fraud_indices:
    if np.random.random() > 0.3:
        data['amount'][idx] *= np.random.uniform(2, 5)  # Higher amounts for fraud
        data['type'][idx] = np.random.choice(['CASH_OUT', 'TRANSFER'], 1)[0]

data['isFraud'] = fraud_labels
data['timestamp'] = pd.DatetimeIndex(timestamps)

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('PS_20174392719_1491204439457_logs.csv', index=False)
print(f"Dataset created with {len(df)} rows and {len(df.columns)} columns")
print(f"Fraud cases: {df['isFraud'].sum()} ({df['isFraud'].sum()/len(df)*100:.2f}%)")
