# GitOps Platform Using ArgoCD

## Overview

This project demonstrates a GitOps-based deployment workflow for applications running on Amazon EKS using ArgoCD. Kubernetes manifests are organized by environment, and ArgoCD continuously synchronizes the desired state stored in Git with the EKS cluster.

## Architecture

```text
Developer
    │
    │ Git Commit / Push
    ▼
GitHub Repository
    │
    ▼
ArgoCD
    │
    ▼
Amazon EKS
```

## Repository Structure

```text
gitops/
├── dev/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── qa/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── prod/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── application-dev.yaml
├── application-qa.yaml
└── application-prod.yaml
```

## Features

* GitOps-based application deployment
* Environment-specific configurations (Dev, QA, Prod)
* Automatic synchronization with ArgoCD
* Self-healing of configuration drift
* Automatic pruning of removed Kubernetes resources
* Continuous deployment to Amazon EKS

## Prerequisites

* AWS Account
* Amazon EKS Cluster
* kubectl
* AWS CLI
* Git
* ArgoCD installed on the cluster

## Deployment Workflow

1. Update Kubernetes manifests.
2. Commit and push changes to Git.
3. ArgoCD detects the changes automatically.
4. ArgoCD synchronizes the manifests with the EKS cluster.
5. The application is deployed without manual intervention.

## ArgoCD Sync Policy

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
```

## Validation

Verify ArgoCD applications:

```bash
kubectl get applications -n argocd
```

Verify workloads:

```bash
kubectl get pods -A
```

## Technologies Used

* Amazon EKS
* Kubernetes
* ArgoCD
* Git & GitHub
* YAML

## Key Concepts

* **GitOps:** Git is the single source of truth for Kubernetes deployments.
* **Auto Sync:** Automatically applies changes committed to Git.
* **Self Heal:** Restores the cluster to the desired state if manual changes occur.
* **Pruning:** Removes Kubernetes resources that have been deleted from the Git repository.
