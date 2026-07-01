# Secret Rotation Outage – Kubernetes Incident Lab

## Overview

This lab simulates a production incident where an application fails authentication after a secret rotation. Although the Kubernetes Secret has been updated, the running application continues using the old secret, resulting in authentication failures.

The objective is to investigate the incident, identify why the rotated secret did not propagate to the application, and restore normal operation.

---

## Incident

**Application Error**

```text
401 Unauthorized
```

**Application Logs**

```text
Token validation failed
```

**Kubernetes Secret**

```bash
kubectl get secret payment-secret
```

```text
Last Updated: 2 weeks ago
```

---

## Objectives

* Investigate the authentication failure.
* Verify the Kubernetes Secret.
* Determine why the rotated secret was not propagated.
* Restore the application using the updated secret.

---

## Environment

* Kubernetes (Kind Cluster)
* Docker Desktop
* kubectl
* BusyBox (Application Simulation)

---

## Project Structure

```text
task_13/
├── payment-secret.yaml
└── payment.yaml
```

---

## Deployment

Create the Kind cluster.

```bash
kind create cluster --name secret-lab
```

Create the namespace.

```bash
kubectl create namespace secret-lab
```

Deploy the Secret and application.

```bash
kubectl apply -f payment-secret.yaml
kubectl apply -f payment.yaml
```

Verify resources.

```bash
kubectl get pods -n secret-lab
kubectl get secret -n secret-lab
```

---

## Incident Simulation

Rotate the Secret by updating the token value in `payment-secret.yaml`.

```yaml
TOKEN: new-token
```

Apply the updated Secret.

```bash
kubectl apply -f payment-secret.yaml
```

Although the Secret is updated, the running Pod continues using the old token because environment variables are loaded only during container startup.

---

## Investigation Steps

### Check Pod Status

```bash
kubectl get pods -n secret-lab
```

### Review Application Logs

```bash
kubectl logs deployment/payment-service -n secret-lab
```

### Verify Kubernetes Secret

```bash
kubectl describe secret payment-secret -n secret-lab
```

### Verify Deployment Configuration

```bash
kubectl describe deployment payment-service -n secret-lab
```

### Restart the Application

```bash
kubectl rollout restart deployment/payment-service -n secret-lab
```

---

## Root Cause Analysis

| Investigation     | Result                                                                                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Application       | 401 Unauthorized                                                                                                                                     |
| Logs              | Token validation failed                                                                                                                              |
| Kubernetes Secret | Updated Successfully                                                                                                                                 |
| Running Pod       | Continued using old token                                                                                                                            |
| Root Cause        | Secret rotation did not propagate because the application consumed the Secret as an environment variable, which is loaded only at container startup. |

---

## Resolution

Restart the deployment to load the updated Secret.

```bash
kubectl rollout restart deployment/payment-service -n secret-lab
```

Verify the application.

```bash
kubectl logs deployment/payment-service -n secret-lab
```

Expected output:

```text
Application Started
Current Token: new-token
Authentication Successful
```

---

## Production Troubleshooting Workflow

```text
Authentication Failure
        │
        ▼
Review Application Logs
        │
        ▼
Inspect Kubernetes Secret
        │
        ▼
Verify Secret Update
        │
        ▼
Check Pod Configuration
        │
        ▼
Restart Deployment
        │
        ▼
Verify Application Health
```

---

## Key Learnings

* Understand Kubernetes Secret lifecycle.
* Investigate authentication failures caused by stale secrets.
* Verify Secret updates using `kubectl`.
* Learn that environment variables sourced from Secrets are read only during container startup.
* Apply a production-style troubleshooting workflow for secret rotation incidents.

---

## Cleanup

Delete the namespace.

```bash
kubectl delete namespace secret-lab
```

Delete the Kind cluster.

```bash
kind delete cluster --name secret-lab
```

---

**Note:** In production, secret rotation is commonly managed by external secret providers such as AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault. If secret synchronization or pod restart mechanisms are not configured, applications may continue using stale credentials even after the secret has been successfully rotated.
