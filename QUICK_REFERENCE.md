# 🚀 Quick Reference Card

## 📋 GitHub Secrets Required

| Secret Name | Example Value | Description |
|------------|---------------|-------------|
| `AWS_ACCESS_KEY_ID` | `AKIAIOSFODNN7EXAMPLE` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | `wJalrXUtnFEMI/K7MDENG/...` | AWS secret key |
| `S3_BUCKET` | `heart-disease-ml-models-2025` | S3 bucket name |
| `SAGEMAKER_ROLE_ARN` | `arn:aws:iam::123456789012:role/...` | SageMaker role ARN |

---

## 🔧 Local Commands

### Train Model
```bash
python train_and_save.py
```

### Test Inference Locally
```bash
python inference.py
```

### Test Deployed Endpoint
```bash
python test_endpoint.py
```

### Cleanup Resources
```bash
python cleanup.py
```

---

## ☁️ AWS CLI Commands

### Deploy Manually (if not using GitHub Actions)

```bash
# 1. Package model
tar -czf model.tar.gz model.joblib inference.py

# 2. Upload to S3
aws s3 cp model.tar.gz s3://YOUR_BUCKET/models/heart-disease/model.tar.gz

# 3. Create model
aws sagemaker create-model \
  --model-name heart-disease-predictor \
  --primary-container Image=683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3,ModelDataUrl=s3://YOUR_BUCKET/models/heart-disease/model.tar.gz \
  --execution-role-arn arn:aws:iam::YOUR_ACCOUNT:role/SageMakerRole

# 4. Create endpoint config
aws sagemaker create-endpoint-config \
  --endpoint-config-name heart-disease-predictor-config \
  --production-variants VariantName=AllTraffic,ModelName=heart-disease-predictor,InitialInstanceCount=1,InstanceType=ml.t2.medium

# 5. Create endpoint
aws sagemaker create-endpoint \
  --endpoint-name heart-disease-predictor \
  --endpoint-config-name heart-disease-predictor-config
```

### Test Endpoint

```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name heart-disease-predictor \
  --content-type application/json \
  --body '{"instances": [[63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]]}' \
  output.json
```

### Cleanup

```bash
aws sagemaker delete-endpoint --endpoint-name heart-disease-predictor
aws sagemaker delete-endpoint-config --endpoint-config-name heart-disease-predictor-config
aws sagemaker delete-model --model-name heart-disease-predictor
```

---

## 🐍 Python Test Code

```python
import boto3
import json

# Initialize client
client = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Test data (13 features)
test_input = {
    "instances": [
        [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]  # High risk
    ]
}

# Make prediction
response = client.invoke_endpoint(
    EndpointName='heart-disease-predictor',
    ContentType='application/json',
    Body=json.dumps(test_input)
)

# Parse result
result = json.loads(response['Body'].read())
print(f"Prediction: {result['predictions'][0]}")
print(f"Risk Score: {result['risk_scores'][0]:.2%}")
```

---

## 📊 Input Features (Order Matters!)

1. **age** - Age in years (29-77)
2. **sex** - 1=male, 0=female
3. **cp** - Chest pain type (0-3)
4. **trestbps** - Resting blood pressure (94-200)
5. **chol** - Cholesterol mg/dl (126-564)
6. **fbs** - Fasting blood sugar >120 (1=true, 0=false)
7. **restecg** - Resting ECG (0-2)
8. **thalach** - Max heart rate (71-202)
9. **exang** - Exercise angina (1=yes, 0=no)
10. **oldpeak** - ST depression (0-6.2)
11. **slope** - ST slope (0-2)
12. **ca** - Major vessels (0-4)
13. **thal** - Thalassemia (0-3)

---

## 🔍 Expected Output

```json
{
    "predictions": [1],
    "risk_scores": [0.87]
}
```

- **predictions**: `0` = No Disease, `1` = Disease
- **risk_scores**: Probability (0.0 to 1.0)

---

## 🛠️ Troubleshooting Quick Fixes

### Error: "ValidationException" (IAM Role ARN)
**Most Common Issue!**
```bash
# Fix: See QUICK_FIX.md or FIX_IAM_ROLE_ERROR.md
# Verify your setup:
python verify_aws_setup.py

# Check role ARN format
aws iam get-role --role-name SageMakerExecutionRole
```

### Error: "ResourceNotFound"
```bash
# Check if endpoint exists
aws sagemaker describe-endpoint --endpoint-name heart-disease-predictor
```

### Error: "AccessDenied"
```bash
# Check IAM permissions
aws iam list-attached-user-policies --user-name github-actions-sagemaker
```

### Error: Model not loading
```bash
# Verify model file
python -c "import joblib; model = joblib.load('model.joblib'); print('Model loaded successfully')"
```

---

## 📁 Project Files Overview

| File | Purpose |
|------|---------|
| `train_and_save.py` | Train model & save as joblib |
| `inference.py` | SageMaker inference handler |
| `requirements.txt` | Python dependencies |
| `test_endpoint.py` | Test deployed endpoint |
| `cleanup.py` | Delete AWS resources |
| `.github/workflows/deploy.yml` | CI/CD pipeline |

---

## 💡 Pro Tips

1. **Always cleanup** after testing to avoid charges
2. **Use ml.t2.medium** for cost-effective testing
3. **Monitor CloudWatch** for endpoint logs
4. **Version your models** in S3 with timestamps
5. **Test locally first** before deploying

---

## 🔗 Useful Links

- [SageMaker Console](https://console.aws.amazon.com/sagemaker/)
- [S3 Console](https://console.aws.amazon.com/s3/)
- [IAM Console](https://console.aws.amazon.com/iam/)
- [CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/)

---

## 📞 Emergency Commands

### Stop Everything
```bash
python cleanup.py
```

### Check Costs
```bash
aws ce get-cost-and-usage \
  --time-period Start=2025-10-01,End=2025-10-03 \
  --granularity DAILY \
  --metrics BlendedCost
```

### List All Endpoints
```bash
aws sagemaker list-endpoints
```

---

**Keep this card handy during deployment! 📌**
