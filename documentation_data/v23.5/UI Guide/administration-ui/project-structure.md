---
title: "Project Structure on UI"
slug: "project-structure"
hidden: false
createdAt: "2022-04-19T20:26:33.568Z"
updatedAt: "2023-10-19T20:59:24.625Z"
---
Supervised machine learning involves identifying a predictive task, finding data to enable that task, and building a model using that data. Fiddler captures this workflow with project, dataset, and model entities.

## Projects

A project represents a machine learning task (e.g. predicting house prices, assessing creditworthiness, or detecting fraud).

A project can contain one or more models for the ML task (e.g. LinearRegression-HousePredict, RandomForest-HousePredict).

Create a project by clicking on **Projects** and then clicking on **Add Project**.

![](https://files.readme.io/8e4b429-Add_project_0710.png "Add_project_0710.png")

- **_Create New Project_** — A window will pop up where you can enter the project name and click **Create**. Once the project is created, it will be displayed on the projects page.

You can access your projects from the Projects Page.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/82404e6-Screenshot_2022-12-27_at_1.00.15_PM.png",
        null,
        "Projects Page on Fiddler UI"
      ],
      "align": "center",
      "caption": "Projects Page on Fiddler UI"
    }
  ]
}
[/block]

## Datasets

A dataset in Fiddler is a data table containing features, model outputs, and a target for machine learning models. Optionally, you can also upload metadata and “decision” columns, which can be used to segment the dataset for analyses, track business decisions, and work as protected attributes in bias-related workflows. For more details refer to [Datasets](doc:project-architecture#datasets) in the Platform Guide.

Once you click on a particular project, you will be able to see if there are any datasets associated with the project. For example, the bank_churn project, in the following screenshot, has the bank_churn dataset. [Datasets are uploaded via the Fiddler client](ref:clientupload_dataset). 

![](https://files.readme.io/3fa7700-Screenshot_2022-12-27_at_1.05.05_PM.png)

## Models

A model in Fiddler represents a machine learning model. A project will have one or more models for the ML task (e.g. a project to predict house prices might contain LinearRegression-HousePredict and RandomForest-HousePredict). For further details refer to the [Models](doc:project-architecture#models) section in the Platform Guide.

![](https://files.readme.io/e151df5-Model_Dashboard.png "Model_Dashboard.png")

### Model Artifacts

At its most basic level, a model in Fiddler is simply a directory that contains [model artifacts](doc:artifacts-and-surrogates) such as:

- The model file (e.g. `*.pkl`)
- `package.py`: A wrapper script containing all of the code needed to standardize the execution of the model.

![](https://files.readme.io/7170489-Model_Details.png "Model_Details.png")

![](https://files.readme.io/2b3d52e-Model_Details_1.png "Model_Details_1.png")

## Project Dashboard

You can collate specific visualizations under the Project Dashboard. After visualizations are created using the Model Analytics tool, you can pin them to the dashboard, which can then be shared with others.

![](https://files.readme.io/b7cb9ce-Chart_Dashboard.png "Chart_Dashboard.png")

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_