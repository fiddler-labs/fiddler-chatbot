# Flexible Model Deployment

Fiddler supports explainability for models with varying dependencies. This is achieved by running each model in its own dedicated container to provide the resources and dependencies that are unique to that model. For example, if your team has two models developed with the same libraries but using different versions you can run both those models by specifying the exact version they were built with.

> 📘 Note
>
> For models that require monitoring features only, there is no need to upload your model artifact or create a surrogate model as these are only used to support explainability features.

***

When adding a model artifact to your Fiddler model (see [add\_artifact](../../../Python\_Client\_3-x/api-methods-30.md#add\_artifact)), you specify the deployment configuration needed to run it using the [DeploymentParams](../../../Python\_Client\_3-x/api-methods-30.md#deploymentparams) argument. Fiddler has a set of starter images from which to select the configuration most appropriate for running your model. These images vary by included libraries and Python versions. Note you can also customize an image by including your own requirements.txt file along with the model artifact package.

#### DeploymentParams Arguments

*   `image_uri`: This is the Docker image used to create a new runtime to serve the model. You can choose a base image from the following list, with the matching requirements for your model:

    | Image URI                         | Dependencies                                                                                                                                                                     |
    | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `md-base/python/python-39:2.0.2`  | <p>fiddler-client==3.0.3<br>flask==2.2.5<br>gevent==23.9.0<br>gunicorn==22.0.0<br>prometheus-flask-exporter==0.21.0<br>pyarrow==14.0.1<br>pydantic==1.10.13</p>                  |
    | `md-base/python/python-310:1.0.0` | <p>fiddler-client==3.0.3<br>flask==2.2.5<br>gevent==23.9.0<br>gunicorn==22.0.0<br>prometheus-flask-exporter==0.21.0<br>pyarrow==14.0.1<br>pydantic==1.10.13</p>                  |
    | `md-base/python/python-311:1.0.0` | <p>fiddler-client==3.0.3<br>flask==2.2.5<br>gevent==23.9.0<br>gunicorn==22.0.0<br>prometheus-flask-exporter==0.21.0<br>pyarrow==14.0.1<br>pydantic==1.10.13</p>                  |
    | `md-base/python/java:2.1.0`       | <p>fiddler-client==3.0.3<br>flask==2.2.5<br>gevent==23.9.0<br>gunicorn==22.0.0<br>h2o==3.46.0.5<br>prometheus-flask-exporter==0.21.0<br>pyarrow==14.0.1<br>pydantic==1.10.13</p> |
    | `md-base/python/rpy2:2.0.2`       | <p>fiddler-client==3.0.3<br>flask==2.2.5<br>gevent==23.9.0<br>gunicorn==22.0.0<br>prometheus-flask-exporter==0.21.0<br>pyarrow==14.0.1<br>pydantic==1.10.13<br>rpy2==3.5.1</p>   |

> 📘 Image upgrades
>
> These Docker images are upgraded routinely to resolve security vulnerabilities and the image tag is updated accordingly. Unsupported Python versions are not provided.

> 🚧 Be aware
>
> Model version features are supported with the image versions listed above. Images below 2.x for `python-39`, `java` and `rpy2` will continue to work for existing models using a single version. From 24.5 onwards, model version first class support is added and these require the new model deployment base image tag versions.

Each base image comes with a few pre-installed libraries and these can be overridden and added to by specifying a [requirements.txt](../artifacts-and-surrogates.md#requirementstxt-file) file inside your model artifact directory where [package.py](../artifacts-and-surrogates.md#packagepy-wrapper-script) is defined.

Note that the old images `deep-learning` and `machine-learning` are deprecated (All current versions are still working, but we stopped maintaining and upgrading those). We encourage users to select any plain Python image, and add the necessary libraries in `requirements.txt`.

> 🚧 Be aware
>
> Installing new dependencies at runtime will take time and is prone to network errors.

```
* `replicas`: The number of Docker image replicas running the model.
* `memory`: The amount of memory (mebibytes) reserved per replica. NLP models might need more memory, so ensure to allocate the required amount of resources.
```

> 🚧 Be aware
>
> Your model might require more memory than the default setting. Please ensure you set a sufficient amount of resources. If you see a `ModelServeError` error when adding a model, it means the current settings were not enough to run your model.

* `cpu`: The amount of CPU (milli cpus) reserved per replica. Both number of features and model complexity can require more CPU allocation.

Both [add\_artifact](../../../Python\_Client\_3-x/api-methods-30.md#add\_artifact) and [update\_artifact](../../../Python\_Client\_3-x/api-methods-30.md#update\_artifact) methods support passing `deployment_params`. For example:

```python
# Specify deployment parameters
deployment_params = fdl.DeploymentParams(
        image_uri="md-base/python/python-311:1.0.0",
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

Once the model is added in Fiddler, you can fine-tune the model deployment based on the scaling requirements, using [update\_model\_deployment](../../../Python\_Client\_3-x/api-methods-30.md#update-model-deployment). This function allows you to:

* **Horizontal scaling**: horizontal scaling via replicas parameter. This will create multiple Kubernetes pods internally to handle concurrent requests.
* **Vertical scaling**: Model deployments support vertical scaling via cpu and memory parameters. Some models might need more memory to load the artifacts into memory or process the requests.
* **Scale down**: You may want to scale down the model deployments to avoid allocating the resources when the model is not in use. Use _active_ parameter set to _False_ to scale down the deployment.
* **Scale up**: To scale model deployments back up, set _active_ parameter to _True_.

{% include "../../../.gitbook/includes/main-doc-footer.md" %}

