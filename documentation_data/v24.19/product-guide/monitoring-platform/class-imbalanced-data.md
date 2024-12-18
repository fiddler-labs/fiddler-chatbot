---
title: Class-Imbalanced Data
slug: class-imbalanced-data
excerpt: ''
createdAt: Tue Jul 05 2022 17:20:48 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 21:19:41 GMT+0000 (Coordinated Universal Time)
---

# Class Imbalanced Data

### Overview

Drift is a measure of how different the production distribution is from the baseline distribution on which the model was trained. In practice, the distributions are approximated using histograms and then compared using divergence metrics like Jensen–Shannon divergence or Population Stability Index. Generally, when constructing the histograms, every event contributes equally to the bin counts.

However, for scenarios with large class imbalance the minority class’ contribution to the histograms would be minimal. Hence, any change in production distribution with respect to the minority class would not lead to a significant change in the production histograms. Consequently, even if there is a significant change in distribution with respect to the minority class, the drift value would not change significantly.

To solve this issue, Fiddler monitoring provides a way for events to be weighted based on the class distribution. For such models, when computing the histograms, events belonging to the minority class would be up-weighted whereas those belonging to the majority class would be down-weighted.

### Solutions

Fiddler has implemented two solutions for class imbalance use cases.

#### Workflow 1: User provided global class weights

* The user computes the class distribution on baseline data and then provides the class weights via the Model-Info object.
* Class weights can either be manually entered by the user or computed from their dataset
* To tease out drift in a class-imbalanced fraud use case checkout out the [class-imbalanced-notebook](../../QuickStart\_Notebooks/class-imbalance-monitoring-example.md)

#### Workflow 2: User provided event level weights

User provides event level weights as a metadata column in baseline data and provides them while publishing events:

* Users will add a `_weight` column of type metadata in the model's ModelSpec.
* The baseline dataset requires this `_weight` column. Note that all rows must contain valid float values. We expect the user to enforce this assumption.
* Note that the use of weighting parameters requires the presence of a model output in the baseline dataset.

{% include "../../.gitbook/includes/main-doc-footer.md" %}

