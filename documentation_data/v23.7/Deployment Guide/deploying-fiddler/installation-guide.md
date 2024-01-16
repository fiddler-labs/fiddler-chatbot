---
title: "On-prem Installation Guide"
slug: "installation-guide"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 20:20:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
Fiddler can run on most mainstream flavors of Kubernetes, provided that a suitable [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) is available to provide POSIX-compliant block storage (see [On-prem Technical Requirements](technical-requirements)).

## Before you start

- Create a namespace where Fiddler will be deployed, or request that a namespace/project be created for you by the team that administers your Kubernetes cluster.
  ```text
  [~] kubectl create ns my-fiddler-ns
  ```

- Identify the name of the storage class(es) that you will use for Fiddler's block storage needs. Consult the team that administers your Kubernetes cluster for guidance if you are not sure which class to use.
  ```
  [~] kubectl get storageclass
  NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
  gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  96d
  ```

- If using Kubernetes [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to route traffic to Fiddler, identify the name of the ingress class that should be used. Consult the team that administers your Kubernetes cluster for guidance if you are not sure which class to use.
  ```
  [~] kubectl get ingressclass
  NAME    CONTROLLER             PARAMETERS   AGE
  nginx   k8s.io/ingress-nginx   <none>       39d
  ```

## Quick-start any-prem deployment

Follow the steps below for a quick-start deployment of Fiddler on your Kubernetes cluster suitable for demonstration purposes. This configuration assumes that an ingress controller is available the cluster.

1. Create a `Secret` for pulling images from the Fiddler container registry using the YAML manifest provided to you.

   - Verify that the name of the secret is `fiddler-pull-secret`  
     ```yaml
     apiVersion: v1
     kind: Secret
     metadata:
       name: fiddler-pull-secret
     data:
       .dockerconfigjson: [REDACTED]
     type: kubernetes.io/dockerconfigjson
     ```

   - Create the secret in the namespace where Fiddler will be deployed.

     ```
     [~] kubectl -n my-fiddler-ns apply -f fiddler-pull-secret.yaml
     ```

2. Deploy Fiddler using Helm.

   ```
   [~] helm repo add fiddler https://helm.fiddler.ai/stable/fiddler
   [~] helm repo update
   [~] export STORAGE_CLASS=<my-storage-class>
   [~] export INGRESS_CLASS=<my-ingress-class>
   [~] export FIDDLER_FQDN=fiddler.acme.com
   [~] helm upgrade -i -n my-fiddler-ns \
      -f https://helm.fiddler.ai/stable/samples/v2.yaml \
      -f https://helm.fiddler.ai/stable/samples/anyprem.yaml  \
      --set="grafana.grafana\.ini.server.root_url=https://${FIDDLER_FQDN}/grafana" \
      --set=hostname=${FIDDLER_FQDN}  \
      --set=k8s.storage.className=${STORAGE_CLASS} \
      --set=clickhouse.storage.className=${STORAGE_CLASS} \
      --set=zookeeper.storage.className=${STORAGE_CLASS} \
      --set=ingress.class=${INGRESS_CLASS} \
      --wait \
       fiddler fiddler/fiddler
   ```
