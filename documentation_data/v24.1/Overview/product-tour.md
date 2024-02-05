---
title: "Product Tour"
slug: "product-tour"
excerpt: "Here's a tour of our product UI!"
hidden: false
metadata: 
  title: "Product Tour | Fiddler Docs"
  description: "Take a tour of Fiddler AI Observability platform."
  image: []
  robots: "index"
createdAt: "Tue Apr 19 2022 20:09:29 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 17 2024 22:14:18 GMT+0000 (Coordinated Universal Time)"
---
# Video Demo

Watch the video to learn how Fiddler AI Observability provides data science and MLOps teams with a unified platform to monitor, analyze, explain, and improve machine learning models at scale, and build trust in AI.

[block:embed]
{
  "html": "<iframe class=\"embedly-embed\" src=\"//cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fwww.youtube.com%2Fembed%2FPENnn3YUAcg&display_name=YouTube&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DPENnn3YUAcg&image=http%3A%2F%2Fi.ytimg.com%2Fvi%2FPENnn3YUAcg%2Fhqdefault.jpg&key=7788cb384c9f4d5dbbdbeffd9fe4b92f&type=text%2Fhtml&schema=youtube\" width=\"854\" height=\"480\" scrolling=\"no\" title=\"YouTube embed\" frameborder=\"0\" allow=\"autoplay; fullscreen\" allowfullscreen=\"true\"></iframe>",
  "url": "https://www.youtube.com/watch?v=PENnn3YUAcg",
  "favicon": "https://www.google.com/favicon.ico",
  "image": "http://i.ytimg.com/vi/PENnn3YUAcg/hqdefault.jpg",
  "provider": "youtube.com",
  "href": "https://www.youtube.com/watch?v=PENnn3YUAcg",
  "typeOfEmbed": "youtube"
}
[/block]


# Documented UI Tour

When you log in to Fiddler, you are on the Home page and you can visualize monitoring information for your models across all your projects. 

- At the top of the page, you will see donut charts for the number of triggered alerts for [Performance](doc:performance-tracking-platform), [Data Drift](doc:data-drift-platform), and [Data Integrity](doc:data-integrity-platform). 
- To the right of the donut charts, you will find the Bookmarks as well as a Recent Job Status card that lets you keep track of long-running async jobs and whether they have failed, are in progress, or successfully completed. 
- The [Monitoring](doc:monitoring-ui) summary table displays your models across different [projects](doc:project-architecture) along with information on their traffic, drift, and the number of triggered alerts.

![](https://files.readme.io/31f5f2a-image.png)

View all of your bookmarked, Projects, Models, Datasets, Charts, and Dashboards by clicking "View All" on the Bookmarks card on the homepage or navigating directly to Bookmarks via the navigation bar.

![](https://files.readme.io/aad0a68-image.png)

Track all of your ongoing and completed model, dataset, and event publish jobs by clicking "View All" on the Jobs card on the homepage or navigating directly to the Jobs via the navigation bar.

![](https://files.readme.io/f914df5-image.png)

On the side navigation bar, below charts, is the [Projects](doc:project-structure) Tab. You can click on the Projects tab and it lands on a page that lists all your projects contained within Fiddler. See the [Fiddler Samples](doc:product-tour#fiddler-samples)  section below for more information on these projects. You can create new projects within the UI (by clicking the “Add Project” button) or via the [Fiddler Client](ref:about-the-fiddler-client).

![](https://files.readme.io/8a47f0a-image.png)

**Projects** represent your organization's distinct AI applications or use cases. Within Fiddler, Projects house all the **Models** specific to a given application, and thus serve as a jumping-off point for the majority of Fiddler’s model monitoring and explainability features.

Go ahead and click on the _bank_churn_ to navigate to the Project Overview page.

![](https://files.readme.io/a4e5021-image.png)

Here you can see a list of the models contained within the fraud detection project, as well as a project dashboard to which analyze charts can be pinned. Go ahead and click the “churn_classifier” model.

![](https://files.readme.io/6154301-image.png)

From the Model Overview page, you can view details about the model: its metadata (schema), the files in its model directory, and its features, which are sorted by impact (the degree to which each feature influences the model’s prediction score).

You can then navigate to the platform's core monitoring and explainability capabilities. These include:

- **_Monitor_** — Track and configure alerts on your model’s performance, data drift, data integrity, and overall service metrics. Read the [Monitoring](doc:monitoring-platform) documentation for more details.
- **_Analyze_** — Analyze the behavior of your model in aggregate or with respect to specific segments of your population. Read the [Analytics](doc:analytics-ui) documentation for more details.
- **_Explain_** — Generate “point” or prediction-level explanations on your training or production data for insight into how each model decision was made. Read the [Explainability](doc:explainability-platform) documentation for more details.
- **_Evaluate_** — View your model’s performance on its training and test sets for quick validation prior to deployment. Read the [Evaluation](doc:evaluation-ui) documentation for more details.

## Fiddler Samples

Fiddler Samples is a set of datasets and models that are preloaded into Fiddler. They represent different data types, model frameworks, and machine learning techniques. See the table below for more details.

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

See the [README](https://github.com/fiddler-labs/fiddler-examples) for more information.

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/demo?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/4d190fd-fiddler-docs-cta-demo.png\" alt=\"Fiddler Demo\"></a>\n</div>"
}
[/block]
