# 🔍 Error Analysis: IAM Role ARN Validation Failure

## 📊 Error Details

### Error Message
```
An error occurred (ValidationException) when calling the CreateModel operation: 
1 validation error detected: Value '***' at 'executionRoleArn' failed to 
satisfy constraint: Member must satisfy regular expression pattern: 
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+

Error: Process completed with exit code 254.
```

### Where It Happens
- **File**: `.github/workflows/deploy.yml`
- **Step**: "Create SageMaker Model" (line 57-66)
- **Command**: `aws sagemaker create-model`
- **Parameter**: `--execution-role-arn ${{ env.SAGEMAKER_ROLE }}`

### Code Location
```yaml
- name: Create SageMaker Model
  run: |
    aws sagemaker create-model \
      --model-name ${{ env.MODEL_NAME }} \
      --primary-container Image=...,ModelDataUrl=... \
      --execution-role-arn ${{ env.SAGEMAKER_ROLE }}  # ← ERROR HERE
```

---

## 🎯 Root Cause Analysis

### What's Happening
1. GitHub Actions reads `SAGEMAKER_ROLE_ARN` secret
2. The secret value is invalid (empty, placeholder, or wrong format)
3. AWS SageMaker API rejects the request
4. Deployment fails

### Why It's Failing
The `executionRoleArn` parameter requires a valid AWS IAM Role ARN that:
- ✅ Exists in your AWS account
- ✅ Has the correct format: `arn:aws:iam::XXXXXXXXXXXX:role/RoleName`
- ✅ Has SageMaker permissions
- ✅ Can be passed by your IAM user

### Common Causes
1. **Secret Not Set**: `SAGEMAKER_ROLE_ARN` GitHub secret is empty
2. **Placeholder Value**: Secret contains `"your-role-arn-here"` or similar
3. **Role Doesn't Exist**: IAM role not created in AWS
4. **Wrong Format**: ARN is incomplete or malformed
5. **Copy-Paste Error**: Extra spaces, line breaks, or truncated ARN

---

## 🔬 Technical Details

### Required ARN Pattern
```regex
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+
```

### Pattern Breakdown
- `arn:aws` - Fixed prefix (can be `aws`, `aws-cn`, `aws-us-gov`)
- `iam::` - IAM service identifier
- `\d{12}` - 12-digit AWS account ID (e.g., `123456789012`)
- `:role/` - Role separator
- `[a-zA-Z_0-9+=,.@\-_/]+` - Role name (alphanumeric + special chars)

### Valid Examples
```
✅ arn:aws:iam::123456789012:role/SageMakerExecutionRole
✅ arn:aws:iam::987654321098:role/MyCustomRole
✅ arn:aws:iam::111122223333:role/service-role/AmazonSageMaker-ExecutionRole
```

### Invalid Examples
```
❌ your-role-arn-here
❌ arn:aws:iam:::role/SageMakerRole (missing account ID)
❌ arn:aws:iam::12345:role/Role (account ID too short)
❌ arn:aws:iam::123456789012:SageMakerRole (missing :role/)
❌ *** (masked/empty value)
```

---

## 🛠️ Diagnostic Steps

### Step 1: Check GitHub Secret Value
```powershell
# You can't view the secret directly, but you can verify it's set
# Go to: GitHub Repo → Settings → Secrets and variables → Actions
# Look for: SAGEMAKER_ROLE_ARN
```

### Step 2: Verify IAM Role Exists
```powershell
# Check if role exists in AWS
aws iam get-role --role-name SageMakerExecutionRole

# Expected output:
# {
#     "Role": {
#         "Arn": "arn:aws:iam::123456789012:role/SageMakerExecutionRole",
#         ...
#     }
# }
```

### Step 3: Run Verification Script
```powershell
cd "c:\Users\Abdul Rehman\OneDrive\Desktop\aiclass\ML_Projects\heart-dicease-system"
python verify_aws_setup.py
```

This will:
- Check AWS credentials
- Verify IAM role exists
- Validate ARN format
- Check permissions
- Show you the correct ARN to use

### Step 4: Check GitHub Actions Logs
1. Go to GitHub repository
2. Click "Actions" tab
3. Click on the failed workflow run
4. Expand "Create SageMaker Model" step
5. Look for the exact error message

---

## ✅ Solution Summary

### Quick Fix (5 minutes)
1. Create IAM role in AWS Console
2. Copy the Role ARN
3. Update GitHub secret `SAGEMAKER_ROLE_ARN`
4. Push code to redeploy

**See**: `QUICK_FIX.md`

### Detailed Fix (15 minutes)
1. Create IAM role with proper permissions
2. Verify role ARN format
3. Update GitHub secret
4. Verify IAM user can pass the role
5. Run verification script
6. Deploy again

**See**: `FIX_IAM_ROLE_ERROR.md`

---

## 🔄 Workflow After Fix

```
┌─────────────────────┐
│ 1. Create IAM Role  │
│    in AWS Console   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. Copy Role ARN    │
│    (starts with     │
│    arn:aws:iam::)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. Update GitHub    │
│    Secret           │
│    SAGEMAKER_ROLE_  │
│    ARN              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. Run Verification │
│    python verify_   │
│    aws_setup.py     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. Push to GitHub   │
│    git push         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 6. GitHub Actions   │
│    Deploys          │
│    Successfully ✅  │
└─────────────────────┘
```

---

## 📋 Prevention Checklist

To avoid this error in the future:

- [ ] Always create IAM role before setting up GitHub Actions
- [ ] Copy ARN directly from AWS Console (avoid manual typing)
- [ ] Verify ARN format before pasting into GitHub
- [ ] Run `verify_aws_setup.py` before first deployment
- [ ] Keep IAM role name consistent (`SageMakerExecutionRole`)
- [ ] Document your AWS account ID for reference

---

## 🎓 Learning Points

### What You're Learning
1. **AWS IAM**: Roles, policies, and permissions
2. **ARN Format**: AWS Resource Name structure
3. **GitHub Secrets**: Secure credential management
4. **CI/CD Debugging**: Troubleshooting deployment pipelines
5. **AWS SageMaker**: Model deployment requirements

### Key Concepts
- **IAM Role**: Defines what AWS services can do
- **Execution Role**: Allows SageMaker to access S3, CloudWatch, etc.
- **ARN**: Unique identifier for AWS resources
- **GitHub Secrets**: Encrypted environment variables
- **PassRole Permission**: Allows user to assign role to service

---

## 📚 Additional Resources

### AWS Documentation
- [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [SageMaker Execution Roles](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html)
- [ARN Format](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)

### Project Documentation
- `QUICK_FIX.md` - Fast solution
- `FIX_IAM_ROLE_ERROR.md` - Comprehensive guide
- `verify_aws_setup.py` - Diagnostic tool
- `QUICK_REFERENCE.md` - Command reference

---

## 🎯 Success Metrics

### Before Fix
```
❌ GitHub Actions: Failed
❌ SageMaker Model: Not created
❌ Endpoint: Not deployed
❌ Error: ValidationException
```

### After Fix
```
✅ GitHub Actions: Passed
✅ SageMaker Model: Created
✅ Endpoint: InService
✅ Test: Returns predictions
```

---

## 💡 Pro Tips

1. **Always verify locally first**: Run `verify_aws_setup.py` before deploying
2. **Keep ARN handy**: Save your Role ARN in a secure note
3. **Use consistent naming**: Stick with `SageMakerExecutionRole`
4. **Check logs**: GitHub Actions logs show exact error location
5. **Test incrementally**: Fix one issue at a time

---

**Next Step**: Open `QUICK_FIX.md` or `FIX_IAM_ROLE_ERROR.md` to fix the issue!

**Good luck! 🚀**
