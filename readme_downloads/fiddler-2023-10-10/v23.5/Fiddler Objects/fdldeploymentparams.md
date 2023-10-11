---
title: "fdl.DeploymentParams"
slug: "fdldeploymentparams"
excerpt: "Represents the deployment parameters for a model"
hidden: false
createdAt: "2023-01-11T22:32:19.679Z"
updatedAt: "2023-06-30T15:52:14.509Z"
---
> Supported from server version `23.1` and above with Model Deployment feature enabled.

[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "image_uri",
    "0-1": "Optional[str]",
    "0-2": "md-base/python/machine-learning:1.0.1",
    "0-3": "Reference to the docker image to create a new runtime to serve the model.  \n  \nCheck the available images on the [Model Deployment](doc:model-deployment) page.",
    "1-0": "replicas",
    "1-1": "Optional[int]",
    "1-2": "1",
    "1-3": "The number of replicas running the model.  \n  \nMinimum value: 1  \nMaximum value: 10  \nDefault value: 1",
    "2-0": "memory",
    "2-1": "Optional[int]",
    "2-2": "256",
    "2-3": "The amount of memory (mebibytes) reserved per replica.  \n  \nMinimum value: 150  \nMaximum value: 16384 (16GiB)  \nDefault value: 256",
    "3-0": "cpu",
    "3-1": "Optional[int]",
    "3-2": "100",
    "3-3": "The amount of CPU (milli cpus) reserved per replica.  \n  \nMinimum value:  10  \nMaximum value: 4000 (4vCPUs)  \nDefault value: 100"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
deployment_params = fdl.DeploymentParams(
        image_uri="md-base/python/machine-learning:1.1.0",
        cpu=250,
        memory=512,
  		  replicas=1,
)
```

> 📘 What parameters should I set for my model?
> 
> Setting the right parameters might not be straightforward and Fiddler is here to help you.
> 
> The parameters might vary depending the number of input features used, the pre-processing steps used and the model itself.
> 
> This table is helping you defining the right parameters

1. **Surrogate Models guide**

| Number of input features | Memory (mebibytes) | CPU (milli cpus) |
| :----------------------- | :----------------- | :--------------- |
| \< 10                    | 250 (default)      | 100 (default)    |
| \< 20                    | 400                | 300              |
| \< 50                    | 600                | 400              |
| \<100                    | 850                | 900              |
| \<200                    | 1600               | 1200             |
| \<300                    | 2000               | 1200             |
| \<400                    | 2800               | 1300             |
| \<500                    | 2900               | 1500             |

2. **User Uploaded guide**

For uploading your artifact model, refer to the table above and increase the memory number, depending on your model framework and complexity. Surrogate models use lightgbm framework. 

For example, an NLP model for a TEXT input might need memory set at 1024 or higher and CPU at 1000.

> 📘 Usage Reference
> 
> See the usage with:
> 
> - [add_model_artifact](ref:clientadd_model_artifact)
> - [add_model_surrogate](ref:clientadd_model_surrogate)
> - [update_model_artifact](ref:clientupdate_model_artifact)
> - [update_model_surrogate](ref:clientupdate_model_surrogate)
> 
> Check more about the [Model Deployment](doc:model-deployment) feature set.