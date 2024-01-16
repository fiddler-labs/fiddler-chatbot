---
title: "Model: Artifacts, Package, Surrogate"
slug: "artifacts-and-surrogates"
excerpt: "Important terminologies for the ease of use of Fiddler Explainability"
hidden: false
createdAt: "Tue Nov 15 2022 18:06:36 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Model Artifacts and Model Package

A model in Fiddler is a placeholder that may not need the **model artifacts** for monitoring purposes. However, for explainability, model artifacts are needed. 

_Required_ model artifacts include: 

- The **[model file](doc:artifacts-and-surrogates#model-file) **(e.g. `*.pkl`)
- [`package.py`](doc:artifacts-and-surrogates#packagepy-wrapper-script): A wrapper script containing all of the code needed to standardize the execution of the model.

A collection of model artifacts in a directory is referred to as a **model package**. To start, **place your model artifacts in a new directory**. This directory will be the model package you will upload to Fiddler to add or update model artifacts. 

While the model file and package.py are required artifacts in a model package, you can also _optionally_ add other artifacts such as:

- [`model.yaml`](doc:artifacts-and-surrogates#modelyaml-configuration-file): A YAML file containing all the information about the model as specified in [ModelInfo](ref:fdlmodelinfo). This model metadata is used in Fiddler’s explanations, analytics, and UI.
- Any serialized [preprocessing objects](#preprocessing-objects) needed to transform data before running predictions or after.

In the following, we discuss the various model artifacts.

### Model File

A model file is a **serialized representation of your model** as a Python object.

Model files can be stored in a variety of formats. Some include

- Pickle (`.pkl`)
- Protocol buffer (`.pb`)
- Hierarchical Data Format/HDF5 (`.h5`)

### package.py wrapper script

Fiddler’s artifact upload process is **framework-agnostic**. Because of this, a **wrapper script** is needed to let Fiddler know how to interact with your particular model and framework.

The wrapper script should be named `package.py`, and it should be **placed in the same directory as your model artifact**. Below is an example of what `package.py` should look like.

```python
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class MyModel:

    def __init__(self):
        """
        Here we can load in the model and any other necessary
            serialized objects from the PACKAGE_PATH.
        """

    def predict(self, input_df):
        """
        The predict() function should return a DataFrame of predictions
            whose columns correspond to the outputs of your model.
        """

def get_model():
    return MyModel()
```

The only hard requirements for `package.py` are

- The script must be named `package.py`
- The script must implement a function called `get_model`, which returns a model object
- This model object must implement a function called `predict`, which takes in a pandas DataFrame of model inputs and returns a pandas DataFrame of model predictions

### model.yaml configuration file

In case you want to update the custom explanations (`custom_explanation_names`) or the preferred explanation method (`preferred_explanation_method`) in the model info, you will need to construct a YAML file with **specifications for how your model operates**. This can be easily obtained from [fdl.ModelInfo()](ref:fdlmodelinfo) object.

> 📘 Info
> 
> For information on constructing a [fdl.ModelInfo()](ref:fdlmodelinfo) object, see [Creating ModelInfo Object](doc:registering-a-model#creating-a-modelinfo-object).

> 🚧 Warning
> 
> Currently, only the following fields in model info can be updated:
> 
> - `custom_explanation_names`
> - `preferred_explanation_method`
> - `display_name`
> - `description`

Once you have your [fdl.ModelInfo()](ref:fdlmodelinfo), you can call its [fdl.ModelInfo.to_dict()](ref:fdlmodelinfoto_dict) function to **generate a dictionary** that can be used for the YAML configuration file.

```python
import yaml

with open('model.yaml', 'w') as yaml_file:
    yaml.dump({'model': model_info.to_dict()}, yaml_file)
```

Note that we are adding `model` key whose value is the dictionary produced by the [`fdl.ModelInfo`](ref:fdlmodelinfo) object.

Once it’s been created, you can place it in the directory with your model artifact and `package.py` script.

### Preprocessing objects

Another component of your model package could be any **serialized preprocessing objects** that are used to transform the data before or after making predictions.

You can place these in the model package directory as well.

> 📘 Info
> 
> For example, in the case that we have a **categorical feature**, we may need to **encode** it as one or more numeric columns before calling the model’s prediction function. In that case, we may have a serialized transform object called `encoder.pkl`. This should also be included in the model package directory.

### requirements.txt file

> 📘 Info
> 
> This is only used starting at 23.1 version with Model Deployment enabled.

Each base image (see [image_uri](doc:model-deployment) for more information on base images) comes with a few pre-installed libraries and these can be overridden by specifying `requirements.txt` file inside your model artifact directory where `package.py` is defined.

Add the dependencies to requirements.txt file like this:

```python
scikit-learn==1.0.2  
numpy==1.23.0  
pandas==1.5.0
```

## Surrogate Model

A surrogate model is an approximation of your model intended to make qualitative explainability calculations possible for scenarios where model ingestion is impossible or explainability is an occasional nice-to-have, but not a primary component of a model monitoring workflow.  

Fiddler creates a surrogate when you call [`add_model_surrogate`](/reference/clientadd_model_surrogate).  This requires that you've already added a model using [add_model](ref:clientadd_model).

> 🚧 Surrogates can currently only be created for models with tabular input types.

Fiddler produces a surrogate by training a gradient-boosted decision tree (LightGBM) to the ground-truth labels provided and with a general, predefined set of settings.
