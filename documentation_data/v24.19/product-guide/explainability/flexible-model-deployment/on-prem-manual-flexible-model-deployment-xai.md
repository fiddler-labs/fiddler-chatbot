# On Prem Manual Flexible Model Deployment Xai

This page outlines how to upload a model artifact or surrogate if you have an on-prem deployment of Fiddler and your deployment doesn't give k8s permissions to create model deployment pods dynamically.

> 📘 Note
>
> Follow this page if you want to upload a model artifact or a surrogate model. For monitoring only models, without artifact uploaded, this is not required.

## Permissions

Model surrogate or artifact upload is going to create a model deployment pod dynamically, one per model with all required requirements to run the model.

Fiddler requires permission to perform CRUD operations on k8s resources like deployment and service. If this permission is not provided, then manual provision is required to spin up the required k8s resources.

In addition, Fiddler offers the ability to run `pip install` at runtime to install additional dependencies not included in the chosen image. If this permission is not provided for your deployment, please reach out to the Fiddler team with the list of required of dependencies for your model, and we will build an image for you.

### Model On-boarding Steps

* Call [add\_artifact](../../../Python\_Client\_3-x/api-methods-30.md#add\_artifact) with MANUAL deployment type in the [DeploymentParams](../../../Python\_Client\_3-x/api-methods-30.md#deploymentparams) object. The model artifact will be stored, but no deployment pod will be created at this stage. Model validation and feature impact computation will not be performed. Model deployment status will be inactive.

```python
# Specify deployment parameters
deployment_params = fdl.DeploymentParams(
        image_uri="md-base/python/machine-learning:1.4.0",
        cpu=250,
        memory=512,
  		  replicas=1)

# Add model artifact
job = model.add_artifact(
  model_dir =  str, #path to your model dirctory with model artifacts and package.py 
  deployment_param = DeploymentParams | None,
) -> AsyncJob
job.wait()
```

* Manually create Model Deployment k8s resources. Please check the [next section](on-prem-manual-flexible-model-deployment-xai.md#instructions-to-manually-create-model-deployment-k8s-resources) and follow the instructions to create the required k8s resources.
* Call [update\_model\_deployment](../../../Python\_Client\_3-x/api-methods-30.md#update-model-deployment) with the parameter `active=True`. This step will use the model deployment pod previously created, add the model files, validate the model deployment, and compute global feature impact. Model will be active and available for XAI features after this step.

```python
model_deployment.cpu = 300
model_deployment.active = True
model_deployment.update()
```

## Instructions to Manually Create Model Deployment k8s Resources

Fiddler will provide a script to create `service.yaml` and `deployment.yaml` files. Customers can review those files and manually apply those on their deployment. A list of environment variable has to be defined in order to run the script.

```shell
./deploy-model-deployment.sh
```

| Environment variables                 | Description                                                         |
| ------------------------------------- | ------------------------------------------------------------------- |
| ENDPOINT                              | Fiddler URL for your deployment                                     |
| TOKEN                                 | Fiddler Token                                                       |
| ORGANIZATION\_NAME                    | The name of the Fiddler organization                                |
| PROJECT\_NAME                         | The name of the project where the MODEL\_NAME is located in Fiddler |
| MODEL\_NAME                           | The name of the model to create resources for                       |
| IMAGE\_PULL\_SECRET\_NAME             | The image pull secret name (Optional)                               |
| MODEL\_DEPLOYMENT\_EXTRA\_ANNOTATIONS | Custom extra annotations (Optional)                                 |
| MODEL\_DEPLOYMENT\_EXTRA\_LABELS      | Custom extra labels (Optional)                                      |

{% include "../../../.gitbook/includes/main-doc-footer.md" %}

