"""
Cleanup script to delete SageMaker resources
"""

import boto3
import sys

def cleanup_sagemaker_resources(endpoint_name='heart-disease-predictor', region='us-east-1'):
    """Delete SageMaker endpoint, endpoint config, and model"""
    
    client = boto3.client('sagemaker', region_name=region)
    
    print("="*60)
    print("Cleaning up SageMaker Resources")
    print("="*60)
    
    # Delete endpoint
    try:
        print(f"\n1. Deleting endpoint: {endpoint_name}")
        client.delete_endpoint(EndpointName=endpoint_name)
        print(f"   ✓ Endpoint '{endpoint_name}' deleted successfully")
    except client.exceptions.ResourceNotFound:
        print(f"   ℹ Endpoint '{endpoint_name}' not found")
    except Exception as e:
        print(f"   ✗ Error deleting endpoint: {str(e)}")
    
    # Delete endpoint config
    try:
        config_name = f"{endpoint_name}-config"
        print(f"\n2. Deleting endpoint config: {config_name}")
        client.delete_endpoint_config(EndpointConfigName=config_name)
        print(f"   ✓ Endpoint config '{config_name}' deleted successfully")
    except client.exceptions.ResourceNotFound:
        print(f"   ℹ Endpoint config '{config_name}' not found")
    except Exception as e:
        print(f"   ✗ Error deleting endpoint config: {str(e)}")
    
    # Delete model
    try:
        print(f"\n3. Deleting model: {endpoint_name}")
        client.delete_model(ModelName=endpoint_name)
        print(f"   ✓ Model '{endpoint_name}' deleted successfully")
    except client.exceptions.ResourceNotFound:
        print(f"   ℹ Model '{endpoint_name}' not found")
    except Exception as e:
        print(f"   ✗ Error deleting model: {str(e)}")
    
    print("\n" + "="*60)
    print("Cleanup Complete!")
    print("="*60)

if __name__ == "__main__":
    endpoint_name = sys.argv[1] if len(sys.argv) > 1 else 'heart-disease-predictor'
    region = sys.argv[2] if len(sys.argv) > 2 else 'us-east-1'
    
    cleanup_sagemaker_resources(endpoint_name, region)
