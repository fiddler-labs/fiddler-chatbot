---
title: "Product Tour"
slug: "product-tour"
hidden: false
createdAt: "2022-04-19T20:09:29.819Z"
updatedAt: "2022-07-29T19:23:38.236Z"
---
When you first login to Fiddler, you will land on the Single Pane of Glass product homepage. In this view you can visualize monitoring information for your models across all your projects. At the top of the page you will see an overview of the number of triggered alerts for Performance, Data Drift, and Data Integrity alerts. Beside these donuts charts, you will find the Recent Job Status card that let's you keep track of long running async jobs and whether they have failed, are in progress, or completed successfully. Below this, is the Monitoring Summary table which displays your models across different projects along with information on their traffic, drift, and number of triggered alerts.

![](https://files.readme.io/2e4fb2f-Screen_Shot_2022-07-29_at_12.01.29_PM.png)

You can also go to the Project page by clicking on the Projects tab from the top lever navigation bar. This page lists all the data science projects contained within Fiddler. For more information on these projects, see the [Fiddler Samples](doc:product-tour#fiddler-samples)  section below. You can create new projects either within the UI (by clicking the “Add Project” button) or via the [Fiddler Client](ref:about-the-fiddler-client) .

![](https://files.readme.io/6b0dc77-Screen_Shot_2022-07-29_at_12.01.57_PM.png)

Projects represent the distinct AI applications or use cases within your organization. Within Fiddler, they house all the models specific to a given application, and thus serve as a jumping-off point for the majority of Fiddler’s model monitoring and explainability features.

Go ahead and click on the Lending project to navigate to the Project Overview page.

![](https://files.readme.io/0b7afc0-Screen_Shot_2022-07-29_at_12.02.47_PM.png)

Here you can see a list of the models contained within the Lending project, as well as a project dashboard to which various insights can be pinned. Go ahead and click the “logreg-all” model.

![](https://files.readme.io/fa956eb-Screen_Shot_2022-07-29_at_12.02.19_PM.png)

From the Model Overview page, you can view details about the model: its metadata (schema), the files in its model directory, and its features, which are sorted by impact (the degree to which each feature influences the model’s prediction score).

You can then navigate to the core monitoring and explainability capabilities within the platform. These include:

- **_Monitor_** — Track and configure alerts on your model’s performance, data drift, data integrity, and overall service metrics. Read the [Monitoring](doc:monitoring) documentation for more details.
- **_Analyze_** — Analyze the behavior of your model in aggregate or with respect to specific segments of your population. Read the [Analytics](doc:analytics) documentation for more details.
- **_Explain_** — Generate “point” or prediction-level explanations on your training or production data for insight into how each model decision was made. Read the [Explainability](doc:explainability) documentation for more details.
- **_Evaluate_** — View your model’s performance on its training and test sets for quick validation prior to deployment. Read the [Evaluation](doc:evaluation) documentation for more details.

Fiddler Samples
---------------

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

[^1]\: _Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions_