---
title: Global Explainability
slug: global-explainability-platform
excerpt: ''
createdAt: Fri Nov 18 2022 22:57:28 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 20:45:00 GMT+0000 (Coordinated Universal Time)
---

# Global Explainability

Fiddler provides powerful visualizations to describe the impact of features in your model. Feature impact and importance can be found in either the Explain or Analyze tab.

Global explanations are available in the UI for **structured (tabular)** and **natural language (NLP)** models, for both classification and regression. They are also supported via API using the Fiddler Python package. Global explanations are available for both production and dataset queries.

### Tabular Models

For tabular models, Fiddler’s Global Explanation tool shows the impact/importance of the features in the model.

Two global explanation methods are available:

* _**Feature importance**_ — Gives the average change in loss when a feature is randomly ablated.
* _**Feature impact**_ — Gives the average absolute change in the model prediction when a feature is randomly ablated (removed).
  * _**Custom Feature Impact**_
    * Overview
      * The Custom Feature Impact feature empowers you to provide your feature impact scores for your models, leveraging domain-specific knowledge or external data to inform feature importance. This feature enables you to upload custom feature impact data without requiring the corresponding model artifact.
    * How to Use
      * Prepare Your Data
        * Gather feature names and corresponding impact scores for your model.
        * Ensure impact scores are numeric values; negative values indicate inverse relationships.
      * Upload Feature Impact Data
        * Use the provided API endpoint to upload your data.
        * Required parameters:
          * Model UUID: Unique identifier of your model.
          * Feature Names: List of feature names.
          * Impact Scores: List of corresponding impact scores.
      * View Updated Model Information
        * After successful upload, updated feature impact data will be reflected in:
          * Model details page
          * Charts page
          * Explain page
        * Visualize feature impact scores in charts and explanations.
    * Important Notes
      * Error handling: API returns detailed error messages to help resolve issues.
      * Update existing feature impact data by uploading new data for the same model.
      * If you upload feature impact data for a model with an existing artifact, the artifact will be updated.
      * Missing feature impact data may display a tooltip or message; upload data manually or compute using other tools.
    * Methods:
      * `upload_feature_impact`: Accepts a dictionary of feature impact (key-value pairs of features and their impact) and an update flag (True or False).
    * Parameters:
      * `feature_impact_map`: Dictionary (key-value pairs of features and their impact)
      * `update`: Boolean (true or false)
    *   Sample Usage :

        ```python
        PROJECT_NAME = 'YOUR_PROJECT_NAME'
        MODEL_NAME = 'YOUR_MODEL_NAME'
        FEATURE_IMPACT_MAP = {'feature_1': 0.1, 'feature_2': 0.4}
        project = fdl.Project.from_name(name=PROJECT_NAME)
        model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
        feature_impacts = model.upload_feature_impact(feature_impact_map=FEATURE_IMPACT_MAP, update=False)
        ```

### Language (NLP) Models

For language models, Fiddler’s Global Explanation performs ablation feature impact on a collection of text samples, determining which words have the most impact on the prediction.

> 📘 Info
>
> For speed performance, Fiddler uses a random corpus of 200 documents from the dataset. When using the [`get_feature_importance`](../../Python\_Client\_3-x/api-methods-30.md#get\_feature\_importance) function from the Fiddler API client, the argument `num_refs` can be changed to use a bigger corpus of texts.

{% include "../../.gitbook/includes/main-doc-footer.md" %}

