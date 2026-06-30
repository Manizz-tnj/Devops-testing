# Exercise 6 – EKS Node Scale Failure

## Scenario

An application deployed on Amazon EKS is unable to scale despite increased CPU utilization.

### Incident

```
HPA Status

Desired Replicas: 15
Current Replicas: 5

Pending Pods

0/3 nodes available:
Insufficient CPU

Cluster Autoscaler Logs

No node group config found
```

## Objective

Investigate why the application failed to scale and identify whether the issue is related to:

- Horizontal Pod Autoscaler (HPA)
- Worker Nodes
- Cluster Autoscaler

---

# Environment

- Amazon EKS
- Kubernetes
- Cluster Autoscaler
- Horizontal Pod Autoscaler (HPA)
- kubectl
- AWS CLI
- Metrics Server

---

# Steps Performed

## 1. Verified HPA Status

Checked the HPA configuration and observed that it increased the desired replicas from 5 to 15 based on CPU utilization.

```bash
kubectl get hpa

kubectl describe hpa cpu-demo
```

**Observation**

- Desired Replicas: 15
- Current Replicas: 5

**Conclusion**

HPA is functioning correctly.

---

## 2. Checked Pending Pods

Verified pod scheduling status.

```bash
kubectl get pods

kubectl describe pod <pod-name>
```

**Observation**

```
0/3 nodes are available:
Insufficient CPU
```

**Conclusion**

Pods remain in the Pending state because the existing worker nodes do not have sufficient CPU resources.

---

## 3. Verified Node Resource Utilization

Checked CPU usage on worker nodes.

```bash
kubectl top nodes

kubectl describe node <node-name>
```

**Observation**

Worker nodes were fully utilized with very little CPU available.

**Conclusion**

The cluster requires additional worker nodes to schedule new pods.

---

## 4. Investigated Cluster Autoscaler

Verified whether Cluster Autoscaler was provisioning new nodes.

```bash
kubectl get pods -n kube-system

kubectl logs deployment/cluster-autoscaler -n kube-system
```

**Observation**

```
No node group config found
```

**Conclusion**

Cluster Autoscaler was unable to discover the managed node group because of missing or incorrect configuration.

---

# Root Cause

The Horizontal Pod Autoscaler successfully requested additional replicas, but Kubernetes could not schedule them due to insufficient CPU resources on the existing worker nodes.

Although additional nodes were required, Cluster Autoscaler failed to provision them because it could not identify any scalable node group.

---

# Impact

- Application remained at 5 running replicas.
- Remaining replicas stayed in Pending state.
- Increased application load could not be handled.

---

# Resolution

- Verify Cluster Autoscaler deployment.
- Configure Auto Discovery for the managed node group.
- Ensure required IAM permissions are attached.
- Verify EKS node group tags.
- Confirm the Auto Scaling Group is associated with the cluster.

---

# Verification Commands

```bash
kubectl get hpa

kubectl describe hpa cpu-demo

kubectl get pods

kubectl describe pod <pod-name>

kubectl top nodes

kubectl describe node <node-name>

kubectl get pods -n kube-system

kubectl logs deployment/cluster-autoscaler -n kube-system

eksctl get nodegroup --cluster scale-lab
```

---

# Findings

| Component | Status | Result |
|----------|--------|--------|
| HPA | Healthy | Increased desired replicas |
| Worker Nodes | CPU Exhausted | Pods could not be scheduled |
| Cluster Autoscaler | Misconfigured | Failed to add new nodes |

---

# Final Conclusion

The issue was **not caused by the Horizontal Pod Autoscaler**. HPA correctly requested additional replicas based on CPU utilization. The actual problem was that the worker nodes had exhausted their available CPU resources, and the Cluster Autoscaler was misconfigured (`No node group config found`), preventing it from provisioning additional nodes. As a result, the application remained at five running replicas while the remaining pods stayed in the Pending state.
