---
title: "Performance"
slug: "performance"
hidden: false
createdAt: "2022-04-19T20:25:22.895Z"
updatedAt: "2022-06-13T19:52:07.706Z"
---
[block:api-header]
{
  "title": "What is being tracked?"
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4a646d4-qs_monitoring.png",
        "qs_monitoring.png",
        3156,
        1610,
        "#fcfdfd"
      ]
    }
  ]
}
[/block]
* **_Decisions_** - The post-prediction business decisions made as a result of the model output. Decisions are calculated before [client.publish_event()](ref:clientpublish_event) (they're not inferred by Fiddler). For binary classification models, a decision is usually determined using a threshold. For multi-class classification models, it's usually determined using the argmax value of the model outputs.

* **_Performance metrics_**
    1. For binary classification models:
        * Accuracy
        * True Positive Rate/Recall
        * False Positive Rate
        * Precision
        * F1 Score
        * AUC
    2. For multi-class classification models:
        * Accuracy
        * Log loss
    3. For regression models:
        * Coefficient of determination (R-squared)
        * Mean Squared Error
        * Mean Absolute Error
    4. For ranking models:
        * Mean Average Precision (MAP)—for binary relevance ranking only
        * Normalized Discounted Cumulative Gain (NDCG)
[block:api-header]
{
  "title": "Why is it being tracked?"
}
[/block]
* Model performance tells us how well a model is doing on its task. A poorly performing model can have significant business implications.
* The volume of decisions made on the basis of the predictions give visibility into the business impact of the model.
[block:api-header]
{
  "title": "What steps should I take based on this information?"
}
[/block]
* For decisions, if there is an increase or decrease in approvals, we can cross-check with the average prediction and prediction drift trendlines on the [Data Drift Tab](doc:data-drift). In general, the average prediction value should increase with an increase in the number of approvals, and vice-versa.
* For changes in model performance—again, the best way to cross-verify the results is by checking the [Data Drift Tab](doc:data-drift) ). Once you confirm that the performance issue is not due to the data, you need to assess if the change in performance is due to temporary factors, or due to longer-lasting issues.
* You can check if there are any lightweight changes you can make to help recover performance—for example, you could try modifying the decision threshold.
* Retraining the model with the latest data and redeploying it is usually the solution that yields the best results, although it may be time-consuming and expensive.


**Reference**

* See our article on [*The Rise of MLOps Monitoring*](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*