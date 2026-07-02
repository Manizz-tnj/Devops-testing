# Exercise 15 – Complete Production Outage Investigation

## Overview

This project demonstrates a production incident investigation in a Kubernetes environment involving GitOps, secret management, and application dependency failures.

The objective is to identify the root cause of an application outage by investigating multiple infrastructure components and performing a complete Root Cause Analysis (RCA).

---

## Incident Scenario

**Timeline**

* **08:55** – Redis credentials rotated in Secret Manager.
* **09:00** – Application deployment completed successfully.
* **09:05** – Users reported **HTTP 503 Service Unavailable**.

### Available Evidence

* ArgoCD: **Healthy**
* Application Pods: **Running**
* Ingress: **Healthy**
* Application Logs: `Cannot connect to Redis`
* Redis Logs: `Authentication failed`
* Secret Manager: Secret rotated at **08:55**

---

## Objective

Investigate the production outage by analyzing:

* ArgoCD deployment status
* Secret Manager
* External Secrets synchronization
* Kubernetes Secret
* Application logs
* Redis logs

Deliver:

* Incident Timeline
* Root Cause Analysis (RCA)
* Immediate Resolution
* Long-Term Preventive Actions
* Monitoring and Alerting Improvements

---

## Technology Stack

* Kubernetes (Kind)
* Docker
* Helm
* ArgoCD
* External Secrets Operator
* Redis
* Grafana
* Prometheus
* Loki
* Tempo
* kubectl

---

## Project Structure

```text
task_15/
│
├── README.md
├── install.cmd
├── deploy.cmd
├── cleanup.cmd
│
├── argocd/
│   ├── application.yaml
│   └── project.yaml
│
├── external-secrets/
│   ├── namespace.yaml
│   ├── secretstore.yaml
│   ├── source-secret.yaml
│   ├── externalsecret.yaml
│   └── kubernetes-secret.yaml
│
├── redis/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
│
├── app/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── ingress.yaml
│
├── monitoring/
│   ├── grafana-values.yaml
│   ├── prometheus-values.yaml
│   ├── loki-values.yaml
│   └── tempo-values.yaml
│
├── scripts/
│   ├── rotate-secret.cmd
│   ├── verify-secret.cmd
│   ├── generate-traffic.cmd
│   └── restart-app.cmd
│
└── docs/
    ├── investigation.md
    ├── root-cause-analysis.md
    ├── timeline.md
    └── lessons-learned.md
```

---

## Deployment

### Create the Kind Cluster

```bash
kind create cluster --name production-outage
```

### Deploy the Environment

```bash
install.cmd
```

```bash
deploy.cmd
```

Verify resources:

```bash
kubectl get pods -A
```

---

## Investigation Workflow

1. Verify ArgoCD application health.
2. Check Kubernetes Pods and Ingress.
3. Review application logs.
4. Inspect Redis logs.
5. Verify Secret Manager rotation.
6. Check External Secret synchronization.
7. Compare Kubernetes Secret with the latest secret.
8. Identify the authentication failure.
9. Validate application recovery after secret synchronization.

---

## Root Cause

The Redis password was rotated in Secret Manager before the application deployment. The updated credential was not synchronized to the Kubernetes Secret before the application started, causing the application to use stale credentials. Redis rejected authentication requests, resulting in application failures and HTTP 503 responses.

---

## Resolution

* Synchronize the updated secret from Secret Manager.
* Verify the Kubernetes Secret has been updated.
* Restart the application deployment.
* Confirm successful Redis authentication.
* Validate application availability.

---

## Monitoring Improvements

Implement alerts for:

* HTTP 503 error rate
* Redis authentication failures
* External Secret synchronization failures
* Secret rotation events
* Kubernetes Secret age
* Application latency
* Pod restart count
* Redis availability

---

## Learning Outcomes

This project demonstrates practical experience with:

* Kubernetes Troubleshooting
* GitOps using ArgoCD
* Secret Management
* External Secrets Operator
* Redis Authentication
* Distributed Observability
* Production Incident Response
* Root Cause Analysis (RCA)
* DevOps and Site Reliability Engineering (SRE)

---

## Cleanup

Delete all deployed resources:

```bash
cleanup.cmd
```

Or remove the Kind cluster:

```bash
kind delete cluster --name production-outage
```
