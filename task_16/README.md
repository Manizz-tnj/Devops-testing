# Production EKS Platform using Terraform

## Overview

This project builds a production-ready Kubernetes cluster on AWS using EKS and Terraform.

It creates a VPC, EKS cluster, and networking setup required for Kubernetes workloads.

The infrastructure is modular and can be extended with node groups, autoscaling, and monitoring.

---

## What is included

- VPC with public subnets
- Internet Gateway and routing
- EKS cluster (control plane)
- IAM role for EKS
- Terraform modular structure
- Kubernetes access using kubectl

---

## Architecture Flow

Terraform
  |
  |--> VPC
  |--> Subnets
  |--> Internet Gateway
  |--> Route Tables
  |--> EKS Cluster
  |
  ---> Kubernetes Access (kubectl)

---

## Project Structure

task_16/
|
|-- main.tf                (root module)
|-- provider.tf
|-- versions.tf
|
|-- modules/
|     |-- vpc/
|     |     |-- main.tf
|     |     |-- outputs.tf
|     |
|     |-- eks/
|           |-- main.tf
|           |-- variables.tf
|           |-- outputs.tf
|
|-- README.md

---

## Prerequisites

Install the following tools:

- AWS CLI
- Terraform
- kubectl
- Helm (optional)

Check versions:

aws --version
terraform version
kubectl version --client

---

## Setup Steps

1. Configure AWS

aws configure

Make sure your IAM user has EKS permissions.

---

2. Initialize Terraform

terraform init

---

3. Validate configuration

terraform validate

---

4. Plan infrastructure

terraform plan

---

5. Apply infrastructure

terraform apply

Type "yes" when prompted.

---

## Connect to Kubernetes cluster

aws eks update-kubeconfig --region ap-south-1 --name production-eks

---

## Verify cluster

kubectl get nodes

kubectl get ns

---

## Cleanup

terraform destroy

---

## What you learn

- AWS VPC networking
- EKS cluster creation
- Terraform modules
- Kubernetes basics
- Infrastructure as Code workflow

---

## Important Notes

- This setup creates only the EKS control plane initially
- Worker nodes (node group) must be added separately
- Always destroy resources when not needed to avoid AWS charges
