---
title: "Flexible Model Deployment"
slug: "model-deployment"
excerpt: "How to define the environment my model needs?"
hidden: false
createdAt: "Tue Jan 17 2023 20:49:36 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
Fiddler Platform supports models with varying dependencies. For example, the Fiddler platform allows you to have two models, running the same library but have incompatible versions, through our flexible model deployment specification.

When you add a model artifact into Fiddler (see [add_model_artifact](ref:clientadd_model_artifact)), you can specify the deployment needed to run the model. 

`add_model_artifact` now takes a `deployment_params` argument where you can specify the following information using [fdl.DeploymentParams](ref:fdldeploymentparams):

- `image_uri`: This is the docker image used to create a new runtime to serve the model. You can choose a base image from the following list, with the matching requirements for your model:

  [block:parameters]{"data":{"h-0":"Image uri","h-1":"Dependencies","0-0":"`md-base/python/machine-learning:1.1.0`","0-1":"catboost==1.1.1  \nfiddler-client==1.7.4  \nflask==2.2.2  \ngevent==21.12.0  \ngunicorn==20.1.0  \njoblib==1.2.0  \nlightgbm==3.3.0  \nnltk==3.7  \nnumpy==1.23.4  \npandas==1.5.1  \nprometheus-flask-exporter==0.21.0  \npydantic==1.10.7  \nscikit-learn==1.1.1  \nshap==0.40.0  \nxgboost==1.7.1","1-0":"`md-base/python/deep-learning:1.2.0`","1-1":"fiddler-client==1.7.4  \nflask==2.2.2  \ngevent==21.12.0  \ngunicorn==20.1.0  \njoblib==1.2.0  \nnltk==3.7  \nnumpy==1.23.4  \npandas==1.5.1  \nPillow==9.3.0  \nprometheus-flask-exporter==0.21.0  \npydantic==1.10.7  \ntensorflow==2.9.3  \ntorch==1.13.1  \ntorchvision==0.14.1  \ntransformers==4.24.0","2-0":"`md-base/python/python-38:1.1.0`","2-1":"fiddler-client==1.7.4  \nflask==2.2.2  \ngevent==21.12.0  \ngunicorn==20.1.0  \nprometheus-flask-exporter==0.21.0  \npydantic==1.10.7","3-0":"`md-base/python/python-39:1.1.0`","3-1":"fiddler-client==1.7.4  \nflask==2.2.2  \ngevent==21.12.0  \ngunicorn==20.1.0  \nprometheus-flask-exporter==0.21.0  \npydantic==1.10.7"},"cols":2,"rows":4,"align":["left","left"]}[/block]

Each base image comes with a few pre-installed libraries and these can be overridden by specifying [requirements.txt](doc:artifacts-and-surrogates#requirementstxt-file) file inside your model artifact directory where [package.py](doc:artifacts-and-surrogates#packagepy-wrapper-script) is defined.  

`md-base/python/python-38` and `md-base/python/python-39` are images with the least pre-installed dependencies, use this if none of the other images matches your requirement. 

> 🚧 Be aware
> 
> Installing new dependencies at runtime will take time and is prone to network errors.

- `replicas`: The number of replicas running the model.
- `memory`: The amount of memory (mebibytes) reserved per replica. NLP models might need more memory, so ensure to allocate the required amount of resources.

> 🚧 Be aware
> 
> Your model might need more memory than the default setting. Please ensure you set appropriate amount of resources. If you get a `ModelServeError` error when adding a model, it means you didn't provide enough memory for your model.

- `cpu`: The amount of CPU (milli cpus) reserved per replica.

Both [add_model_artifact](ref:clientadd_model_artifact) and [update_model_artifact](ref:clientupdate_model_artifact) methods support passing `deployment_params`. For example:

```python python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

# Specify deployment parameters
deployment_params = fdl.DeploymentParams(
        image_uri="md-base/python/machine-learning:1.1.0",
        cpu=250,
        memory=512,
  		  replicas=1,
)

# Add model artifact
client.add_model_artifact(  
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir='model_dir/',
  	deployment_params=deployment_params,
)
```

Once the model is added in Fiddler, you can fine-tune the model deployment based on the scaling requirements, using [update_model_deployment](ref:clientupdate_model_deployment). This function allows you to:

- **Horizontal scaling**: horizontal scaling via replicas parameter. This will create multiple Kubernetes pods internally to handle requests.
- **Vertical scaling**: Model deployments support vertical scaling via cpu and memory parameters. Some models might need more memory to load the artifacts into memory or process the requests.
- **Scale down**: You may want to scale down the model deployments to avoid allocating the resources when the model is not in use. Use active parameters to scale down the deployment.
- **Scale up**: This will again create the model deployment Kubernetes pods with the resource values available in the database.

> 📘 Note
> 
> Supported from server version `23.1` with Flexible Model Deployment feature enabled.
