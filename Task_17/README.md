# Exercise 17: Implement IRSA for Application Access

## Objective
Configure an EKS application to access DynamoDB securely using IRSA (IAM Roles for Service Accounts) without AWS Access Keys.

## Services Used
- Amazon EKS
- IAM
- IRSA
- DynamoDB
- Amazon ECR
- Docker

## Architecture

Application Pod
↓
Service Account
↓
IAM Role (IRSA)
↓
DynamoDB

## Implementation Steps

### 1. Create EKS Cluster
```bash
eksctl create cluster \
--name payment-cluster \
--region ap-south-1 \
--nodegroup-name workers \
--node-type t3.medium \
--nodes 2
```

### 2. Create DynamoDB Table
```bash
aws dynamodb create-table \
--table-name customer-data \
--attribute-definitions AttributeName=id,AttributeType=S \
--key-schema AttributeName=id,KeyType=HASH \
--billing-mode PAY_PER_REQUEST
```

### 3. Enable OIDC Provider
```bash
eksctl utils associate-iam-oidc-provider \
--cluster payment-cluster \
--approve
```

### 4. Create IAM Policy
Allow:
- GetItem
- PutItem
- UpdateItem

on DynamoDB table `customer-data`.

### 5. Create IAM Service Account
```bash
eksctl create iamserviceaccount \
--cluster payment-cluster \
--namespace default \
--name dynamodb-sa \
--attach-policy-arn <POLICY_ARN> \
--approve
```

### 6. Build and Push Application Image
```bash
docker build -t dynamodb-app .
docker push <ECR-IMAGE-URI>
```

### 7. Deploy Application
Configure deployment to use:

```yaml
serviceAccountName: dynamodb-sa
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

### 8. Verification
Check pod logs:

```bash
kubectl logs <pod-name>
```

Expected:
```text
PutItem Success
UpdateItem Success
```

Verify IAM Role:

```bash
kubectl describe sa dynamodb-sa
```

Verify STS Identity:

```bash
kubectl exec -it <pod-name> -- aws sts get-caller-identity
```

## Validation Checklist

- [x] EKS Cluster Created
- [x] DynamoDB Table Created
- [x] OIDC Enabled
- [x] IAM Policy Created
- [x] IAM Role Attached
- [x] Service Account Configured
- [x] Application Deployed
- [x] DynamoDB Access Successful
- [x] No AWS Access Keys Used

## Outcome

The application successfully performs GetItem, PutItem, and UpdateItem operations on DynamoDB using IRSA-based authentication, following AWS security best practices.
