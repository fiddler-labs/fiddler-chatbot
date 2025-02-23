---
title: "Data Integrity"
slug: "data-integrity"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 20:25:27 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Jan 18 2024 00:19:21 GMT+0000 (Coordinated Universal Time)"
---
ML models are increasingly driven by complex feature pipelines and automated workflows that involve dynamic data. Data is transformed from source to model input, which can result in data inconsistencies and errors.

There are three types of violations that can occur at model inference: **missing feature values**, **type mismatches** (e.g. sending a float input for a categorical feature type) or **range mismatches** (e.g. sending an unknown US State for a State categorical feature).

You can track all these violations in the Data Integrity tab. 

## What is being tracked?

![](https://files.readme.io/dd0af16-image.png)

The time series above tracks the violations of data integrity constraints set up for this model.

- **_Missing value violations_** — The percentage of missing value violations over all features for a given period of time.
- **_Type violations_** — The percentage of data type mismatch violations over all features for a given period of time.
- **_Range violations_** — The percentage of range mismatch violations over all features for a given period of time.
- **_All violating events_** — An aggregation of all the data integrity violations above for a given period of time.

## Why is it being tracked?

- Data integrity issues can cause incorrect data to flow into the model, which can lead to poor model performance and have a negative impact on the business or end-user experience. 

## How does it work?

It can be tedious to set up constraints for individual features when they number in the tens or hundreds. To avoid this, you can provide Fiddler with a baseline dataset that's representative of the data you expect your model to infer on in production. This should be sampled from your model's training set, and can be [uploaded to Fiddler using the Python API client](ref:clientupload_dataset).

Fiddler will automatically generate constraints based on the distribution of data in this dataset.

- **Missing values**: If a feature has no missing values, then the data integrity violation will be set up to trigger when any missing values are seen. Similarly, if the feature has 50% of its values missing, then the data integrity violation will be set up to trigger when more than 50% of the values encountered are missing in a specified time range.
- **Type mismatch**: A data integrity violation will be triggered when the type of a feature value differs from what was specified for that feature in the baseline dataset.
- **Range mismatch**: For categorical features, a data integrity violation will be triggered when it sees any value other than the ones specified in the baseline. Similarly, for continuous variables, the violation will be triggered if the values are outside the range specified in the baseline.

## What steps should I take with this information?

- The visualization above informs us of the feature-wise breakdown of the violations. The raw counts of the violations are shown in parentheses.
- If there is a spike in violations, or an unexpected violation occurs (such as missing values for a feature that doesn’t accept a missing value), then a deeper examination of the feature pipeline may be required.
- You can also drill down deeper into the data by examining it in the **Analyze** tab. We can use SQL to slice and dice the data, and try to find the root cause of the issues.

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
