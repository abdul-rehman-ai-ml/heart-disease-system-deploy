# PowerShell Script to Create SageMaker Execution Role
# Run this if you prefer using AWS CLI

Write-Host "Creating SageMaker Execution Role..." -ForegroundColor Cyan

# 1. Create trust policy
$trustPolicy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@

$trustPolicy | Out-File -FilePath "trust-policy.json" -Encoding utf8

Write-Host "✓ Trust policy created" -ForegroundColor Green

# 2. Create the role
Write-Host "Creating IAM role..." -ForegroundColor Cyan
aws iam create-role `
  --role-name SageMakerExecutionRole `
  --assume-role-policy-document file://trust-policy.json

Write-Host "✓ Role created" -ForegroundColor Green

# 3. Attach SageMaker policy
Write-Host "Attaching SageMaker policy..." -ForegroundColor Cyan
aws iam attach-role-policy `
  --role-name SageMakerExecutionRole `
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

Write-Host "✓ SageMaker policy attached" -ForegroundColor Green

# 4. Attach S3 policy
Write-Host "Attaching S3 policy..." -ForegroundColor Cyan
aws iam attach-role-policy `
  --role-name SageMakerExecutionRole `
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

Write-Host "✓ S3 policy attached" -ForegroundColor Green

# 5. Get the Role ARN
Write-Host "`n" -NoNewline
Write-Host "Getting Role ARN..." -ForegroundColor Cyan
$roleArn = aws iam get-role --role-name SageMakerExecutionRole --query 'Role.Arn' --output text

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "SUCCESS! Role Created" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "`nYour SageMaker Role ARN is:" -ForegroundColor Cyan
Write-Host $roleArn -ForegroundColor White
Write-Host "`n📋 COPY THIS ARN and add it to GitHub Secrets as:" -ForegroundColor Yellow
Write-Host "   Secret Name: SAGEMAKER_ROLE_ARN" -ForegroundColor White
Write-Host "   Secret Value: $roleArn" -ForegroundColor White
Write-Host "`n========================================`n" -ForegroundColor Yellow

# Cleanup
Remove-Item "trust-policy.json" -ErrorAction SilentlyContinue

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions" -ForegroundColor White
Write-Host "2. Update secret: SAGEMAKER_ROLE_ARN" -ForegroundColor White
Write-Host "3. Paste the ARN shown above" -ForegroundColor White
Write-Host "4. Push code to deploy: git push origin main`n" -ForegroundColor White
