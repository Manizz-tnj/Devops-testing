# Payment Service - EKS GitOps Deployment

## Project Overview

This project demonstrates deploying a Python Flask-based **Payment Service** to **Amazon EKS** using a modern **GitOps** workflow.

The application is containerized using Docker, stored in Amazon ECR, deployed using Helm, synchronized with ArgoCD, exposed through AWS ALB Ingress, and monitored using Prometheus and Grafana.

---

## Architecture

```
Developer
    │
    │ Git Push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
(Build & Push Docker Image)
    │
    ▼
Amazon ECR
    │
    ▼
ArgoCD (GitOps)
    │
    ▼
Amazon EKS
    │
    ▼
AWS ALB Ingress
    │
    ▼
End Users

                 │
                 ▼
        Prometheus + Grafana
```

---

## Tech Stack

- Python 3.12
- Flask
- Docker
- Kubernetes
- Helm
- Amazon EKS
- Amazon ECR
- GitHub Actions
- ArgoCD
- AWS Secrets Manager
- IAM Roles for Service Accounts (IRSA)
- AWS Load Balancer Controller
- Prometheus
- Grafana

---

## Project Structure

```
payment-service/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
│
├── helm/
│   └── payment-service/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── namespace.yaml
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
└── docs/
    └── architecture.png
```

---

# Features

- Flask REST API
- Dockerized Application
- Helm Chart Deployment
- GitOps using ArgoCD
- GitHub Actions CI Pipeline
- Amazon ECR Image Repository
- Amazon EKS Deployment
- AWS Secrets Manager Integration
- IRSA Authentication
- AWS ALB Ingress
- Prometheus Monitoring
- Grafana Dashboard

---

# Prerequisites

- AWS Account
- Docker Desktop
- Git
- kubectl
- Helm
- eksctl
- AWS CLI
- GitHub Account

---

# Run Application Locally

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open

```
http://localhost:5000
```

---

# Build Docker Image

```bash
docker build -t payment-service:v1 .
```

Run container

```bash
docker run -d -p 5000:5000 payment-service:v1
```

---

# Push Image to Amazon ECR

Login

```bash
aws configure
```

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

Tag Image

```bash
docker tag payment-service:v1 <ECR_URI>:v1
```

Push Image

```bash
docker push <ECR_URI>:v1
```

---

# Create Amazon EKS Cluster

```bash
eksctl create cluster --name payment-cluster --region ap-south-1 --nodes 2
```

Verify

```bash
kubectl get nodes
```

---

# Deploy Using Helm

Create chart

```bash
helm create payment-service
```

Deploy

```bash
helm install payment ./helm/payment-service
```

Check

```bash
kubectl get pods
```

---

# Install ArgoCD

```bash
kubectl create namespace argocd
```

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

# Configure GitOps

- Push Helm chart changes to GitHub.
- ArgoCD detects repository changes.
- Automatic deployment to Amazon EKS.

---

# AWS Secrets Manager

Store sensitive information such as:

- Database Username
- Database Password
- API Keys

Secrets are securely accessed by Pods using **IRSA** and **Secrets Store CSI Driver**.

---

# Configure ALB Ingress

Deploy AWS Load Balancer Controller and expose the application through an Internet-facing Application Load Balancer.

---

# Monitoring

Install Prometheus

```bash
helm install prometheus prometheus-community/prometheus
```

Install Grafana

```bash
helm install grafana grafana/grafana
```

View metrics such as:

- CPU Usage
- Memory Usage
- Pod Restarts
- Network Traffic
- Request Rate

---

# CI/CD Workflow

```
Developer
      │
      ▼
Git Push
      │
      ▼
GitHub Actions
      │
      ▼
Docker Build
      │
      ▼
Amazon ECR
      │
      ▼
Update Helm Chart
      │
      ▼
GitOps Repository
      │
      ▼
ArgoCD Auto Sync
      │
      ▼
Amazon EKS
      │
      ▼
Application Running
```

---

# Future Enhancements

- Horizontal Pod Autoscaler (HPA)
- SSL using AWS ACM
- ExternalDNS
- Multi-environment deployment (Dev, QA, Prod)
- Terraform Infrastructure as Code
- SonarQube Code Analysis
- Trivy Image Scanning

---

# Author

**Manikandan**

DevOps | AWS | Kubernetes | Docker | GitHub Actions | ArgoCD
