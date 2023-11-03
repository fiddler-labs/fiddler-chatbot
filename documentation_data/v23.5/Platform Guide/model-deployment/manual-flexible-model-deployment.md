---
title: "On-Prem - Manual Flexible Model Deployment (XAI)"
slug: "manual-flexible-model-deployment"
hidden: true
createdAt: "2023-07-03T16:06:11.375Z"
updatedAt: "2023-10-19T20:59:24.675Z"
---
This page outlines how to upload a model artifact or surrogate if you have an on-prem deployment of Fiddler and your deployment doesn't give k8s permissions to create model deployment pods dynamically.

> 📘 
> 
> Follow this page if you want to upload a model artifact or a surrogate model. For monitoring only models, without artifact uploaded, this is not required.

## Permissions

Model surrogate or artifact upload is going to create a model deployment pod dynamically, one per model with all required requirements to run the model.

Fiddler need permissions to perform CRUD operations on k8s resources like deployment and service. If this permissions is not provided, then we need a provision to manually spin up the required k8s resources.

In addition, Fiddler offers the ability to run pip install at runtime to install additional dependencies if the image chosen is missing libraries. If this permission is not provided for your deployment, please reach out to the Fiddler team with the list of required of dependencies for your model, we will build an image for you.

## Model on-boarding steps

- Customer calls [add_model_artifact](ref:clientadd_model_artifact) with MANUAL deployment type in the [fdl.DeploymentParams](ref:fdldeploymentparams) object.  
  The model artifact will be stored, but no deployment pod will be created at this stage. Model validation and feature impact computation will not be performed. Model deployment status will be inactive.

```python
client.add_model_artifact(
    model_id=model_name,
    project_id=project_name,
    model_dir=artifact_dir,
    deployment_params=fdl.DeploymentParams(
      	deployment_type=fdl.DeploymentType.MANUAL,
      	image_uri="md-base/python/machine-learning:1.1.0"
    )
)
```

- Customer manually creates Model Deployment k8s resources. Please check the [next section](doc:manual-flexible-model-deployment#instructions-to-manually-create-model-deployment-k8s-resources) and follow the instructions to create the required k8s resources.
- Customer calls [update_model_deployment](ref:clientupdate_model_deployment) with the parameter `active=True`.  
  This step will use the model deployment pod previously created, add the model files, validate the model deployment and compute global feature impact. Model will be active and available for XAI features after this step.

```python
client.update_model_deployment(
  	project_id=project_id,
    model_id=model_id,
  	active=True
)
```

## Instructions to manually create Model Deployment k8s resources

Fiddler will provide a script to create `service.yaml` and `deployment.yaml` files. Customers can review those files and manually apply those on their deployment. A list of environment variable has to be defined in order to run the script.

```shell
./deploy-model-deployment.sh
```

| Environment variables              | Description                                                        |
| :--------------------------------- | :----------------------------------------------------------------- |
| ENDPOINT                           | Fiddler URL for your deployment                                    |
| TOKEN                              | Fiddler Token                                                      |
| ORGANIZATION_NAME                  | The name of the Fiddler organization                               |
| PROJECT_NAME                       | The name of the project where the MODEL_NAME is located in Fiddler |
| MODEL_NAME                         | The name of the model to create resources for                      |
| IMAGE_PULL_SECRET_NAME             | The image pull secret name (Optional)                              |
| MODEL_DEPLOYMENT_EXTRA_ANNOTATIONS | Custom extra annotations (Optional)                                |
| MODEL_DEPLOYMENT_EXTRA_LABELS      | Custom extra labels (Optional)                                     |