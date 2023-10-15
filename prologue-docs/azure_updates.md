## Azure Kubernetes Service Management Guide

This guide highlights the key steps to manage updates and perform common maintenance tasks in Azure Kubernetes Service (AKS).

### Prerequisites:

Before we start, ensure your local environment has the following:

- Azure CLI installed
- Kubectl installed
- Logged in to your Azure account using `az login`

### Key Variables:

- **Resource Group Name:** Prologue
- **Azure Container Registry (ACR) Name:** prologueacr
- **Kubernetes Cluster Name:** prologueaks
- **Public IPs:** backend-ip, frontend-ip

### Managing Public IPs:

1. To create a new public IP:
    ```bash
    az network public-ip create --resource-group Prologue --name myPublicIP --sku Standard --allocation-method static
    ```
2. To get the IP address value:
    ```bash
    az network public-ip show --resource-group Prologue --name myPublicIP --query ipAddress --output tsv
    ```
3. To delete a public IP:
    ```bash
    az network public-ip delete --name myPublicIP --resource-group Prologue
    ```
### Role Assignment:

To assign a role, for instance "Network Contributor", to a Principal ID of an AKS cluster:

```bash
az aks show --resource-group Prologue --name prologueaks --query "identity.principalId" --output tsv
az role assignment create --assignee <principal-id> --role "Network Contributor" --resource-group Prologue
```
Replace `<principal-id>` with the output from the first command.

### Pulling the Latest Changes:

1. To pull the latest changes from your Azure Container Registry:
    ```bash
    az acr repository show-tags --name prologueacr --repository frontend --output table
    ```

### Deploying the Application:

1. Retrieve the credentials:
    ```bash
    az aks get-credentials --resource-group Prologue --name prologueaks
    ```
2. Apply the `ConfigMap` and `Service` definitions:
    ```bash
    kubectl apply -f backend--env-configmap.yaml
    kubectl apply -f frontend--env-configmap.yaml
    kubectl apply -f redis-service.yaml
    kubectl apply -f backend-core-service.yaml
    kubectl apply -f flower-service.yaml
    kubectl apply -f frontend-service.yaml
    ```
3. Apply the `Deployment` configurations:
    ```bash
    kubectl apply -f redis-deployment.yaml
    kubectl apply -f backend-core-deployment.yaml
    kubectl apply -f worker-deployment.yaml
    kubectl apply -f flower-deployment.yaml
    kubectl apply -f frontend-deployment.yaml
    ```

### Monitoring:

1. Monitor the services:
    ```bash
    kubectl get services  
    ```
2. Check the pods:
    ```bash
    kubectl get pods
    ```
3. Retrieve logs from a specific pod:
   ```bash
   kubectl logs frontend-b46c447cb-pqd4s
   ```
4. Follow logs from a container in a pod:
    ```bash
    kubectl logs -f frontend-b46c447cb-pqd4s 
    ```
   
### Updating:

1. Update the Docker image, tag it and push to the Azure Container Registry. Update the Kubernetes `Deployment` file with the new Docker image and tag and reapply the `Deployment`:

   ```bash
   docker tag prologueacr.azurecr.io/frontend prologueacr.azurecr.io/frontend:v2
   docker push prologueacr.azurecr.io/frontend:v2
   <Update the frontend-deployment.yaml to use frontend:v2 and reapply the Deployment>
   kubectl apply -f frontend-deployment.yaml
   ```

2. To rollback to the previous version if a deployment has issues:
    ```bash
    kubectl rollout undo deployment/frontend
    ```

3. Restart a deployment:
   ```bash
   kubectl rollout restart deployment/frontend
   ```
### Deleting a Service:

1. If a service is not needed:
    ```bash
    kubectl delete service frontend
    ```

### Deleting the Cluster:

Delete the Kubernetes cluster:

```bash
az aks delete --name prologueaks --resource-group Prologue --yes
```