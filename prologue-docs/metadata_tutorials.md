# Azure Kubernetes Service: Update Metadata Annotations Guide

This guide details the process of updating metadata annotations in service files when the IP needs to be changed or when routing is required to a specific host.

## Annotations for Public IP

Annotations are used to attach metadata to objects in a Kubernetes (k8s) cluster. Below are specific annotations used for configuring Azure Load Balancer settings.

- `service.beta.kubernetes.io/azure-load-balancer-resource-group` specifies the resource group of the load balancer. 
- `service.beta.kubernetes.io/azure-load-balancer-ipv4` specifies the IPv4 of the load balancer.
- `service.beta.kubernetes.io/azure-pip-name` specifies the Public IP Name for the service.

All these annotation properties are located in the Service YAML configuration file. You would need to update them based on your needs.

## Sample Configuration

Below is a sample setup of a Service YAML configuration file where specific IP routing to a host is configured:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: default
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-resource-group: Prologue
    service.beta.kubernetes.io/azure-load-balancer-ipv4: <ip-address>
    service.beta.kubernetes.io/azure-pip-name: frontend-ip
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

## Updating annotations:

1. Open your service YAML file (for example, `frontend-service.yaml` or `backend-core-service.yaml`).

2. Locate the `annotations` block under `metadata`.

3. Update the values as per your requirement. For example, to change the IP, update the `service.beta.kubernetes.io/azure-load-balancer-ipv4` value:

   ```yaml
   service.beta.kubernetes.io/azure-load-balancer-ipv4: <new-ip-address>
   ```

4. Now save the changes and close the file.

5. Apply the updated service configuration file using kubectl apply:

   ```bash
   kubectl apply -f frontend-service.yaml
   ```

Kubernetes will now use the updated configuration for routing. Ensure that the update successfully reflects in the changes with `kubectl get services`.