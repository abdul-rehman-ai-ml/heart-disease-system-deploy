"""
Test script for SageMaker endpoint
"""

import boto3
import json
import sys

def test_endpoint(endpoint_name='heart-disease-predictor', region='us-east-1'):
    """Test the deployed SageMaker endpoint"""
    
    client = boto3.client('sagemaker-runtime', region_name=region)
    
    # Test cases
    test_cases = [
        {
            "name": "High Risk Patient",
            "data": [[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]]
        },
        {
            "name": "Low Risk Patient",
            "data": [[45, 0, 1, 120, 200, 0, 1, 170, 0, 0.5, 1, 0, 2]]
        }
    ]
    
    print("="*60)
    print(f"Testing Endpoint: {endpoint_name}")
    print("="*60)
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        print(f"Input: {test_case['data'][0]}")
        
        try:
            response = client.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=json.dumps({"instances": test_case['data']})
            )
            
            result = json.loads(response['Body'].read())
            prediction = result['predictions'][0]
            risk_score = result['risk_scores'][0]
            
            print(f"Prediction: {'Disease' if prediction == 1 else 'No Disease'}")
            print(f"Risk Score: {risk_score:.2%}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    endpoint_name = sys.argv[1] if len(sys.argv) > 1 else 'heart-disease-predictor'
    region = sys.argv[2] if len(sys.argv) > 2 else 'us-east-1'
    
    test_endpoint(endpoint_name, region)
