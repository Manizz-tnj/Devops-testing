# Exercise 7 – ALB Ingress Failure

## Scenario

An application deployed on Amazon EKS is inaccessible through the Application Load Balancer (ALB).

### Incident

```
User Error

504 Gateway Timeout

Ingress

alb.ingress.kubernetes.io/target-type: ip

Events

Target registration failed

AWS Load Balancer Controller Logs

Unable to discover subnets
```

## Objective

Investigate why the application is inaccessible and identify the root cause by analyzing:

- Ingress resource
- AWS Load Balancer Controller logs
- Kubernetes events
- Service and Endpoints
- VPC subnet configuration

---

# Environment

- Amazon EKS
- Kubernetes
- AWS Load Balancer Controller
- Application Load Balancer (ALB)
- kubectl
- AWS CLI

---

# Troubleshooting Steps

## 1. Verify the Application Pods

Check whether the application pods are running.

```bash
kubectl get pods -n alb-demo
```

**Observation**

Pods are in the **Running** state.

**Conclusion**

The application itself is healthy.

---

## 2. Verify the Service

Check the Kubernetes service.

```bash
kubectl get svc -n alb-demo
```

Verify service endpoints.

```bash
kubectl get endpoints -n alb-demo
```

**Observation**

Service endpoints are available.

**Conclusion**

The service is correctly forwarding traffic to the application pods.

---

## 3. Verify the Ingress Resource

Describe the ingress.

```bash
kubectl describe ingress nginx-ingress -n alb-demo
```

**Observation**

Ingress events reported:

```
Target registration failed
```

**Conclusion**

The ALB could not register backend targets.

---

## 4. Check AWS Load Balancer Controller

Verify that the controller is running.

```bash
kubectl get pods -n kube-system
```

View controller logs.

```bash
kubectl logs deployment/aws-load-balancer-controller -n kube-system
```

**Observation**

```
Unable to discover subnets
```

**Conclusion**

The controller failed to locate suitable VPC subnets for creating the Application Load Balancer.

---

## 5. Verify VPC Subnet Tags

Checked subnet tags in the AWS VPC console.

Required tags:

### Public ALB

```
kubernetes.io/role/elb = 1
```

### Cluster Tag

```
kubernetes.io/cluster/<cluster-name> = shared
```

**Observation**

Required subnet tags were missing or incorrectly configured.

**Conclusion**

Without these tags, the AWS Load Balancer Controller cannot discover eligible subnets.

---

# Root Cause

The AWS Load Balancer Controller failed to discover suitable VPC subnets because the required subnet tags were missing or incorrectly configured.

As a result:

- The Application Load Balancer could not be provisioned correctly.
- Target registration failed.
- User requests returned **504 Gateway Timeout**.

---

# Impact

- Application inaccessible through the ALB.
- Backend targets were not registered.
- External traffic could not reach the application.

---

# Resolution

- Verify that the AWS Load Balancer Controller is running.
- Ensure the controller has the required IAM permissions.
- Add the required subnet tags:
  - `kubernetes.io/role/elb=1` (public ALB)
  - `kubernetes.io/cluster/<cluster-name>=shared`
- Recreate or reconcile the Ingress resource.
- Confirm that the ALB is successfully created and targets become healthy.

---

# Verification Commands

```bash
kubectl get pods -n alb-demo

kubectl get svc -n alb-demo

kubectl get endpoints -n alb-demo

kubectl get ingress -n alb-demo

kubectl describe ingress nginx-ingress -n alb-demo

kubectl get pods -n kube-system

kubectl logs deployment/aws-load-balancer-controller -n kube-system

kubectl get events -n alb-demo --sort-by=.metadata.creationTimestamp
```

---

# Findings

| Component | Status | Observation |
|----------|--------|-------------|
| Application Pods | Healthy | Running successfully |
| Service | Healthy | Endpoints available |
| Ingress | Failed | Target registration failed |
| AWS Load Balancer Controller | Failed | Unable to discover subnets |
| VPC Subnets | Misconfigured | Required tags missing |

---

# Final Conclusion

The root cause of the incident was a **misconfiguration of the VPC subnets**. The required subnet tags for the AWS Load Balancer Controller were missing, preventing it from discovering suitable subnets for the Application Load Balancer. Consequently, backend targets could not be registered, resulting in a **504 Gateway Timeout** when users attempted to access the application.

This exercise demonstrates the importance of verifying Kubernetes Ingress resources, AWS Load Balancer Controller logs, subnet tagging, and service endpoints when troubleshooting ALB-related connectivity issues in Amazon EKS.
