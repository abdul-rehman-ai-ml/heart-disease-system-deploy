# ⚡ QUICK FIX: IAM Role ARN Error

## 🎯 The Problem
Your GitHub Actions deployment is failing with:
```
Value '***' at 'executionRoleArn' failed to satisfy constraint
```

## ✅ The Solution (5 Minutes)

### Step 1: Create IAM Role (2 min)
1. Go to: https://console.aws.amazon.com/iam/
2. Click **Roles** → **Create role**
3. Select **AWS service** → **SageMaker** → **Next**
4. Select **AmazonSageMakerFullAccess** → **Next**
5. Role name: `SageMakerExecutionRole` → **Create role**
6. Click on the role → **Copy the ARN** (looks like `arn:aws:iam::123456789012:role/SageMakerExecutionRole`)

### Step 2: Update GitHub Secret (2 min)
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Find `SAGEMAKER_ROLE_ARN` → **Update secret**
3. Paste the ARN from Step 1
4. Click **Update secret**

### Step 3: Verify Setup (1 min)
Run this in PowerShell:
```powershell
cd "c:\Users\Abdul Rehman\OneDrive\Desktop\aiclass\ML_Projects\heart-dicease-system"
python verify_aws_setup.py
```

### Step 4: Deploy Again
```powershell
git add .
git commit -m "Fix: Update IAM role ARN" --allow-empty
git push origin main
```

---

## 📋 Checklist

- [ ] Created `SageMakerExecutionRole` in AWS IAM
- [ ] Copied the Role ARN (starts with `arn:aws:iam::`)
- [ ] Updated GitHub secret `SAGEMAKER_ROLE_ARN`
- [ ] Ran `verify_aws_setup.py` (all checks passed)
- [ ] Pushed code to trigger deployment

---

## 🆘 Still Not Working?

### Check 1: Verify ARN Format
Your ARN should look like:
```
arn:aws:iam::123456789012:role/SageMakerExecutionRole
```

**NOT like:**
- ❌ `your-role-arn-here`
- ❌ `***`
- ❌ Empty/blank
- ❌ `arn:aws:iam:::role/...` (missing account ID)

### Check 2: Verify All 4 GitHub Secrets
Go to: Settings → Secrets and variables → Actions

You should have:
1. ✅ `AWS_ACCESS_KEY_ID`
2. ✅ `AWS_SECRET_ACCESS_KEY`
3. ✅ `S3_BUCKET`
4. ✅ `SAGEMAKER_ROLE_ARN`

### Check 3: Verify IAM User Permissions
Your IAM user needs:
- ✅ `AmazonSageMakerFullAccess`
- ✅ `AmazonS3FullAccess`
- ✅ Permission to pass the role

---

## 📖 Need More Details?

See **FIX_IAM_ROLE_ERROR.md** for comprehensive guide

---

## ✨ Success Looks Like

When fixed, GitHub Actions will show:
```
✅ Create SageMaker Model
✅ Create Endpoint Config
✅ Create or Update Endpoint
✅ Wait for Endpoint
✅ Test Endpoint
✅ Deployment Complete!
```

**Good luck! 🚀**
