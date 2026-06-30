# Exercise 8 – Egress Restriction Incident

## Scenario

An application running on Amazon EKS is unable to communicate with Amazon DynamoDB.

### Incident

```
Application Logs

Connection timeout

Connectivity Test

curl https://dynamodb.ap-south-1.amazonaws.com

Connection timed out
```

## Objective

Investigate why the application cannot access Amazon DynamoDB and determine whether the issue is related to:

- Security Groups
- Kubernetes Network Policies
- Route Tables
- VPC Endpoints

---

# Task Explanation

This exercise focuses on **network troubleshooting in Amazon EKS**.

The application is running successfully, but every request sent to Amazon DynamoDB results in a **Connection Timeout**. Unlike authentication or permission errors, a timeout indicates that the request never reaches the AWS service.

Your goal is to identify which networking component is preventing outbound (egress) traffic from leaving the Kubernetes cluster.

The investigation covers four major networking components:

### 1. Security Groups

Security Groups act as virtual firewalls for EC2 instances.

Verify that the worker node Security Group allows outbound HTTPS (TCP Port 443). If outbound traffic is blocked, the application cannot communicate with DynamoDB.

---

### 2. Kubernetes Network Policies

Network Policies control communication between Kubernetes Pods.

An Egress Network Policy can block all outbound traffic from a pod. If such a policy exists, requests to DynamoDB will fail even if the AWS network configuration is correct.

---

### 3. Route Tables

Route Tables determine where outbound traffic is sent.

For public subnets, traffic should be routed through an Internet Gateway.

For private subnets, traffic should be routed through a NAT Gateway.

If no valid route exists, external AWS services cannot be reached.

---

### 4. VPC Endpoints

Applications running in private subnets often communicate with AWS services using VPC Endpoints.

If the cluster is deployed in private subnets without a NAT Gateway, a DynamoDB Gateway Endpoint must exist. Otherwise, requests to DynamoDB will timeout.

---

# Environment

- Amazon EKS
- Kubernetes
- Amazon DynamoDB
- AWS CLI
- kubectl
- VPC
- Security Groups
- Route Tables
- VPC Endpoints

---

# Troubleshooting Steps

## Step 1 – Verify the Cluster

Confirm that all worker nodes are healthy.

```bash
kubectl get nodes
```

---

## Step 2 – Deploy a Test Pod

Create a temporary pod with curl installed.

```bash
kubectl run test-pod --image=curlimages/curl --restart=Never -- sleep 3600
```

Verify the pod is running.

```bash
kubectl get pods
```

---

## Step 3 – Test Connectivity

Access the pod.

```bash
kubectl exec -it test-pod -- sh
```

Run the connectivity test.

```bash
curl https://dynamodb.ap-south-1.amazonaws.com
```

### Expected Result

```
{"__type":"com.amazonaws.dynamodb.v20120810#MissingAuthenticationToken"}
```

Receiving this response confirms that the pod can successfully reach the DynamoDB endpoint.

### Incident Result

```
Connection timed out
```

This indicates a networking issue rather than an IAM or authentication problem.

Exit the pod.

```bash
exit
```

---

## Step 4 – Review Application Logs

Check the application logs for timeout errors.

```bash
kubectl logs <pod-name>
```

---

## Step 5 – Investigate Network Policies

List all Network Policies.

```bash
kubectl get networkpolicy --all-namespaces
```

Describe any policy affecting the application namespace.

```bash
kubectl describe networkpolicy <policy-name> -n <namespace>
```

Verify that outbound (Egress) traffic is not being blocked.

---

## Step 6 – Verify Service and Endpoints

Check the application service.

```bash
kubectl get svc
```

Verify endpoints.

```bash
kubectl get endpoints
```

---

## Step 7 – Verify DNS Resolution

Confirm DNS resolution from inside the pod.

```bash
kubectl exec -it test-pod -- nslookup dynamodb.ap-south-1.amazonaws.com
```

---

## Step 8 – Test General Internet Connectivity

Verify whether outbound internet access is working.

```bash
kubectl exec -it test-pod -- curl https://google.com
```

---

## Step 9 – Verify CoreDNS

Ensure CoreDNS is running correctly.

```bash
kubectl get pods -n kube-system
```

---

## Step 10 – Verify Security Groups

Navigate to:

**AWS Console → EC2 → Security Groups**

Verify:

- Outbound HTTPS (TCP 443) is allowed.
- No restrictive outbound rules are blocking traffic.

---

## Step 11 – Verify Route Tables

Navigate to:

**AWS Console → VPC → Route Tables**

Verify:

For Public Subnets:

```
0.0.0.0/0 → Internet Gateway
```

For Private Subnets:

```
0.0.0.0/0 → NAT Gateway
```

---

## Step 12 – Verify VPC Endpoints

Navigate to:

**AWS Console → VPC → Endpoints**

Verify that a DynamoDB Gateway Endpoint exists if the cluster uses private subnets.

---

# Root Cause Analysis

The timeout indicates that outbound traffic from the Kubernetes pods is being blocked before reaching Amazon DynamoDB.

Possible causes include:

- Missing outbound HTTPS rule in the Security Group.
- Restrictive Kubernetes Network Policy.
- Missing default route in the Route Table.
- Missing DynamoDB Gateway VPC Endpoint for private subnets.

---

# Impact

- Application unable to communicate with DynamoDB.
- Database requests fail.
- Application functionality dependent on DynamoDB becomes unavailable.

---

# Resolution

- Allow outbound HTTPS traffic in the Security Group.
- Remove or update restrictive Egress Network Policies.
- Verify Route Tables contain a valid default route.
- Configure a DynamoDB Gateway VPC Endpoint if the cluster runs in private subnets.

---

# Verification Commands

```bash
kubectl get nodes

kubectl get pods

kubectl logs <pod-name>

kubectl get networkpolicy --all-namespaces

kubectl describe networkpolicy <policy-name> -n <namespace>

kubectl get svc

kubectl get endpoints

kubectl exec -it test-pod -- nslookup dynamodb.ap-south-1.amazonaws.com

kubectl exec -it test-pod -- curl https://google.com

kubectl get pods -n kube-system
```

---

# Findings

| Component | Status | Observation |
|----------|--------|-------------|
| Application | Healthy | Running successfully |
| DNS | Healthy | Hostname resolved correctly |
| Security Groups | Investigated | Verified outbound HTTPS rules |
| Network Policies | Investigated | Checked for Egress restrictions |
| Route Tables | Investigated | Verified default route configuration |
| VPC Endpoints | Investigated | Confirmed DynamoDB endpoint availability |

---

# Final Conclusion

The application could not access Amazon DynamoDB because outbound (egress) network traffic was blocked. By systematically investigating Security Groups, Kubernetes Network Policies, Route Tables, and VPC Endpoints, the root cause can be identified and resolved. This exercise demonstrates a structured approach to diagnosing egress connectivity issues in Amazon EKS and reinforces the importance of validating both Kubernetes and AWS networking configurations.
