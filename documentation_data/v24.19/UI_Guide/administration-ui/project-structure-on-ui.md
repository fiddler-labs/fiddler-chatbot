---
title: Project Structure on UI
slug: project-structure-on-ui
excerpt: >-
  This document provides information on how to create projects, models,
  datasets, and project dashboards within Fiddler for organizing and managing
  machine learning models.
hidden: true
metadata:
  description: >-
    This document provides information on how to create projects, models,
    datasets, and project dashboards within Fiddler for organizing and managing
    machine learning models.
  image: []
  robots: index
createdAt: Fri Apr 05 2024 11:20:17 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 11 2024 09:30:14 GMT+0000 (Coordinated Universal Time)
---

# Project Structure On Ui

A project within Fiddler helps organize models under observation. Additionally, a project acts as the authorization unit to govern access to your models. To onboard a model to Fiddler, you must first have a project with which you wish to associate it.

### Projects

Create a project by clicking on **Projects** and then clicking on **Add Project**.

![](../../.gitbook/assets/8e4b429-Add\_project\_0710.png)

* _**Create New Project**_ — A window will pop up where you can enter the project name and click **Create**. Once the project is created, it will be displayed on the projects page.

You can access your projects from the Projects Page.

![Projects Page on Fiddler UI](../../.gitbook/assets/82404e6-Screenshot\_2022-12-27\_at\_1.00.15\_PM.png)

Projects Page on Fiddler UI

### Models

A model in Fiddler represents a machine learning model. A project will have one or more models for the ML task (e.g. a project to predict house prices might contain LinearRegression-HousePredict and RandomForest-HousePredict). For further details refer to the [Models](doc:project-architecture#models) section in the Platform Guide.

You can create a model from the Fiddler Client

![](../../.gitbook/assets/e151df5-Model\_Dashboard.png)

### Datasets

A dataset in Fiddler is a data table containing features, model outputs, and a target for machine learning models. Optionally, you can also upload metadata and “decision” columns, which can be used to segment the dataset for analyses, track business decisions, and work as protected attributes in bias-related workflows. For more details refer to [Datasets](doc:project-architecture#datasets) in the Platform Guide.

Once you click on a particular project/model, you will be able to see if there are any datasets associated with the model. For example, the bank\_churn project, in the following screenshot, has the bank\_churn dataset. [Datasets are uploaded via the Fiddler client](../../Python_Client_2-x/api-methods-20.md#clientuploaddataset).

![Dataset and Baselines in a model](../../.gitbook/assets/d25c3a1-Screenshot\_2024-04-05\_at\_5.04.09\_PM.png)

Dataset and Baselines in a model

#### Model Schema and Artifacts

A model in Fiddler is simply a directory that contains [model Schema and artifacts](../../product-guide/explainability/artifacts-and-surrogates.md) such as:

* Input, Output, Prediction and Target column(s)
* The model file (e.g. `*.pkl`)
* `package.py`: A wrapper script containing all of the code needed to standardize the execution of the model.

![](../../.gitbook/assets/4b3f2d1-Screenshot\_2024-04-05\_at\_5.06.51\_PM.png)

![](../../.gitbook/assets/3897e25-Screenshot\_2024-04-05\_at\_5.04.09\_PM.png)

### Project Dashboard

You can collate specific visualizations under the Project Dashboard. After visualizations are created using the Model Analytics tool, you can pin them to the dashboard, which can then be shared with others.

![](../../.gitbook/assets/232cc47-Screenshot\_2024-04-05\_at\_5.12.51\_PM.png)

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
