# Amazon EKS IRSA Troubleshooting Lab

## Overview

This project demonstrates how to configure **IAM Roles for Service Accounts (IRSA)** in Amazon EKS and troubleshoot an IAM authentication issue where an application is unable to access Amazon DynamoDB due to the pod assuming the **worker node IAM role** instead of the intended **IRSA role**.

## Objectives

- Provision an Amazon EKS cluster
- Create and configure an IAM Role for Service Accounts (IRSA)
- Deploy a Kubernetes pod using a ServiceAccount
- Verify AWS identity from within the pod
- Access an Amazon DynamoDB table using IRSA
- Simulate an IRSA failure
- Troubleshoot and restore access

## Architecture

```text
Kubernetes Pod
      │
      ▼
ServiceAccount (IRSA)
      │
      ▼
IAM Role
      │
      ▼
AWS STS
      │
      ▼
Amazon DynamoDB
```

## Technologies Used

- Amazon EKS
- IAM Roles for Service Accounts (IRSA)
- Amazon DynamoDB
- AWS IAM
- AWS CLI
- kubectl
- eksctl
- Kubernetes

## Project Structure

```text
.
├── README.md
├── manifests/
│   └── pod.yaml
└── iam/
    └── dynamodb-policy.json
```

## Deployment Steps

1. Create an Amazon EKS cluster.
2. Create a DynamoDB table and insert sample data.
3. Associate an IAM OIDC provider with the cluster.
4. Create an IAM policy with DynamoDB read permissions.
5. Create an IRSA-enabled Kubernetes ServiceAccount.
6. Deploy a test pod using the ServiceAccount.
7. Verify the pod assumes the IRSA role.
8. Access the DynamoDB table successfully.

## Failure Simulation

To reproduce the issue:

- Replace the pod's `serviceAccountName` with `default`.
- Redeploy the pod.
- Verify that the pod assumes the **worker node IAM role**.
- Attempt to access DynamoDB and observe the `AccessDeniedException`.

## Troubleshooting

The following checks were performed:

- Verified the Kubernetes ServiceAccount
- Validated the IRSA annotation
- Confirmed AWS identity using `aws sts get-caller-identity`
- Verified the IAM OIDC provider
- Checked IAM role permissions and trust policy
- Restored the correct ServiceAccount configuration

## Outcome

The issue was resolved by configuring the pod to use the correct **IRSA-enabled ServiceAccount**, allowing it to assume the intended IAM role and successfully access Amazon DynamoDB.

## Learning Outcomes

- Amazon EKS authentication
- IAM Roles for Service Accounts (IRSA)
- Kubernetes ServiceAccounts
- AWS STS and IAM role assumption
- DynamoDB access control
- Production-style IAM troubleshooting in EKS
