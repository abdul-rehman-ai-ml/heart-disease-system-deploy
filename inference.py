"""
SageMaker Inference Handler for Heart Disease Prediction
This script handles model loading and predictions in SageMaker
"""

import json
import joblib
import numpy as np
import os

# Global variable to store the loaded model
model = None

def model_fn(model_dir):
    """
    Load the model for inference
    This function is called once when the endpoint is created
    """
    global model
    model_path = os.path.join(model_dir, 'model.joblib')
    model = joblib.load(model_path)
    return model

def input_fn(request_body, content_type='application/json'):
    """
    Deserialize and prepare the prediction input
    """
    if content_type == 'application/json':
        input_data = json.loads(request_body)
        
        # Handle different input formats
        if 'instances' in input_data:
            instances = input_data['instances']
        elif isinstance(input_data, list):
            instances = input_data
        else:
            instances = [input_data]
        
        return np.array(instances)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(input_data, model):
    """
    Apply model to the incoming request
    """
    # Make predictions
    predictions = model.predict(input_data)
    
    # Get probability scores
    probabilities = model.predict_proba(input_data)
    
    # Extract risk scores (probability of disease - class 1)
    risk_scores = probabilities[:, 1].tolist()
    
    return {
        'predictions': predictions.tolist(),
        'risk_scores': risk_scores
    }

def output_fn(prediction, accept='application/json'):
    """
    Serialize the prediction result
    """
    if accept == 'application/json':
        return json.dumps(prediction), accept
    else:
        raise ValueError(f"Unsupported accept type: {accept}")

# For local testing
if __name__ == "__main__":
    # Load model
    model = model_fn('.')
    
    # Test prediction
    test_input = {
        "instances": [[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]]
    }
    
    input_data = input_fn(json.dumps(test_input))
    prediction = predict_fn(input_data, model)
    output, content_type = output_fn(prediction)
    
    print("Test Prediction:")
    print(output)
