# Task 5 - Helm Upgrade Failure (Simulation)

## Objective
Demonstrate Helm upgrade failure due to immutable Kubernetes Deployment selector field.

## What was changed

In Helm helper template:

Before:
app.kubernetes.io/name: payment-service

After:
app.kubernetes.io/name: payment-service-v2

## Why this is a problem

Kubernetes Deployment selector field is immutable.
Once created, it cannot be modified.

## Expected Error (if cluster existed)

cannot patch Deployment
spec.selector:
field is immutable

## Root Cause
Helm tried to update Deployment selector labels which Kubernetes does not allow.

## Fix
- Do not change selector labels
- Use image tag updates instead
- Recreate Deployment if label change is required

## Learning
Understood Kubernetes immutable fields and safe Helm upgrade strategy.
