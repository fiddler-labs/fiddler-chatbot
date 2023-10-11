---
title: "Product Tour"
slug: "product-tour"
excerpt: "Here's a tour of our product UI!"
hidden: false
createdAt: "2022-04-19T20:09:29.819Z"
updatedAt: "2023-02-03T20:45:51.481Z"
---
When you log in to Fiddler, you are on the Home page and you can visualize monitoring information for your models across all your projects. 

- At the top of the page, you will see donut charts for the number of triggered alerts for [Performance](doc:performance-tracking-platform), [Data Drift](doc:data-drift-platform), and [Data Integrity](doc:data-integrity-platform). 
- To the right of the donut charts, you will find the Recent Job Status card that lets you keep track of long-running async jobs and whether they have failed, are in progress, or successfully completed. 
- The [Monitoring](doc:monitoring-ui) Summary table displays your models across different [projects](doc:project-architecture) along with information on their traffic, drift, and the number of triggered alerts.

![](https://files.readme.io/2e4fb2f-Screen_Shot_2022-07-29_at_12.01.29_PM.png)

On the navigation bar at the top, next to the Home Tab, is the [Projects](doc:project-structure) Tab. You can click on the Projects tab and it lands on a page that lists all your projects contained within Fiddler. See the [Fiddler Samples](doc:product-tour#fiddler-samples)  section below for more information on these projects. You can create new projects within the UI (by clicking the “New Project” button) or via the [Fiddler Client](ref:about-the-fiddler-client).

![](https://files.readme.io/6b0dc77-Screen_Shot_2022-07-29_at_12.01.57_PM.png)

**Projects** represent your organization's distinct AI applications or use cases. Within Fiddler, Projects house all the **Models** specific to a given application, and thus serve as a jumping-off point for the majority of Fiddler’s model monitoring and explainability features.

Go ahead and click on the _Lending project_ to navigate to the Project Overview page.

![](https://files.readme.io/0b7afc0-Screen_Shot_2022-07-29_at_12.02.47_PM.png)

Here you can see a list of the models contained within the Lending project, as well as a project dashboard to which various insights can be pinned. Go ahead and click the “logreg-all” model.

![](https://files.readme.io/fa956eb-Screen_Shot_2022-07-29_at_12.02.19_PM.png)

From the Model Overview page, you can view details about the model: its metadata (schema), the files in its model directory, and its features, which are sorted by impact (the degree to which each feature influences the model’s prediction score).

You can then navigate to the platform's core monitoring and explainability capabilities. These include:

- **_Monitor_** — Track and configure alerts on your model’s performance, data drift, data integrity, and overall service metrics. Read the [Monitoring](doc:monitoring-platform) documentation for more details.
- **_Analyze_** — Analyze the behavior of your model in aggregate or with respect to specific segments of your population. Read the [Analytics](doc:analytics-ui) documentation for more details.
- **_Explain_** — Generate “point” or prediction-level explanations on your training or production data for insight into how each model decision was made. Read the [Explainability](doc:explainability-platform) documentation for more details.
- **_Evaluate_** — View your model’s performance on its training and test sets for quick validation prior to deployment. Read the [Evaluation](doc:evaluation-ui) documentation for more details.

## Fiddler Samples

Fiddler Samples is a set of datasets and models that are preloaded into Fiddler. These samples are also available in the [Samples git repo](https://github.com/fiddler-labs/fiddler-samples/tree/master/content_root/samples). They represent different data types, model frameworks, and machine learning techniques. See the table below for more details.

| **Project**   | **Model**                       | **Dataset** | **Model Framework** | **Algorithm**       | **Model Task**             | **Explanation Algos** |
| ------------- | ------------------------------- | ----------- | ------------------- | ------------------- | -------------------------- | --------------------- |
| Bank Churn    | Bank Churn                      | Tabular     | scikit-learn        | Random Forest       | Binary Classification      | Fiddler Shapley       |
| Heart Disease | Heart Disease                   | Tabular     | Tensorflow          |                     | Binary Classification      | Fiddler Shapley, IG   |
| IMDB          | Imdb Rnn                        | Text        | Tensorflow          | BiLSTM              | Binary Classfication       | Fiddler Shapley, IG   |
| Iris          | Iris                            | Tabular     | scikit-learn        | Logistic Regression | Multi-class Classification | Fiddler Shapley       |
| Lending       | Logreg-all                      | Tabular     | scikit-learn        | Logistic Regression | Binary Classification      | Fiddler Shapley       |
|               | Logreg-simple                   | Tabular     | scikit-learn        | Logistic Regression | Binary Classification      | Fiddler Shapley       |
|               | Xgboost-simple-sagemaker        | Tabular     | scikit-learn        | XGboost             | Binary Classification      | Fiddler Shapley       |
| Newsgroup     | Christianity Atheism Classifier | Text        | scikit-learn        | Random Forest       | Binary Classification      | Fiddler Shapley       |
| Wine Quality  | Linear Model Wine Regressor     | Tabular     | scikit-learn        | Elastic Net         | Regression                 | Fiddler Shapley       |
|               | DNN Wine Regressor              | Tabular     | Tensorflow          |                     | Regression                 | Fiddler Shapley       |

See the [README](https://github.com/fiddler-labs/fiddler-samples/blob/master/README.md) for more information.

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_