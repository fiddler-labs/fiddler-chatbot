---
title: "Performance"
slug: "performance"
hidden: false
createdAt: "2022-04-19T20:25:22.895Z"
updatedAt: "2023-02-14T01:18:55.377Z"
---
## What is being tracked?

![](https://files.readme.io/4a646d4-qs_monitoring.png "qs_monitoring.png")

- **_Decisions_** - The post-prediction business decisions made as a result of the model output. Decisions are calculated before [client.publish_event()](ref:clientpublish_event) (they're not inferred by Fiddler). For binary classification models, a decision is usually determined using a threshold. For multi-class classification models, it's usually determined using the argmax value of the model outputs.

- **_Performance metrics_**
  1. For binary classification models:
     - Accuracy
     - True Positive Rate/Recall
     - False Positive Rate
     - Precision
     - F1 Score
     - AUC
     - AUROC
     - Binary Cross Entropy
     - Geometric Mean
     - Calibrated Threshold
     - Data Count
     - Expected Calibration Error
  2. For multi-class classification models:
     - Accuracy
     - Log loss
  3. For regression models:
     - Coefficient of determination (R-squared)
     - Mean Squared Error (MSE)
     - Mean Absolute Error (MAE)
     - Mean Absolute Percentage Error (MAPE)
     - Weighted Mean Absolute Percentage Error (WMAPE)
  4. For ranking models:
     - Mean Average Precision (MAP)—for binary relevance ranking only
     - Normalized Discounted Cumulative Gain (NDCG)

## Why is it being tracked?

- Model performance tells us how well a model is doing on its task. A poorly performing model can have significant business implications.
- The volume of decisions made on the basis of the predictions give visibility into the business impact of the model.

## What steps should I take based on this information?

- For decisions, if there is an increase or decrease in approvals, we can cross-check with the average prediction and prediction drift trendlines on the [Data Drift Tab](doc:data-drift). In general, the average prediction value should increase with an increase in the number of approvals, and vice-versa.
- For changes in model performance—again, the best way to cross-verify the results is by checking the [Data Drift Tab](doc:data-drift) ). Once you confirm that the performance issue is not due to the data, you need to assess if the change in performance is due to temporary factors, or due to longer-lasting issues.
- You can check if there are any lightweight changes you can make to help recover performance—for example, you could try modifying the decision threshold.
- Retraining the model with the latest data and redeploying it is usually the solution that yields the best results, although it may be time-consuming and expensive.

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_



[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/trial?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/af83f1a-fiddler-docs-cta-trial.png\" alt=\"Fiddler Free Trial\"></a>\n</div>"
}
[/block]