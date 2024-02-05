---
title: "Project Architecture"
slug: "project-architecture"
excerpt: ""
hidden: false
createdAt: "Tue Nov 15 2022 18:06:28 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:58:14 GMT+0000 (Coordinated Universal Time)"
---
Supervised machine learning involves identifying a predictive task, finding data to enable that task, and building a model using that data. 

Fiddler captures this workflow with **project**, **dataset**, and **model** entities.

## Project

In Fiddler, a project is essentially a parent folder that hosts one or more **model** (s) for the ML task (e.g. A Project HousePredict for predicting house prices will LinearRegression-HousePredict, RandomForest-HousePredict).

## Models

A model in Fiddler represents a **placeholder** for a machine-learning model. It's a placeholder because we may not need the **[model artifacts](doc:artifacts-and-surrogates#Model-Artifacts)**. Instead, we may just need adequate [information about the model](ref:fdlmodelinfo) in order to monitor model-specific data. 

> 📘 Info
> 
> You can [upload your model artifacts](https://dash.readme.com/project/fiddler/v1.6/docs/uploading-model-artifacts) to Fiddler to unlock high-fidelity explainability for your model. However, it is not required. If you do not wish to upload your artifact but want to explore explainability with Fiddler, we can build a [**surrogate model**](doc:artifacts-and-surrogates#surrogate-model) on the backend to be used in place of your artifact.

## Datasets

A dataset in Fiddler is a data table containing [information about data](ref:fdldatasetinfo) such as **features**, **model outputs**, and a **target** for machine learning models. Optionally, you can also upload **metadata** and “**decision**” columns, which can be used to segment the dataset for analyses, track business decisions, and work as protected attributes in bias-related workflows. 

In order to monitor **production data**, a [dataset must be uploaded](ref:clientupload_dataset) to be used as a **baseline** for making comparisons. This baseline dataset should be sampled from your model's **training data**. The sample should be unbiased and should faithfully capture moments of the parent distribution. Further, values appearing in the baseline dataset's columns should be representative of their entire ranges within the complete training dataset.

**Datasets are used by Fiddler in the following ways:**

1. As a reference for [drift calculations](doc:data-drift-platform) and [data integrity violations ](doc:data-integrity-platform)on the **[Monitor](doc:monitoring-ui)** page
2. To train a model to be used as a [surrogate](doc:artifacts-and-surrogates#surrogate-model) when using [`add_model_surrogate`](/reference/clientadd_model_surrogate)
3. For computing model performance metrics globally on the **[Evaluate](doc:evaluation-ui)** page, or on slices on the **[Analyze](doc:analytics-ui)** page
4. As a reference for explainability algorithms (e.g. partial dependence plots, permutation feature impact, approximate Shapley values, and ICE plots).

Based on the above uses, _datasets with sizes much in excess of 10K rows are often unnecessary_ and can lead to excessive upload, precomputation, and query times. That being said, here are some situations where larger datasets may be desirable:

- **Auto-modeling for tasks with significant class imbalance; or strong and complex feature interactions, possibly with deeply encoded semantics**
  - However, in use cases like these, most users opt to upload carefully-engineered model artifacts tailored to the specific application.
- **Deep segmentation analysis**
  - If it’s desirable to perform model analyses on very specific subpopulations (e.g. “55-year-old Canadian home-owners who have been customers between 18 and 24 months”), large datasets may be necessary to have sufficient reference representation to drive model analytics.

> 📘 Info
> 
> Datasets can be uploaded to Fiddler using the[ Python API client](doc:installation-and-setup).

 [Check the UI Guide to Visualize Project Architecture on our User Interface](doc:project-structure)

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
