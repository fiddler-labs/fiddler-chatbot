---
title: "On-Prem - Manual Flexible Model Deployment (XAI)"
slug: "manual-flexible-model-deployment"
hidden: true
createdAt: "2023-07-03T16:06:11.375Z"
updatedAt: "2023-08-07T16:29:38.232Z"
---
This page outlines how to use Model Deployments to unlock XAI if you have an on-prem setting of Fiddler and your deployment doesn't give k8s permissions to create pods dynamically.

> 📘 
> 
> Follow this page if you want to upload / update / delete a model artifact or a surrogate model. For monitoring only models, without artifact uploaded, this is not required.

## Permissions

Model surrogate or artifact upload is going to create a model deployment pod dynamically, one per model with all required requirements to run the model.

Fiddler needs permission to perform CRUD operations on k8s resources like deployment and service. If this permission is not provided, then we need a provision to manually spin up the required k8s resources.

In addition, Fiddler offers the ability to run pip install at runtime to install additional dependencies if the image chosen is missing libraries. If this permission is not provided for your deployment, please reach out to the Fiddler team with the list of required dependencies for your model, and we will build an image for you.

> 🚧 Be aware
> 
> Manual Flexible Model Deployment is a fully manual process and need a lot more effort on your side between probably multiple people from your organization (DS + infra / devops). We strongly encourage to provide the necessary permissions to avoid this manual process.

> 👍 Good to know
> 
> If your Fiddler deployment provides the necessary resources, you don't need to follow this page and you can use the regular process. Please check out this [page](doc:model-deployment) in this case.

## Model onboarding steps

If you want to add a model artifact or surrogate, please follow the instructions below.

- First, you need to call [add_model_artifact](ref:clientadd_model_artifact) or [add_model_surrogate](ref:clientadd_model_surrogate) with `MANUAL` deployment type ([fdl.DeploymentType](ref:fdldeploymenttype)) in the [fdl.DeploymentParams](ref:fdldeploymentparams) object.  
  The model artifact will be stored, but no deployment pod will be created at this stage. Model validation and feature impact computation will not be performed. Model deployment status will be inactive.

```python
# Adding a model artifact
client.add_model_artifact(
  model_id=model_name,
  project_id=project_name,
  model_dir=artifact_dir,
  deployment_params=fdl.DeploymentParams(
    deployment_type=fdl.DeploymentType.MANUAL,
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=400,
    memory=600,
  )
)

# ---------- OR ----------

# Adding a model surrogate
client.add_model_surrogate(
  model_id=model_name,
  project_id=project_name,
  deployment_params=fdl.DeploymentParams(
    deployment_type=fdl.DeploymentType.MANUAL,
  )
)
```

- Then, contact the DevOps/infra person from your company to manually create Model Deployment k8s resources. They can check the [next section](doc:manual-flexible-model-deployment#instructions-to-manually-create-model-deployment-k8s-resources) and follow the instructions to create the required k8s resources.
- Finally, you call [update_model_deployment](ref:clientupdate_model_deployment) with the parameter `active=True`.  
  This step will use the model deployment pod previously created, add the model files, validate the model deployment, and compute global feature impact. The model will be active and available for XAI features after this step.

```python
client.update_model_deployment(
  project_id=project_id,
  model_id=model_id,
  active=True,
)
```

## Instructions to manually create Model Deployment k8s resources

Fiddler will provide a script to create `service.yaml` and `deployment.yaml` files. You can review those files and manually apply those on your deployment. Please contact Fiddler if you don't have the script and the template files.

```shell
./deploy-model-deployment.sh
```

To run the script above, a couple of environment variables need to be set.

| Env variable                         | Description                                                        | Required |
| :----------------------------------- | :----------------------------------------------------------------- | :------- |
| `ENDPOINT`                           | Fiddler URL for your deployment                                    | Yes      |
| `TOKEN`                              | Fiddler Token                                                      | Yes      |
| `ORGANIZATION_NAME`                  | The name of the Fiddler organization                               | Yes      |
| `PROJECT_NAME`                       | The name of the project where the MODEL_NAME is located in Fiddler | Yes      |
| `MODEL_NAME`                         | The name of the model to create resources for                      | Yes      |
| `IMAGE_PULL_SECRET_NAME`             | The image pull secret name                                         | No       |
| `MODEL_DEPLOYMENT_EXTRA_ANNOTATIONS` | Custom extra annotations                                           | No       |
| `MODEL_DEPLOYMENT_EXTRA_LABELS`      | Custom extra labels                                                | No       |

## Updating Model Deployment parameters

- In case you need to update the model deployment parameters of the model (like for example `memory` and `cpu`) you can call [update_model_deployment](ref:clientupdate_model_deployment) with the parameter  `active=False`.  
  The new parameters will be stored, but no new deployment pod will be created at this stage. Model validation and feature impact computation will not be performed. Model deployment status will be inactive.

```python
client.update_model_deployment(
  project_id=project_id,
  model_id=model_id,
  memory=800,
  cpu=1000,
  active=False,
)
```

- Then, contact the DevOps/infra person from your company to manually create Model Deployment k8s resources. They can check the [previous section](doc:manual-flexible-model-deployment#instructions-to-manually-create-model-deployment-k8s-resources) and follow the instructions to create the required k8s resources.
- Finally, you call [update_model_deployment](ref:clientupdate_model_deployment) with the parameter `active=True`.  
  This step will use the model deployment pod previously created, add the model files, validate the model deployment, and compute global feature impact. The model will be active and available for XAI features after this step.

```python
client.update_model_deployment(
  project_id=project_id,
  model_id=model_id,
  active=True
)
```

## Updating model artifact/surrogate

If you are trying to update a model artifact or surrogate, please follow the steps below.

- First, you need to call [update_model_artifact](ref:clientupdate_model_artifact) or [update_model_surrogate](ref:clientupdate_model_surrogate) with `MANUAL` deployment type ([fdl.DeploymentType](ref:fdldeploymenttype)) in the [fdl.DeploymentParams](ref:fdldeploymentparams) object.  
  The new model artifact will be stored, but no new deployment pod will be created at this stage. Model validation and feature impact computation will not be performed. Model deployment status will be inactive.

```python
# Update model artifact
client.update_model_artifact(
  model_id=model_name,
  project_id=project_name,
  model_dir=artifact_dir,
  deployment_params=fdl.DeploymentParams(
    deployment_type=fdl.DeploymentType.MANUAL,
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=400,
    memory=600,
  )
)

# ---------- OR ----------

# Update model surrogate
client.update_model_surrogate(
  model_id=model_name,
  project_id=project_name,
  deployment_params=fdl.DeploymentParams(
    deployment_type=fdl.DeploymentType.MANUAL,
  )
)
```

- Then, contact the DevOps/infra person from your company to manually create Model Deployment k8s resources. They can check the [above section](doc:manual-flexible-model-deployment#instructions-to-manually-create-model-deployment-k8s-resources) and follow the instructions to create the required k8s resources.
- Finally, you call [update_model_deployment](ref:clientupdate_model_deployment) with the parameter `active=True`.  
  This step will use the model deployment pod previously created, add the model files, validate the model deployment, and compute global feature impact. The model will be active and available for XAI features after this step.

```python
client.update_model_deployment(
  project_id=project_id,
  model_id=model_id,
  active=True,
)
```

## Deleting Model Deployments

To delete the model deployment pod, you will need to follow the instructions below.

- First, contact the DevOps/infra person from your company to delete the pod. Note: deleting the model in Fiddler will not delete the pod. Using the files created in the [section above](doc:manual-flexible-model-deployment#instructions-to-manually-create-model-deployment-k8s-resources), get the model deployment pod name. Delete manually the pod.
- After the pod is deleted, you can use the [delete_model](ref:clientdelete_model) function to delete the model object in Fiddler.