---
title: "Global Explanations"
slug: "global-explanations-platform"
excerpt: "Platform Guide"
hidden: true
createdAt: "Mon Dec 19 2022 19:29:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:41:52 GMT+0000 (Coordinated Universal Time)"
---
Fiddler provides powerful visualizations to describe the impact of features in your model. Feature impact and importance can be found in either the Explain or Analyze tab.

Global explanations are available in the UI for **structured (tabular)** and **natural language (NLP)** models, for both classification and regression. They are also supported via API using the Fiddler Python package. Global explanations are available for both production and dataset queries.

## Tabular Models

For tabular models, Fiddler’s Global Explanation tool shows the impact/importance of the features in the model.

Two global explanation methods are available:

* **_Feature impact_** — Gives the average absolute change in the model prediction when a feature is randomly ablated (removed).
  * **_User-Defined Feature Impact_** - The User-Defined Feature Impact feature allows you to upload custom feature impact for models to execute Global model explanations in Fiddler and see the feature drift impact without the need to compute feature impact in Fiddler
    * Methods: upload_feature_impact: Accepts a dictionary of feature impact (key-value pairs of features and their impact) and an update flag (true or false).
    * Parameters:
      * feature_impact_map: Dictionary (key-value pairs of features and their impact)
      * update: Boolean (true or false)
    * Sample Usage :

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'
FEATURE_IMPACT_MAP = {'feature_1': 0.1, 'feature_2': 0.4}

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

feature_impacts = model.upload_feature_impact(feature_impact_map=FEATURE_IMPACT_MAP, update=False)
```
* **_Feature importance_** — Gives the average change in loss when a feature is randomly ablated.

## Language (NLP) Models

For language models, Fiddler’s Global Explanation performs ablation feature impact on a collection of text samples, determining which words have the most impact on the prediction.

> 📘 Info
>
> For speed performance, Fiddler uses a random corpus of 200 documents from the dataset. When using the [`run_feature_importance`](https://api.fiddler.ai/#client-run_feature_importance) function from the Fiddler API client, the argument `n_inputs` can be changed to use a bigger corpus of texts.

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
