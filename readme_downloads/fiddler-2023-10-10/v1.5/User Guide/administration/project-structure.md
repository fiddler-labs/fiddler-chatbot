---
title: "Project Structure"
slug: "project-structure"
hidden: false
createdAt: "2022-04-19T20:26:33.568Z"
updatedAt: "2022-09-14T20:04:04.614Z"
---
Supervised machine learning involves identifying a predictive task, finding data to enable that task, and building a model using that data. Fiddler captures this workflow with project, dataset, and model entities.

You can access your projects from the left-side menu.

## Projects

A project represents a machine learning task (e.g. predicting house prices, assessing creditworthiness, or detecting fraud).

A project can contain one or more models for the ML task (e.g. LinearRegression-HousePredict, RandomForest-HousePredict).

Create a project by clicking on **Projects** and then clicking on **Add Project**.

![](https://files.readme.io/8e4b429-Add_project_0710.png "Add_project_0710.png")



- **_Create New Project_** — A window will pop up where you can enter the project name and click **Create**. Once the project is created, it will be displayed on the projects page.

## Datasets

A dataset in Fiddler is a data table containing features, model outputs, and a target for machine learning models. Optionally, you can also upload metadata and “decision” columns, which can be used to segment the dataset for analyses, track business decisions, and work as protected attributes in bias-related workflows.

In order to monitor production data, a dataset must be uploaded to be used as a baseline for making comparisons. This baseline dataset should be sampled from your model's training data. The sample should be unbiased and should faithfully capture moments of the parent distribution. Further, values appearing in the baseline dataset's columns should be representative of their entire ranges within the complete training dataset.

**Datasets are used by Fiddler in the following ways:**

1. As a reference for drift calculations and data integrity violations on the `Monitor` page
2. To train a model to be used as a surrogate when using [`register_model`](https://api.fiddler.ai/#client-register_model)
3. For computing model performance metrics globally on the **Evaluate** page, or on slices on the **Analyze** page
4. As a reference for explainability algorithms (e.g. partial dependence plots, permutation feature impact, approximate Shapley values, and ICE plots).

Based on the above uses, datasets with sizes much in excess of 10K rows are often unnecessary and can lead to excessive upload, precomputation, and query times. That being said, here are some situations where larger datasets may be desirable:

- **Auto-modeling for tasks with significant class imbalance; or strong and complex feature interactions, possibly with deeply encoded semantics**
  - However, in use cases like these, most users opt to upload carefully-engineered model artifacts tailored to the specific application.
- **Deep segmentation analysis**
  - If it’s desirable to perform model analyses on very specific subpopulations (e.g. “55-year-old Canadian home-owners who have been customers between 18 and 24 months”), large datasets may be necessary to have sufficient reference representation to drive model analytics.

> 📘 Info
> 
> Datasets can be uploaded to Fiddler using the Python API client.

## Models

A model in Fiddler represents a machine learning model. A project will have one or more models for the ML task (e.g. a project to predict house prices might contain LinearRegression-HousePredict and RandomForest-HousePredict).

> 📘 Info
> 
> You can upload your model artifact to Fiddler to unlock high-fidelity explainability for your model. However, it is not required. If you do not upload your artifact, Fiddler will build a surrogate model on the backend to be used in its place.

![](https://files.readme.io/e151df5-Model_Dashboard.png "Model_Dashboard.png")



### Model Components

At its most basic level, a model in Fiddler is simply a directory that contains three key components:

1. The model file (e.g. `*.pkl`)
2. `model.yaml`: A YAML file containing all the metadata needed to describe the model, what goes into the model, and what should come out of it. This model metadata is used in Fiddler’s explanations, analytics, and UI.
3. `package.py`: A wrapper script containing all of the code needed to standardize the execution of the model.

![](https://files.readme.io/7170489-Model_Details.png "Model_Details.png")



![](https://files.readme.io/2b3d52e-Model_Details_1.png "Model_Details_1.png")



## Project Dashboard

You can collate specific visualizations under the Project Dashboard. After visualizations are created using the Model Analytics tool, you can pin them to the dashboard, which can then be shared with others.

![](https://files.readme.io/b7cb9ce-Chart_Dashboard.png "Chart_Dashboard.png")



[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_