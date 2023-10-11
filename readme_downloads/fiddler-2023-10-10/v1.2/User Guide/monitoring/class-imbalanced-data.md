---
title: "Class-Imbalanced Data"
slug: "class-imbalanced-data"
hidden: false
createdAt: "2022-07-05T17:20:48.830Z"
updatedAt: "2022-07-06T16:29:11.907Z"
---
[block:api-header]
{
  "title": "Monitoring class-imbalanced models"
}
[/block]
Drift is a measure of how different the production distribution is from the baseline distribution on which the model was trained. In practice, the distributions are approximated using histograms and then compared using divergence metrics like Jensen–Shannon divergence or Population Stability Index. Generally when constructing the histograms, every event contributes equally to the bin counts.

However, for scenarios with large class imbalance the minority class’ contribution to the histograms would be minimal. Hence, any change in production distribution with respect to minority class would not lead to significant change in the production histograms. Consequently, even if there is a significant change in distribution with respect to the minority class, the drift value would not change significantly.

To solve this issue, Fiddler monitoring provides a way for events to be weighted based on class distribution. For such models, when computing the histograms, events belonging to minority class would be up-weighted whereas those belonging to majority class would be down-weighted.

* Please refer to the API docs on how to [specify class-weights](/reference/fdlweightingparams)
* To tease out drift in a class-imbalanced fraud-usecase checkout out the [class-imbalanced-fraud-notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/business-use-cases/class-imbalance/class_weighted_drift.ipynb)
* Note that the use of weighting parameters requires the presence of model outputs in the baseline dataset.
**Reference**

* See our article on [_The Rise of MLOps Monitoring_](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*