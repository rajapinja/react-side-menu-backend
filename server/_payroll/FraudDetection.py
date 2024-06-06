from sklearn.ensemble import IsolationForest

# Load payroll data
payroll_data = pd.read_csv('payroll_data.csv')

# Train Isolation Forest model for anomaly detection
model = IsolationForest(contamination=0.01)
model.fit(payroll_data[['salary']])

# Predict anomalies
anomalies = model.predict(payroll_data[['salary']])
