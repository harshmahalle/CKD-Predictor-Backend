import sys
import numpy as np
import json
import os
import joblib

# Determine the directory where predictor.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to the saved model and scaler
model_path = os.path.join(script_dir, '..', 'models', 'svc_model.joblib')
scaler_path = os.path.join(script_dir, '..', 'models', 'x_scaler.joblib')

# Load the saved model and scaler once
try:
    svc_model = joblib.load(model_path)
    x_scaler = joblib.load(scaler_path)
except Exception as e:
    error_output = {'error': f'Error loading model or scaler: {str(e)}'}
    print(json.dumps(error_output))
    sys.exit(1)

def predict(features):
    features = np.array(features).reshape(1, -1)
    features = x_scaler.transform(features)
    prediction = svc_model.predict(features)
    proba = svc_model.predict_proba(features).max()
    return prediction[0], proba

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            input_data = json.loads(line)
            sg = float(input_data['sg'])
            al = float(input_data['al'])
            sc = float(input_data['sc'])
            hemo = float(input_data['hemo'])
            pcv = float(input_data['pcv'])
            htn = int(input_data['htn'])

            result, probability = predict([sg, al, sc, hemo, pcv, htn])

            output = {
                'prediction': str(result),
                'probability': float(probability)
            }

            print(json.dumps(output))
            sys.stdout.flush()
        except Exception as e:
            error_output = {'error': str(e)}
            print(json.dumps(error_output))
            sys.stdout.flush()

if __name__ == '__main__':
    main()


