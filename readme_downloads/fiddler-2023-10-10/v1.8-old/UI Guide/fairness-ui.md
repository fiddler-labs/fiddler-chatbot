---
title: "Fairness"
slug: "fairness-ui"
excerpt: "UI Guide"
hidden: false
createdAt: "2022-12-20T17:16:23.668Z"
updatedAt: "2022-12-20T17:27:52.786Z"
---
In the context of [intersectional fairness](doc:fairness#intersectional-fairness), we compute the [fairness metrics](doc:fairness#fairness-metrics) for each subgroup. The values should be similar among subgroups. If there exists some bias in the model, we display the min-max ratio, which takes the minimum value divided by the maximum value for a given metric. If this ratio is close to 1, then the metric is very similar among subgroups. The figure below gives an example of two protected attributes, Gender and Education, and the Equal Opportunity metric.

![](https://files.readme.io/906df04-intersectional_metrics.svg "intersectional_metrics.svg")

For the[ Disparate Impact metric](doc:fairness#disparate-impact), we don’t display a min-max ratio but an absolute min. The intersectional version of this metric is a little different. For a given subgroup, take all possible permutations of 2 subgroups and then display the minimum. If the absolute minimum is greater than 80%, then all combinations are greater than 80%.

## Model Behavior

In addition to the fairness metrics, we provide information about model outcomes and model performance for each subgroup. In the platform, you can see a visualization like the one below by default. You have the option to display the same numbers in a table for a deeper analysis.

![](https://files.readme.io/e03e620-model_behavior_1.svg "model_behavior_1.svg")

![](https://files.readme.io/ca0c5be-model_behavior_2.svg "model_behavior_2.svg")

## Dataset Fairness

Finally, we provide a section for dataset fairness, with a mutual information matrix and a label distribution. Note that this is a pre-modeling step.

![](https://files.readme.io/c96f7fd-data_fairness.svg "data_fairness.svg")

Mutual information gives information about existing dependence in your dataset between the protected attributes and the remaining features. We are displaying Normalized Mutual Information (NMI). This metric is symmetric, and has values between 0 and 1, where 1 means perfect dependency.

![](https://files.readme.io/a946365-mutual_info.svg "mutual_info.svg")

For more details about the implementation of the intersectional framework, please refer to this [research paper](https://arxiv.org/pdf/2101.01673.pdf).

## Reference

[^1]\: USEEOC article on [_Discrimination By Type_](https://www.eeoc.gov/discrimination-type)  
[^2]\:  USEEOC article on [_Intersectional Discrimination/Harassment_](https://www.eeoc.gov/initiatives/e-race/significant-eeoc-racecolor-casescovering-private-and-federal-sectors#intersectional)