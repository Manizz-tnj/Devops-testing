\# Task 24 - EKS + IRSA + DynamoDB Integration



\## Objective

Deploy a containerized application on EKS that performs DynamoDB operations using IRSA (no AWS access keys).



\---



\## Architecture

Application Pod → ServiceAccount → IRSA Role → IAM Policy → DynamoDB



\---



\## Prerequisites

\- EKS cluster

\- kubectl configured

\- AWS CLI configured

\- Docker + ECR repository



\---



\## Steps



\### 1. Create DynamoDB Table

```bash

aws dynamodb create-table \\

\--table-name CustomerTable \\

\--attribute-definitions AttributeName=CustomerId,AttributeType=S \\

\--key-schema AttributeName=CustomerId,KeyType=HASH \\

\--billing-mode PAY\_PER\_REQUEST

```



\---



\### 2. Create IAM Policy

Allow:

\- GetItem

\- PutItem

\- UpdateItem

\- Scan



Attach to role.



\---



\### 3. Create IRSA Service Account

```bash

eksctl create iamserviceaccount \\

\--cluster eks-lab \\

\--namespace default \\

\--name dynamo-app-sa \\

\--attach-policy-arn arn:aws:iam::<ACCOUNT\_ID>:policy/DynamoDBAccessPolicy \\

\--approve

```



\---



\### 4. Build \& Push Docker Image

```bash

docker build -t dynamo-app .



docker tag dynamo-app:latest <ECR\_URI>



docker push <ECR\_URI>

```



\---



\### 5. Deploy to EKS

```yaml

apiVersion: apps/v1

kind: Deployment

metadata:

&#x20; name: dynamo-app

spec:

&#x20; replicas: 1

&#x20; selector:

&#x20;   matchLabels:

&#x20;     app: dynamo-app

&#x20; template:

&#x20;   metadata:

&#x20;     labels:

&#x20;       app: dynamo-app

&#x20;   spec:

&#x20;     serviceAccountName: dynamo-app-sa

&#x20;     containers:

&#x20;     - name: app

&#x20;       image: <ECR\_URI>

```



```bash

kubectl apply -f deployment.yaml

```



\---



\### 6. Verify

```bash

kubectl get pods

kubectl logs <pod-name>

aws dynamodb scan --table-name CustomerTable

```



\---



\## Outcome

Secure EKS deployment using IRSA with successful DynamoDB integration without AWS credentials.

