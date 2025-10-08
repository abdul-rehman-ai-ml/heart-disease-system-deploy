# 🔧 FIX: IAM Role ARN Validation Error

## ❌ Error You're Seeing

```
An error occurred (ValidationException) when calling the CreateModel operation: 
1 validation error detected: Value '***' at 'executionRoleArn' failed to satisfy 
constraint: Member must satisfy regular expression pattern: 
arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+
```

## 🎯 Root Cause

Your `SAGEMAKER_ROLE_ARN` GitHub secret is either:
- ❌ Empty or not set
- ❌ Contains placeholder text (like "your-role-arn-here")
- ❌ Has incorrect format
- ❌ The IAM role doesn't exist in AWS

---

## ✅ SOLUTION: Step-by-Step Fix

### Step 1: Create SageMaker Execution Role in AWS

#### Option A: Using AWS Console (Recommended for Beginners)

1. **Go to AWS IAM Console**
   - Open: https://console.aws.amazon.com/iam/
   - Sign in with your AWS account

2. **Create the Role**
   - Click **"Roles"** in left sidebar
   - Click **"Create role"** button

3. **Select Trusted Entity**
   - Choose: **"AWS service"**
   - Use case: Select **"SageMaker"**
   - Click **"Next"**

4. **Add Permissions**
   - Search and select these policies:
     - ✅ `AmazonSageMakerFullAccess`
     - ✅ `AmazonS3FullAccess`
   - Click **"Next"**

5. **Name the Role**
   - Role name: `SageMakerExecutionRole`
   - Description: `Execution role for SageMaker heart disease predictor`
   - Click **"Create role"**

6. **Copy the Role ARN**
   - Find your new role in the roles list
   - Click on `SageMakerExecutionRole`
   - **COPY** the ARN at the top (looks like this):
     ```
     arn:aws:iam::123456789012:role/SageMakerExecutionRole
     ```
   - **SAVE THIS** - you'll need it for GitHub!

#### Option B: Using AWS CLI (Advanced)

```powershell
# 1. Create trust policy file
@"
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
"@ | Out-File -FilePath trust-policy.json -Encoding utf8

# 2. Create the role
aws iam create-role `
  --role-name SageMakerExecutionRole `
  --assume-role-policy-document file://trust-policy.json

# 3. Attach policies
aws iam attach-role-policy `
  --role-name SageMakerExecutionRole `
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

aws iam attach-role-policy `
  --role-name SageMakerExecutionRole `
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# 4. Get the Role ARN
aws iam get-role --role-name SageMakerExecutionRole --query 'Role.Arn' --output text
```

---

### Step 2: Update GitHub Secret

1. **Go to Your GitHub Repository**
   - Navigate to: https://github.com/YOUR_USERNAME/YOUR_REPO

2. **Open Settings**
   - Click **"Settings"** tab (top right)
   - Click **"Secrets and variables"** → **"Actions"** (left sidebar)

3. **Update or Create Secret**
   
   **If `SAGEMAKER_ROLE_ARN` already exists:**
   - Click on `SAGEMAKER_ROLE_ARN`
   - Click **"Update secret"**
   - Paste your ARN (from Step 1)
   - Click **"Update secret"**

   **If `SAGEMAKER_ROLE_ARN` doesn't exist:**
   - Click **"New repository secret"**
   - Name: `SAGEMAKER_ROLE_ARN`
   - Secret: Paste your ARN (from Step 1)
   - Click **"Add secret"**

4. **Verify Format**
   
   Your ARN should look like:
   ```
   arn:aws:iam::123456789012:role/SageMakerExecutionRole
   ```
   
   ✅ **Correct format:**
   - Starts with `arn:aws:iam::`
   - Has 12-digit account ID
   - Ends with `/role/RoleName`
   - No extra spaces or line breaks

---

### Step 3: Verify All GitHub Secrets

Make sure you have **ALL 4 secrets** configured:

| Secret Name | Example Value | How to Get |
|------------|---------------|------------|
| `AWS_ACCESS_KEY_ID` | `AKIAIOSFODNN7EXAMPLE` | IAM User → Security credentials |
| `AWS_SECRET_ACCESS_KEY` | `wJalrXUtnFEMI/K7MDENG...` | IAM User → Security credentials |
| `S3_BUCKET` | `heart-disease-ml-models-2025` | S3 bucket name you created |
| `SAGEMAKER_ROLE_ARN` | `arn:aws:iam::123456789012:role/...` | From Step 1 above |

---

### Step 4: Verify IAM User Permissions

Your IAM user (the one whose credentials are in `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) needs these permissions:

1. **Go to IAM Console**
   - https://console.aws.amazon.com/iam/

2. **Find Your User**
   - Click **"Users"**
   - Find the user whose credentials you're using

3. **Check Permissions**
   - Click on the user
   - Go to **"Permissions"** tab
   - Ensure these policies are attached:
     - ✅ `AmazonSageMakerFullAccess`
     - ✅ `AmazonS3FullAccess`
     - ✅ `IAMReadOnlyAccess` (to pass the role)

4. **Add Missing Permissions**
   - Click **"Add permissions"** → **"Attach policies directly"**
   - Search and select missing policies
   - Click **"Add permissions"**

---

### Step 5: Test the Fix

#### Option A: Trigger Deployment via Git Push

```powershell
# Make a small change to trigger deployment
cd "c:\Users\Abdul Rehman\OneDrive\Desktop\aiclass\ML_Projects\heart-dicease-system"

# Create a test commit
git add .
git commit -m "Fix: Update IAM role ARN" --allow-empty
git push origin main
```

#### Option B: Manual Workflow Trigger

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click **"Deploy to SageMaker"** workflow
4. Click **"Run workflow"** → **"Run workflow"**

#### Monitor the Deployment

1. Watch the workflow run in GitHub Actions
2. The "Create SageMaker Model" step should now succeed
3. Wait for all steps to complete (~10-15 minutes)

---

## 🔍 Verification Checklist

Before deploying, verify:

- [ ] SageMaker role exists in AWS IAM
- [ ] Role ARN is copied correctly (no typos)
- [ ] GitHub secret `SAGEMAKER_ROLE_ARN` is updated
- [ ] ARN format matches: `arn:aws:iam::XXXXXXXXXXXX:role/RoleName`
- [ ] IAM user has SageMaker permissions
- [ ] All 4 GitHub secrets are configured

---

## 🆘 Still Getting Errors?

### Error: "User is not authorized to perform: iam:PassRole"

**Solution:**
Add this inline policy to your IAM user:

1. IAM Console → Users → Your User
2. Permissions → Add permissions → Create inline policy
3. JSON tab, paste:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::YOUR_ACCOUNT_ID:role/SageMakerExecutionRole"
        }
    ]
}
```

4. Replace `YOUR_ACCOUNT_ID` with your 12-digit AWS account ID
5. Name: `PassRoleToSageMaker`
6. Create policy

### Error: "Role does not exist"

**Solution:**
- Verify the role name is exactly `SageMakerExecutionRole`
- Check you're in the correct AWS region
- Run: `aws iam get-role --role-name SageMakerExecutionRole`

### Error: "Access Denied"

**Solution:**
- Verify AWS credentials in GitHub secrets are correct
- Check IAM user has required permissions
- Ensure credentials haven't expired

---

## 📋 Quick Reference: Valid ARN Format

```
arn:aws:iam::123456789012:role/SageMakerExecutionRole
│   │   │   │            │    │
│   │   │   │            │    └─ Role name
│   │   │   │            └────── "role" literal
│   │   │   └─────────────────── 12-digit account ID
│   │   └─────────────────────── Service (iam)
│   └─────────────────────────── Partition (aws)
└─────────────────────────────── ARN prefix
```

**Components:**
- `arn:aws:iam::` - Fixed prefix
- `123456789012` - Your AWS account ID (12 digits)
- `:role/` - Fixed separator
- `SageMakerExecutionRole` - Your role name

---

## ✅ Success Indicators

You'll know it's fixed when:

1. ✅ GitHub Actions workflow completes without errors
2. ✅ "Create SageMaker Model" step shows green checkmark
3. ✅ You see: "Endpoint is ready!" in the logs
4. ✅ Test endpoint returns predictions

---

## 🎯 Next Steps After Fix

Once deployment succeeds:

```powershell
# 1. Test the endpoint
python test_endpoint.py

# 2. Clean up resources (to avoid charges)
python cleanup.py
```

---

## 📞 Additional Resources

- **AWS IAM Roles**: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html
- **SageMaker Execution Roles**: https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html
- **GitHub Secrets**: https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

**Good luck! This should fix your deployment issue! 🚀**
