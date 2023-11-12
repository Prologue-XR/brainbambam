## Azure Containerization and Orchestration Setup

This document outlines the components and services created for our Azure container orchestration setup.

### Azure Resource Group
- **Name:** Prologue

### Azure Container Registry (ACR)
- **Name:** prologueacr
- **Created Docker Images:**
  - prologueacr.azurecr.io/worker:v4
  - prologueacr.azurecr.io/frontend:v4
  - prologueacr.azurecr.io/backend-core:v4
  - prologueacr.azurecr.io/flower:v4

### Azure Kubernetes Service (AKS)
- **Cluster Name:** prologueaks
- **Deployments And Associated Services Created:**
  - **1. Redis**
    - Deployment: redis-deployment.yaml
    - Service: redis-service.yaml
  - **2. Backend-core**
    - Deployment: backend-core-deployment.yaml
    - Service: backend-core-service.yaml
  - **3. Worker**
    - Deployment: worker-deployment.yaml
    - Service: None
  - **4. Flower**
    - Deployment: flower-deployment.yaml
    - Service: flower-service.yaml
  - **5. Frontend**
    - Deployment: frontend-deployment.yaml
    - Service: frontend-service.yaml

### Azure Public IP 
- **Name**: backend-ip   
- **Allocation Method:** static   
- **Associated Service:** backend-core      

- **Name**: frontend-ip   
- **Allocation Method:** static    
- **Associated Service:** frontend     
 
### Kubernetes ConfigMaps  
- **Associated with Backend-core:** backend--env-configmap.yaml
- **Associated with Frontend:** frontend--env-configmap.yaml      

### Kubernetes Role  
- **Role Assigned:** Network Contributor          