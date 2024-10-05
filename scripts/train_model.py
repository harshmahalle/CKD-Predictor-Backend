import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score 
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
import joblib
import os

# Determine the directory where train_model.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the CSV file
csv_path = os.path.join(script_dir, '..', 'data', 'kidney_disease.csv')

# Load dataset
df = pd.read_csv(csv_path)
columns_to_retain = ['sg', 'al', 'sc', 'hemo', 'pcv', 'htn', 'classification']
df = df.drop([col for col in df.columns if col not in columns_to_retain], axis=1)
df = df.dropna(axis=0)

# Encode categorical variables if any
for column in df.columns:
    if pd.api.types.is_numeric_dtype(df[column]):
        continue
    df[column] = df[column].astype('category').cat.codes

X = df.drop(['classification'], axis=1)
y = df['classification']

# Scale the input
x_scaler = MinMaxScaler()
X_scaled = x_scaler.fit_transform(X)

# Train SVM model
svc_model = SVC(C=0.1, kernel='linear', gamma=1, probability=True)
svc_model.fit(X_scaled, y)

# Make predictions on the training data
y_pred = svc_model.predict(X_scaled)

# Calculate evaluation metrics
accuracy = accuracy_score(y, y_pred)

# Print evaluation metrics
print(f"Training Accuracy: {accuracy * 100:.2f}%")

# Save the scaler and model
model_path = os.path.join(script_dir, '..', 'models', 'svc_model.joblib')
scaler_path = os.path.join(script_dir, '..', 'models', 'x_scaler.joblib')

os.makedirs(os.path.join(script_dir, '..', 'models'), exist_ok=True)

joblib.dump(svc_model, model_path)
joblib.dump(x_scaler, scaler_path)

print(f"Model saved to {model_path}")
print(f"Scaler saved to {scaler_path}")
