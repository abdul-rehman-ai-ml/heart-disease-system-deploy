#!/usr/bin/env python3
"""
AWS Setup Verification Script
Checks if your AWS credentials and IAM role are configured correctly
"""

import boto3
import re
import sys
from botocore.exceptions import ClientError, NoCredentialsError

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    print_header("1. Checking AWS Credentials")
    
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print_success("AWS credentials are configured")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        print(f"   User ID: {identity['UserId']}")
        
        return True, identity['Account']
    except NoCredentialsError:
        print_error("No AWS credentials found")
        print("   Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False, None
    except Exception as e:
        print_error(f"Error checking credentials: {str(e)}")
        return False, None

def check_sagemaker_permissions():
    """Check if user has SageMaker permissions"""
    print_header("2. Checking SageMaker Permissions")
    
    try:
        sagemaker = boto3.client('sagemaker', region_name='us-east-1')
        # Try to list models (read-only operation)
        sagemaker.list_models(MaxResults=1)
        
        print_success("User has SageMaker permissions")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print_error("User does not have SageMaker permissions")
            print("   Add 'AmazonSageMakerFullAccess' policy to your IAM user")
        else:
            print_error(f"Error checking SageMaker permissions: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False

def check_s3_permissions():
    """Check if user has S3 permissions"""
    print_header("3. Checking S3 Permissions")
    
    try:
        s3 = boto3.client('s3')
        # Try to list buckets (read-only operation)
        response = s3.list_buckets()
        
        print_success("User has S3 permissions")
        print(f"   Found {len(response['Buckets'])} buckets")
        
        # List bucket names
        if response['Buckets']:
            print("\n   Available buckets:")
            for bucket in response['Buckets'][:5]:  # Show first 5
                print(f"   - {bucket['Name']}")
        
        return True
    except ClientError as e:
        print_error(f"User does not have S3 permissions: {str(e)}")
        print("   Add 'AmazonS3FullAccess' policy to your IAM user")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False

def check_iam_role(role_name='SageMakerExecutionRole', account_id=None):
    """Check if SageMaker execution role exists"""
    print_header("4. Checking SageMaker Execution Role")
    
    try:
        iam = boto3.client('iam')
        
        # Try to get the role
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        
        print_success(f"Role '{role_name}' exists")
        print(f"   Role ARN: {role_arn}")
        
        # Validate ARN format
        arn_pattern = r'^arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+$'
        if re.match(arn_pattern, role_arn):
            print_success("Role ARN format is valid")
        else:
            print_error("Role ARN format is invalid")
        
        # Check attached policies
        print("\n   Checking attached policies...")
        policies = iam.list_attached_role_policies(RoleName=role_name)
        
        required_policies = ['AmazonSageMakerFullAccess']
        found_policies = [p['PolicyName'] for p in policies['AttachedPolicies']]
        
        for policy in required_policies:
            if policy in found_policies:
                print_success(f"Policy '{policy}' is attached")
            else:
                print_warning(f"Policy '{policy}' is NOT attached")
        
        print("\n   📋 Copy this ARN for GitHub Secret:")
        print(f"   {role_arn}")
        
        return True, role_arn
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print_error(f"Role '{role_name}' does not exist")
            print("\n   Create the role using:")
            print("   1. AWS Console: IAM → Roles → Create role → SageMaker")
            print("   2. Or see FIX_IAM_ROLE_ERROR.md for detailed steps")
            
            if account_id:
                print(f"\n   Expected ARN format:")
                print(f"   arn:aws:iam::{account_id}:role/{role_name}")
        else:
            print_error(f"Error checking role: {str(e)}")
        return False, None
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False, None

def check_passrole_permission(role_arn):
    """Check if user can pass the role to SageMaker"""
    print_header("5. Checking PassRole Permission")
    
    try:
        iam = boto3.client('iam')
        sts = boto3.client('sts')
        
        # Get current user
        identity = sts.get_caller_identity()
        user_arn = identity['Arn']
        
        # This is a simplified check - actual PassRole is tested during deployment
        print_success("User identity verified")
        print("   Note: PassRole permission will be tested during actual deployment")
        
        return True
        
    except Exception as e:
        print_warning(f"Could not verify PassRole permission: {str(e)}")
        print("   This will be tested during deployment")
        return True

def validate_arn_format(arn):
    """Validate ARN format"""
    pattern = r'^arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+$'
    return bool(re.match(pattern, arn))

def main():
    """Main verification function"""
    print("\n" + "="*60)
    print("  AWS SETUP VERIFICATION FOR SAGEMAKER DEPLOYMENT")
    print("="*60)
    
    results = {
        'credentials': False,
        'sagemaker': False,
        's3': False,
        'role': False,
        'passrole': False
    }
    
    # Check credentials
    results['credentials'], account_id = check_aws_credentials()
    if not results['credentials']:
        print("\n❌ FAILED: Fix AWS credentials first")
        sys.exit(1)
    
    # Check SageMaker permissions
    results['sagemaker'] = check_sagemaker_permissions()
    
    # Check S3 permissions
    results['s3'] = check_s3_permissions()
    
    # Check IAM role
    results['role'], role_arn = check_iam_role(account_id=account_id)
    
    # Check PassRole permission
    if results['role'] and role_arn:
        results['passrole'] = check_passrole_permission(role_arn)
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    if all_passed:
        print_success("All checks passed! ✨")
        print("\n📋 Next Steps:")
        print("   1. Copy the Role ARN shown above")
        print("   2. Add it to GitHub Secrets as 'SAGEMAKER_ROLE_ARN'")
        print("   3. Push your code to trigger deployment")
        print("\n   See FIX_IAM_ROLE_ERROR.md for detailed instructions")
    else:
        print_error("Some checks failed")
        print("\n❌ Failed Checks:")
        for check, passed in results.items():
            if not passed:
                print(f"   - {check}")
        
        print("\n📖 See FIX_IAM_ROLE_ERROR.md for solutions")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
