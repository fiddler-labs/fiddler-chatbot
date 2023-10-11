---
title: "Product Tour"
slug: "product-tour"
hidden: false
createdAt: "2022-04-19T20:09:29.819Z"
updatedAt: "2022-06-13T20:00:35.789Z"
---
When you first login to Fiddler, you will land on the product homepage, which contains an introductory video to the Fiddler platform and links to the documentation with in-depth look into the Fiddler platform. It also provides information on recently viewed projects, starred projects, and more.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b2d6b15-Home_Page.png",
        "Home_Page.png",
        2880,
        1530,
        "#c7c9cd"
      ],
      "caption": ""
    }
  ]
}
[/block]
You can go to the Model Monitoring Summary page from the side tab, which will give details of traffic, drift, data integrity violations, and triggered alerts on your models.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e48d983-Monitoring_Summary.png",
        "Monitoring_Summary.png",
        2856,
        1528,
        "#f2f4f8"
      ],
      "caption": ""
    }
  ]
}
[/block]
You can also go to the Project page from the side tab, which lists all the data science projects contained within Fiddler. For more information on these projects, see the [Fiddler Samples](doc:product-tour#fiddler-samples)  section below. You can create new projects either within the UI (by clicking the “Add Project” button) or via the [Fiddler Client](ref:about-the-fiddler-client) .
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/890fd13-Project_Landing.png",
        "Project_Landing.png",
        2880,
        1530,
        "#f1f2f7"
      ],
      "caption": ""
    }
  ]
}
[/block]
Projects represent the distinct AI applications or use cases within your organization. Within Fiddler, they house all the models specific to a given application, and thus serve as a jumping-off point for the majority of Fiddler’s model monitoring and explainability features.

Go ahead and click on the Lending project to navigate to the Project Overview page.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/666051e-Project_Detail.png",
        "Project_Detail.png",
        2880,
        1528,
        "#f1f2f7"
      ],
      "caption": ""
    }
  ]
}
[/block]
Here you can see a list of the models contained within the Lending project, as well as a project dashboard to which various insights can be pinned. Go ahead and click the “logreg-all” model.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/409ea9d-Model_Detail.png",
        "Model_Detail.png",
        2880,
        1530,
        "#f1f2f7"
      ],
      "caption": ""
    }
  ]
}
[/block]
From the Model Overview page, you can view details about the model: its metadata (schema), the files in its model directory, and its features, which are sorted by impact (the degree to which each feature influences the model’s prediction score).

You can then navigate to the core monitoring and explainability capabilities within the platform. These include:

* ***Monitor*** — Track and configure alerts on your model’s performance, data drift, data integrity, and overall service metrics. Read the [Monitoring](doc:monitoring) documentation for more details.
* ***Analyze*** — Analyze the behavior of your model in aggregate or with respect to specific segments of your population. Read the [Analytics](doc:analytics) documentation for more details.
* ***Explain*** — Generate “point” or prediction-level explanations on your training or production data for insight into how each model decision was made. Read the [Explainability](doc:explainability) documentation for more details.
* ***Evaluate*** — View your model’s performance on its training and test sets for quick validation prior to deployment. Read the [Evaluation](doc:evaluation) documentation for more details.
[block:api-header]
{
  "title": "Fiddler Samples"
}
[/block]
Fiddler Samples is a set of datasets and models that are preloaded into Fiddler. These samples are also available in the [Samples git repo](https://github.com/fiddler-labs/fiddler-samples/tree/master/content_root/samples). They represent different data types, model frameworks, and machine learning techniques. See the table below for more details.

| __Project__ | __Model__ | __Dataset__ | __Model Framework__ | __Algorithm__ | __Model Task__ | __Explanation Algos__ |
|-	|-	|-	|-	|-	|-	|-	|
| Bank Churn 	| Bank Churn 	| Tabular 	| scikit-learn 	| Random Forest 	| Binary Classification 	| Fiddler Shapley 	|
| Heart Disease 	| Heart Disease 	| Tabular 	| Tensorflow 	|  	| Binary Classification 	| Fiddler Shapley, IG 	|
| IMDB 	| Imdb Rnn 	| Text 	| Tensorflow 	| BiLSTM 	| Binary Classfication 	| Fiddler Shapley, IG 	|
| Iris 	| Iris 	| Tabular 	| scikit-learn 	| Logistic Regression 	| Multi-class Classification 	| Fiddler Shapley 	|
| Lending 	| Logreg-all 	| Tabular 	| scikit-learn 	| Logistic Regression 	| Binary Classification 	| Fiddler Shapley 	|
|  	| Logreg-simple 	| Tabular 	| scikit-learn 	| Logistic Regression 	| Binary Classification 	| Fiddler Shapley 	|
|  	| Xgboost-simple-sagemaker 	| Tabular 	| scikit-learn 	| XGboost 	| Binary Classification 	| Fiddler Shapley 	|
| Newsgroup 	| Christianity Atheism Classifier 	| Text 	| scikit-learn 	| Random Forest 	| Binary Classification 	| Fiddler Shapley 	|
| Wine Quality 	| Linear Model Wine Regressor 	| Tabular 	| scikit-learn 	| Elastic Net 	| Regression 	| Fiddler Shapley 	|
|  	| DNN Wine Regressor 	| Tabular 	| Tensorflow 	|  	| Regression 	| Fiddler Shapley	|

See the [README](https://github.com/fiddler-labs/fiddler-samples/blob/master/README.md) for more information.

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*