---
title: Model Versions
slug: model-versions
excerpt: ''
createdAt: Thu May 02 2024 15:02:32 GMT+0000 (Coordinated Universal Time)
updatedAt: Wed May 08 2024 19:22:59 GMT+0000 (Coordinated Universal Time)
---

# Model Versions

## Overview

Model versions in Fiddler provide a structured approach to managing related models, offering enhanced efficiency in tasks such as model retraining and champion vs. challenger analyses. Rather than creating entirely new model instances for updates, users can opt for creating versions of existing models, maintaining their foundational structure while accommodating necessary changes. These changes can span schema modifications, including column additions or removals, adjustments to data types and value ranges, updates to model specifications, and refinement of task parameters or Explainable AI (XAI) settings.

## Use Cases

Model versions are particularly useful in scenarios where:

* **Model Retraining**: Models require updating with new data or improved algorithms without disrupting existing deployments.
* **Champion vs. Challenger Analyses**: Comparing the performance of different model versions to identify the most effective one for deployment.
* **Historical Tracking**: Maintaining a clear record of model iterations and changes over time for auditing or analysis purposes.

## Capabilities

With model versions, users can:

* **Maintain Model Lineage**: Easily trace the evolution of models by keeping track of different versions and their respective changes.
* **Efficiently Manage Updates**: Streamline the process of updating models by creating new versions with incremental changes, avoiding the need to re-upload entire model instances.
* **Flexibly Modify Schemas**: Modify model schemas, including column structures, data types, and other specifications, to adapt models to evolving requirements.
* **Adjust Parameters**: Refine task parameters, XAI settings, and other configurations to improve explainability, or tailor the task to better suit the model's purpose.
* **Ensure Consistency**: Ensure consistency in model deployments by managing related models within the same versioning system, facilitating comparisons and deployments.

## Example of Creating a Model Version

Utilizing [from\_name()](../../Python\_Client\_3-x/api-methods-30.md#from\_name-3) and [duplicate()](../../Python\_Client\_3-x/api-methods-30.md#duplicate) methods, we can efficiently create a new model version with modifications based on an existing model. First, we retrieve the existing model by specifying its name, project ID, and version. Subsequently, we duplicate this model while updating its version, transitioning, for instance, from `v3` to `v4`. Within the new version (`v4`), we tailor the value ranges of the 'Age' column to meet our requirements. Finally, the [create()](../../Python\_Client\_3-x/api-methods-30.md#create-3) method is invoked to publish the newly minted model version `v4`.

```python
# Define project ID and model name
PROJECT_ID = 'your_project_id'
MODEL_NAME = 'your_model_name'

# Retrieve the existing model version by name and project ID
existing_model = fdl.Model.from_name(name=MODEL_NAME, project_id=PROJECT_ID, version='v3')

# Duplicate the existing model to create a new version
new_model = existing_model.duplicate(version='v4')

# Modify the schema of the new version
new_model.schema['Age'].min = 18
new_model.schema['Age'].max = 60

# Create the new version of the model
new_model.create()
```

{% include "../../.gitbook/includes/main-doc-footer.md" %}

