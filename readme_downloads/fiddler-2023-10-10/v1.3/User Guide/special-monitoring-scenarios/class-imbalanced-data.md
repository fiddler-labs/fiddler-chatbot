---
title: "Class-Imbalanced Data"
slug: "class-imbalanced-data"
hidden: false
createdAt: "2022-07-05T17:20:48.830Z"
updatedAt: "2022-08-01T17:31:51.504Z"
---
Monitoring class-imbalanced models
----------------------------------

Drift is a measure of how different the production distribution is from the baseline distribution on which the model was trained. In practice, the distributions are approximated using histograms and then compared using divergence metrics like Jensen–Shannon divergence or Population Stability Index. Generally when constructing the histograms, every event contributes equally to the bin counts.

However, for scenarios with large class imbalance the minority class’ contribution to the histograms would be minimal. Hence, any change in production distribution with respect to minority class would not lead to significant change in the production histograms. Consequently, even if there is a significant change in distribution with respect to the minority class, the drift value would not change significantly.

To solve this issue, Fiddler monitoring provides a way for events to be weighted based on class distribution. For such models, when computing the histograms, events belonging to minority class would be up-weighted whereas those belonging to majority class would be down-weighted.

Fiddler has implemented two solutions for class imbalance use cases.

**Workflow 1: User provided global class weights**  
User computes the class distribution on baseline data and then provides the class-weights via Model-Info object.  
Class weights can either be manually entered by the user or computed from their dataset

- Please refer to the API docs on how to [specify global class-weights](/reference/fdlweightingparams)

- To tease out drift in a class-imbalanced fraud-usecase checkout out the [class-imbalanced-fraud-notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/business-use-cases/class-imbalance/class_weighted_drift.ipynb)

**Workflow 2: User provided event level weights**  
User provides event level weights as a metadata column in baseline data and provides them while publishing events  
Details:

- Users will add an "\_\_weight" column in their model_info (must be a metadata type column, and must be nullable=True).

- The reference data needs to have an "\_\_weight" column, which may never be all null/missing/NaN  weights; all rows must contain valid float values. We expect the user to enforce this assumption.

- Note that the use of weighting parameters requires the presence of model outputs for both workflows in the baseline dataset.  
  **Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]\: _Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions_