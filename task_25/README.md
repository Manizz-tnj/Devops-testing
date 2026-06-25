# Observability Platform Deployment

## Overview
This project implements a complete observability stack for monitoring system metrics, logs, and distributed traces using open-source tools. It is designed for local deployment using Docker Compose and serves as a foundation for understanding modern DevOps observability practices.

The stack provides unified visibility into infrastructure and application behavior through Grafana dashboards.

---

## Objectives
- Collect and visualize system and application metrics
- Centralize log management
- Enable distributed tracing
- Build real-time monitoring dashboards
- Understand observability fundamentals (Metrics, Logs, Traces)

---

## Tech Stack
- Prometheus – Metrics collection and monitoring
- Grafana – Visualization and dashboards
- Loki – Log aggregation system
- Tempo – Distributed tracing backend
- Grafana Alloy – Telemetry collector
- Node Exporter – System metrics exporter
- Docker Compose – Container orchestration

---

## Architecture
Node Exporter → Prometheus → Grafana (Metrics)  
Application Logs → Alloy → Loki → Grafana (Logs)  
Application Traces → Tempo → Grafana (Traces)

---

## Project Structure
observability-stack/
├── docker-compose.yml
├── prometheus.yml
├── alloy-config.alloy
└── README.md

---

## Prerequisites
Install the following tools:
- Docker Desktop
- Docker Compose
- Git
- VS Code (recommended)

Verify installation:
docker --version
docker compose version
git --version

---

## Setup Instructions

### 1. Create Project Directory
mkdir observability-stack
cd observability-stack

---

### 2. Start Services
docker compose up -d

Verify running containers:
docker ps

---

## Access Services

Grafana → http://localhost:3000  
Prometheus → http://localhost:9090  
Node Exporter → http://localhost:9100  
Loki → http://localhost:3100  
Tempo → http://localhost:3200  

---

## Grafana Login
Username: admin  
Password: admin  

---

## Dashboards

### CPU Usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)

---

### Memory Usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/
node_memory_MemTotal_bytes * 100

---

### Request Rate
rate(http_requests_total[1m])

---

### Error Rate
rate(http_requests_total{status=~"5.."}[1m])

---

## Features
- Infrastructure monitoring
- Log aggregation
- Distributed tracing
- Real-time dashboards
- Docker-based deployment

---

## Cleanup Commands

Stop services:
docker compose down

Remove containers:
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

Remove images:
docker rmi -f $(docker images -aq)

Full cleanup:
docker system prune -a --volumes -f

---

## Learning Outcomes
- Understanding observability concepts
- Working with Prometheus metrics
- Creating Grafana dashboards
- Log management using Loki
- Distributed tracing with Tempo
- Containerized DevOps workflows

---

## Future Improvements
- Kubernetes deployment using Helm charts
- OpenTelemetry integration
- Alerting with Prometheus Alertmanager
- Production-grade security and authentication

---

## Author
Observability Stack Project (DevOps Learning)
