---
title: Performance
slug: performance
excerpt: ''
createdAt: Tue Apr 19 2022 20:25:22 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 22 2024 15:58:55 GMT+0000 (Coordinated Universal Time)
---

# Performance

### What is being tracked?

![](../../.gitbook/assets/ffefe4c-image.png)

* _**Decisions**_ - The post-prediction business decisions made as a result of the model output. Decisions are calculated before [model.publish()](../../Python\_Client\_3-x/api-methods-30.md#publish) (they're not inferred by Fiddler). For binary classification models, a decision is usually determined using a threshold. For multi-class classification models, it's usually determined using the argmax value of the model outputs.
* _**Performance metrics**_
  1. For binary classification models:
     * Accuracy
     * True Positive Rate/Recall
     * False Positive Rate
     * Precision
     * F1 Score
     * AUC
     * AUROC
     * Binary Cross Entropy
     * Geometric Mean
     * Calibrated Threshold
     * Data Count
     * Expected Calibration Error
  2. For multi-class classification models:
     * Accuracy
     * Log loss
  3. For regression models:
     * Coefficient of determination (R-squared)
     * Mean Squared Error (MSE)
     * Mean Absolute Error (MAE)
     * Mean Absolute Percentage Error (MAPE)
     * Weighted Mean Absolute Percentage Error (WMAPE)
  4. For ranking models:
     * Mean Average Precision (MAP)—for binary relevance ranking only
     * Normalized Discounted Cumulative Gain (NDCG)

### Why is it being tracked?

* Model performance tells us how well a model is doing on its task. A poorly performing model can have significant business implications.
* The volume of decisions made on the basis of the predictions give visibility into the business impact of the model.

### What steps should I take based on this information?

* For decisions, if there is an increase or decrease in approvals, we can cross-check with the average prediction and prediction drift trendlines on the [Data Drift Tab](data-drift.md). In general, the average prediction value should increase with an increase in the number of approvals, and vice-versa.
* For changes in model performance—again, the best way to cross-verify the results is by checking the [Data Drift Tab](data-drift.md) ). Once you confirm that the performance issue is not due to the data, you need to assess if the change in performance is due to temporary factors, or due to longer-lasting issues.
* You can check if there are any lightweight changes you can make to help recover performance—for example, you could try modifying the decision threshold.
* Retraining the model with the latest data and redeploying it is usually the solution that yields the best results, although it may be time-consuming and expensive.

{% include "../../.gitbook/includes/main-doc-footer.md" %}

