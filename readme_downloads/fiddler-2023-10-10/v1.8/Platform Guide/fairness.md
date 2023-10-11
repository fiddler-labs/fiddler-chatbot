---
title: "Fairness"
slug: "fairness"
hidden: false
createdAt: "2022-04-19T20:24:34.945Z"
updatedAt: "2023-09-27T18:30:00.217Z"
---
> 🚧 Note
> 
> Model Fairness is in preview mode. Contact us for early access.

Fiddler provides powerful visualizations and metrics to detect model bias. Currently, _we support structured (tabular) models for classification tasks_ in both the Fiddler UI and the [API client](ref:about-the-fiddler-client). These visualizations are available for both production and dataset queries.

## Definitions of Fairness

Models are trained on real-world examples to mimic past outcomes on unseen data. The training data could be biased, which means the model will perpetuate the biases in the decisions it makes.

While there is not a universally agreed upon definition of fairness, we define a ‘fair’ ML model as a model that does not favor any group of people based on their characteristics.

Ensuring fairness is key before deploying a model in production. For example, in the US, the government prohibited discrimination in credit and real-estate transactions with fair lending laws like the Equal Credit Opportunity Act (ECOA) and the Fair Housing Act (FHAct).

The Equal Employment Opportunity Commission (EEOC) acknowledges 12 factors of discrimination:[<sup>\[1\]</sup>](#reference) age, disability, equal pay/compensation, genetic information, harassment, national origin, pregnancy, race/color, religion, retaliation, sex, sexual harassment. These are what we call protected attributes.

## Fairness Metrics

Fiddler provides the following fairness metrics:

- Disparate Impact
- Group Benefit
- Equal Opportunity
- Demographic Parity

The choice of the metric is use case-dependent. An important point to make is that it's impossible to optimize all the metrics at the same time. This is something to keep in mind when analyzing fairness metrics.

## Disparate Impact

Disparate impact is a form of **indirect and unintentional discrimination**, in which certain decisions disproportionately affect members of a protected group.

Mathematically, disparate impact compares the pass rate of one group to that of another.

The pass rate is the rate of positive outcomes for a given group. It's defined as follows:

pass rate = passed / (num of ppl in the group)

Disparate impact is calculated by:

`DI = (pass rate of group 1) / (pass rate of group 2)`

Groups 1 and 2 are interchangeable. Therefore, the following formula can be used to calculate disparate impact:

`DI = min{pr_1, pr_2} / max{pr_1, pr_2}.`

The disparate impact value is between 0 and 1. The Four-Fifths rule states that the disparate impact has to be greater than 80%.

For example:

`pass-rate_1 = 0.3, pass-rate_2 = 0.4, DI = 0.3/0.4 = 0.75`

`pass-rate_1 = 0.4, pass-rate_2 = 0.3, DI = 0.3/0.4 = 0.75`

> 📘 Info
> 
> Disparate impact is the only legal metric available. The other metrics are not yet codified in US law.

## Demographic Parity

Demographic parity states that the proportion of each segment of a protected class should receive the positive outcome at equal rates.

Mathematically, demographic parity compares the pass rate of two groups.

The pass rate is the rate of positive outcome for a given group. It is defined as follow:

`pass rate = passed / (num of ppl in the group)`

If the decisions are fair, the pass rates should be the same.

## Group Benefit

Group benefit aims to measure the rate at which a particular event is predicted to occur within a subgroup compared to the rate at which it actually occurs.

Mathematically, group benefit for a given group is defined as follows:

`Group Benefit = (TP+FP) / (TP + FN).`

Group benefit equality compares the group benefit between two groups. If the two groups are treated equally, the group benefit should be the same.

## Equal Opportunity

Equal opportunity means that all people will be treated equally or similarly and not disadvantaged by prejudices or bias.

Mathematically, equal opportunity compares the true positive rate (TPR) between two groups. TPR is the probability that an actual positive will test positive. The true positive rate is defined as follows:

`TPR = TP/(TP+FN)`

If the two groups are treated equally, the TPR should be the same.

## Intersectional Fairness

We believe fairness should be ensured to all subgroups of the population. We extended the classical metrics (which are defined for two classes) to multiple classes. In addition, we allow multiple protected features (e.g. race _and_ gender). By measuring fairness along overlapping dimensions, we introduce the concept of intersectional fairness.

To understand why we decided to go with intersectional fairness, we can take a simple example. In the figure below, we observe that equal numbers of black and white people pass. Similarly, there is an equal number of men and women passing. However, this classification is unfair because we don’t have any black women and white men that passed, and all black men and white women passed. Here, we observe bias within subgroups when we take race and gender as protected attributes.

![](https://files.readme.io/21f6b94-intersectional_fairness.svg "intersectional_fairness.svg")

The EEOC provides examples of past intersectional discrimination/harassment cases.[<sup>\[2\]</sup>](#reference)

## Model Behavior

In addition to the fairness metrics, we provide information about model outcomes and model performance for each subgroup. 

## Dataset Fairness

We also provide a section for dataset fairness, with a mutual information matrix and a label distribution. Note that this is a pre-modeling step.

**Mutual information **gives information about existing dependence in your dataset between the protected attributes and the remaining features. We are displaying Normalized Mutual Information (NMI). This metric is symmetric, and has values between 0 and 1, where 1 means perfect dependency.

For more details about the implementation of the intersectional framework, please refer to this [research paper](https://arxiv.org/pdf/2101.01673.pdf).

## Reference

[^1]\: USEEOC article on [_Discrimination By Type_](https://www.eeoc.gov/discrimination-type)  
[^2]\:  USEEOC article on [_Intersectional Discrimination/Harassment_](https://www.eeoc.gov/initiatives/e-race/significant-eeoc-racecolor-casescovering-private-and-federal-sectors#intersectional)

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/demo?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/4d190fd-fiddler-docs-cta-demo.png\" alt=\"Fiddler Demo\"></a>\n</div>"
}
[/block]