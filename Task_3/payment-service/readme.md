# ARGOCD OUTOF SYNC PRODUCTION INCIDENT - GITOPS TROUBLESHOOTING LAB

============================================================

1. OVERVIEW

This document explains a real-world GitOps production incident where ArgoCD reports an "OutOfSync" state due to configuration drift between Git (desired state) and Kubernetes cluster (live state).

ArgoCD ensures that Kubernetes applications always match the configuration defined in Git.

============================================================

2. OBJECTIVE

- Understand ArgoCD OutOfSync scenario
- Identify configuration drift between Git and Kubernetes
- Investigate what changed in the cluster
- Restore desired state using ArgoCD
- Learn prevention techniques for production environments

============================================================

3. ARCHITECTURE FLOW

Git Repository (Desired State)
        |
        v
ArgoCD Controller
        |
        v
Kubernetes Cluster (Live State)

============================================================

4. INCIDENT DETAILS

Application Name        : payment-service
Desired State (Git)     : replicas = 3
Live State (Cluster)    : replicas = 5

ArgoCD Status:
- Sync Status  : OutOfSync
- Health Status: Healthy

============================================================

5. ROOT CAUSE

A manual change was performed directly on the Kubernetes cluster:

COMMAND EXECUTED:
kubectl scale deployment payment-service --replicas=5

This caused configuration drift between Git and Kubernetes.

============================================================

6. REPRODUCTION STEPS (PRACTICAL LAB)

Step 1: Verify deployment
kubectl get deployment payment-service

Step 2: Apply manual change
kubectl scale deployment payment-service --replicas=5

Step 3: Check ArgoCD status
argocd app get payment-service

Expected result:
Status changes to OutOfSync

============================================================

7. TROUBLESHOOTING STEPS

Step 1: Check application status
argocd app get payment-service

Step 2: Compare Git vs Cluster state
argocd app diff payment-service

Expected output:
- replicas: 3
+ replicas: 5

Step 3: Verify Kubernetes deployment
kubectl get deployment payment-service
kubectl describe deployment payment-service

Step 4: Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

For production (EKS):
- Check AWS CloudTrail logs
- Check Kubernetes audit logs

============================================================

8. RESOLUTION (FIX)

OPTION 1 - Sync from ArgoCD (Recommended)
argocd app sync payment-service

This restores the cluster to match Git state.

------------------------------------------------------------

OPTION 2 - Update Git (If change is valid)

Modify Git repository:
replicas: 5

Then run:
git add .
git commit -m "Update replicas"
git push

ArgoCD will automatically sync the changes.

============================================================

9. PREVENTION STRATEGIES

1. Enable Auto-Sync with Self-Healing

syncPolicy:
  automated:
    prune: true
    selfHeal: true

------------------------------------------------------------

2. Enforce GitOps Workflow

All changes must follow:

Git Commit → Pull Request → CI/CD → ArgoCD → Kubernetes

Avoid direct kubectl changes in production.

------------------------------------------------------------

3. Restrict RBAC Permissions

- Prevent direct modification of production workloads
- Allow only ArgoCD to manage deployments

------------------------------------------------------------

4. Enable Audit Logging

Track:
- Who changed the resource
- When it was changed
- What was changed

============================================================

10. KEY LEARNINGS

- OutOfSync means Git and Cluster are not matching
- Healthy does NOT mean Synced
- Manual kubectl changes break GitOps model
- Git is the single source of truth
- ArgoCD detects and helps fix configuration drift

============================================================

11. CONCLUSION

ArgoCD ensures Kubernetes remains aligned with Git-defined configuration. Any manual cluster change results in OutOfSync status until reconciled through Git or ArgoCD sync.

============================================================
