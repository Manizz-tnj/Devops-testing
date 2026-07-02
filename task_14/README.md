# Exercise 14 – Distributed Tracing Investigation using Kind, Grafana, Prometheus, Loki & Tempo

## Project Overview

This project demonstrates how to investigate application latency in a Kubernetes-based microservices environment using the Grafana Observability Stack.

The objective is to identify the root cause of a slow Checkout API by correlating **metrics**, **logs**, and **distributed traces**.

The lab is deployed locally using a **Kind (Kubernetes in Docker)** cluster and uses the following observability tools:

* Grafana
* Prometheus
* Loki
* Tempo
* OpenTelemetry Demo Application

---

## Incident Scenario

### Reported Issue

Users report that the Checkout API is responding slowly.

### Observations

* 95th Percentile Latency: **4.8 seconds**
* Request Count: **Normal**
* Distributed Trace:

```
Checkout Service
        │
        ▼
Product Catalog / Inventory Service
        │
        ▼
Payment Service
```

The distributed trace indicates that the **Payment Service** is taking approximately **4.2 seconds**, resulting in increased overall API response time.

---

## Objective

The purpose of this exercise is to:

* Deploy a Kubernetes cluster using Kind
* Install the Grafana observability stack
* Deploy an OpenTelemetry-enabled microservices application
* Generate application traffic
* Collect metrics, logs, and traces
* Identify the service responsible for high latency
* Perform a complete Root Cause Analysis (RCA)

---

## Technology Stack

| Component     | Purpose                  |
| ------------- | ------------------------ |
| Kind          | Local Kubernetes Cluster |
| Kubernetes    | Container Orchestration  |
| Helm          | Package Management       |
| Grafana       | Visualization Dashboard  |
| Prometheus    | Metrics Collection       |
| Loki          | Log Aggregation          |
| Tempo         | Distributed Tracing      |
| OpenTelemetry | Trace Instrumentation    |
| Docker        | Container Runtime        |

---

## Project Structure

```
task_14/
│
├── README.md
├── install-observability.cmd
├── deploy-demo.cmd
├── cleanup.cmd
│
├── monitoring/
│   ├── grafana-values.yaml
│   ├── prometheus-values.yaml
│   ├── tempo-values.yaml
│   └── loki-values.yaml
│
└── docs/
    ├── investigation.md
    └── root-cause-analysis.md
```

---

## Prerequisites

Ensure the following software is installed:

* Docker Desktop
* Kind
* kubectl
* Helm
* Git

Verify installation:

```bash
docker --version
kind --version
kubectl version --client
helm version
git --version
```

---

## Environment Setup

### 1. Create Kind Cluster

```bash
kind create cluster --name tracing-lab
```

Verify:

```bash
kubectl get nodes
```

---

### 2. Create Namespace

```bash
kubectl create namespace observability
```

---

### 3. Install Observability Stack

Install:

* Prometheus
* Grafana
* Loki
* Tempo

using Helm.

Verify:

```bash
kubectl get pods -n observability
```

All pods should be in the **Running** state.

---

### 4. Deploy OpenTelemetry Demo

Deploy the sample microservices application.

Verify:

```bash
kubectl get pods
```

Expected services include:

* frontend
* checkoutservice
* paymentservice
* productcatalogservice
* cartservice
* recommendationservice

---

## Investigation Workflow

### Step 1 – Verify Metrics

Open Grafana and navigate to the Prometheus dashboards.

Observe:

* Request Rate
* Error Rate
* 95th Percentile Latency

Finding:

```
95th Percentile Latency ≈ 4.8 seconds
```

This indicates high response latency despite normal request volume.

---

### Step 2 – Review Logs

Open Grafana Explore.

Select Loki.

Inspect logs for:

* checkoutservice
* paymentservice

Identify log entries indicating delayed payment processing.

---

### Step 3 – Analyze Distributed Trace

Open Grafana Explore.

Select Tempo.

Locate a recent trace.

Example:

```
Frontend

↓

Checkout Service

↓

Product Catalog Service

↓

Payment Service
```

Trace Duration:

```
Checkout Service
220 ms

↓

Product Catalog
310 ms

↓

Payment Service
4200 ms
```

The Payment Service consumes most of the request time.

---

## Root Cause

The distributed trace confirms that **Payment Service** introduces approximately **4.2 seconds** of latency.

Since every upstream service waits for the payment response, the overall Checkout API latency increases to approximately **4.8 seconds**.

---

## Resolution

Possible corrective actions include:

* Optimize payment processing logic
* Reduce external API response time
* Implement request timeout policies
* Introduce asynchronous processing where applicable
* Cache reusable payment metadata
* Monitor latency using Grafana alerts

---

## Expected Outcome

After completing this lab, you will be able to:

* Deploy a Kubernetes observability stack
* Collect metrics using Prometheus
* Aggregate logs with Loki
* Analyze distributed traces using Tempo
* Correlate metrics, logs, and traces
* Identify application bottlenecks
* Perform production-style incident investigations
* Produce a professional Root Cause Analysis

---

## Cleanup

Delete the demo application:

```bash
kubectl delete -f demo.yaml
```

Delete the observability stack:

```bash
helm uninstall grafana -n observability
helm uninstall prometheus -n observability
helm uninstall tempo -n observability
helm uninstall loki -n observability
```

Delete the Kind cluster:

```bash
kind delete cluster --name tracing-lab
```

---

## Learning Outcomes

This project demonstrates practical experience with:

* Kubernetes Troubleshooting
* Site Reliability Engineering (SRE)
* DevOps Monitoring
* Distributed Tracing
* Observability Engineering
* Incident Response
* Root Cause Analysis
* Production Debugging

These skills are directly applicable to modern cloud-native and Kubernetes-based production environments.
