---
title: "Fraud Detection"
slug: "fraud-detection"
excerpt: "How to monitor and improve your Fraud Detection ML Models using Fiddler's AI Observability platform"
hidden: false
createdAt: "2022-04-19T20:06:54.951Z"
updatedAt: "2023-06-15T00:39:09.945Z"
---
Machine learning-based fraud detection models have been proven to be more effective than humans when it comes to detecting fraud. However, if left unattended, the performance of fraud detection models can degrade over time leading to big losses for the company and dissatisfied customers.  
The **Fiddler AI Observability** platform provides a variety of tools that can be used to monitor, explain, analyze, and improve the performance of your fraud detection model.

## Monitoring

### Drift Detection

- **Class-imbalanced Data** - Fraud use cases suffer from highly imbalanced data. Users can specify model weights on a global or event level to improve drift detection. Please see more information in  [Class-Imbalanced Data](https://docs.fiddler.ai/v1.3/docs/class-imbalanced-data). 

- **Feature Impact** - Tells us the contribution of features to the model's prediction, averaged over the baseline dataset. The contribution is calculated using [random ablation feature impact](https://arxiv.org/pdf/1910.00174.pdf).

- **Feature Drift** - Tells us how much a feature is drifting away from the baseline dataset for the time period of interest. For more information on how drift metrics are calculated, see [Data Drift](/pages/user-guide/data-science-concepts/monitoring/data-drift/).

- **Prediction Drift Impact** - A heuristic calculated by taking the product of Feature Impact and Feature Drift. The higher the score the more this feature contributed to the prediction value drift.

### Performance Metrics

Accuracy might not be a good measure of model performance in the case of fraud detection as most of the cases are non-fraud. Therefore, we use monitor metrics like: 

1. **Recall** - How many of the non-fraudulent cases were actually detected as fraud? A low recall value might lead to an increased number of cases for review even though all the fraud cases were predicted correctly.
2. **False Positive Rate** - Non-Fraud cases labeled as fraud, high FPR rate leads to dissatisfied customers.

### Data Integrity

- **Range Violations** - This metric shows the percentage of data in the selected production data that has violated the range specified in the baseline data through [`DatasetInfo`](https://api.fiddler.ai/#fdl-datasetinfo) API.
- **Missing Value Violations** - This metric shows the percentage of missing data for a feature in the selected production data.
- **Type Violations** - This metric shows the percentage of data in the selected production data that has violated the type specified in the baseline data through the DatasetInfo API.

## Explanability

### Point Overview

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c7249cf-XAI21.gif",
        "XAI21.gif",
        1083
      ],
      "align": "center",
      "caption": "Point Overview"
    }
  ]
}
[/block]

This tab in the Fiddler AI Observability platform gives an overview for the data point selected. The prediction value for the point along with the strongest positive and negative feature attributions. We can choose from the explanation types. In the case of fraud detection, we can choose from SHAP, Fiddler SHAP, Mean-reset feature impact, Permutation Feature Impact.

For the data point chosen, ‘category’ has the highest positive attribution (35.1%), pushing the prediction value towards fraud, and ‘amt’ has the highest negative attribution(-45.8%), pushing the prediction value towards non-fraud.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b4704f6-XAI11.png",
        "XAI11.png",
        1807
      ],
      "align": "center",
      "caption": "Explanation Type"
    }
  ]
}
[/block]

### Feature Attribution

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/9b91f72-XAI22.gif",
        "XAI22.gif",
        1078
      ],
      "align": "center",
      "caption": "Feature Attribution"
    }
  ]
}
[/block]

The Feature Attribution tab gives us information about how much each feature can be attributed to the prediction value based on the Explanation Type chosen. We can also change the value of a particular feature to measure how much the prediction value changes.  
In the example below we can see that on changing the value of feature ‘amt’ from 110 to 10k the prediction value changes from 0.001 to 0.577 (not fraud to fraud).

### Feature Sensitivity

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/3fba7b9-XAI23.gif",
        "XAI23.gif",
        1073
      ],
      "align": "center",
      "caption": "Feature Sensitivity"
    }
  ]
}
[/block]

This tab plots the prediction value against the range of values for different features (top n user selected). We can change the value for any feature and measure the resulting prediction sensitivity plot of all other features against the initial sensitivity plot. 

On reducing the value of the ‘amt’ feature below from 331 to 10, we can see that the final prediction sensitivity plot shows a prediction value \< 0.5 for any value of ‘age’ and ‘unique_merchant_card’. This shows that a lower value for ‘amt’ will result in a prediction value close to 0 (non-fraud)

## Make your Fraud Detections Model better with Fiddler!

Please refer to our [Colab Notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/business-use-cases/fraud-detection/Fraud_Detection_Usecase_Fiddler.ipynb) for a walkthrough on how to get started with using Fiddler for your fraud detection use case and an interactive demo on usability.

### Overview

It is often the case that a model’s performance will degrade over time. We can use the Fiddler AI Observability platform to monitor the model’s performance in production, look at various metrics and also provide explanations to predictions on various data points. In this walkthrough, we will look at a few scenarios common to a fraud model when monitoring for performance. We will show how you would:

1. Get baseline and production data onto the Fiddler Platform
2. Monitor drift for various features
3. Monitor performance metrics associated with fraud detection like recall, false-positive rate
4. Monitor data integrity Issues like range violations
5. Provide point explanations to the mislabelled points
6. Get to the root cause of the issues

### Example - Model Performance Degradation due to Data Integrity Issues

#### Step 1 - Setting up baseline and publishing production events

Please refer to our [`Quick Start Guide`](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/quickstart/Fiddler_Quick_Start_Guide.ipynb) for a step-by-step walkthrough of how to upload baseline and production data to the Fiddler platform.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/fa8ded4-DatasetReady2.gif",
        "DatasetReady2.gif",
        1064
      ],
      "align": "center",
      "caption": "Setting up baseline"
    }
  ]
}
[/block]

#### Step 2 - Monitor Drift

Once the production events are published, we can monitor drift for the model output in the ‘drift’ tab i.e. - pred_is_fraud, which is the probability value of a case being a fraud. Here we can see that the prediction value of pred_is_fraud increased from February 15 to February 16. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/2f4bd83-MonitorDrift2.jpg",
        "MonitorDrift2.jpg",
        1221
      ],
      "align": "center",
      "caption": "Monitor drift"
    }
  ]
}
[/block]

#### Step 3 - Monitor Performance Metrics

Next, To check if the performance has degraded, we can check the performance metrics in the ‘Performance’ tab. Here we will monitor the ‘Recall’ and ‘FPR’ of the model. We can see that the recall has gone down and FPR has gone up in the same period.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/048968e-ModelPerformance1.png",
        "ModelPerformance1.png",
        2624
      ],
      "align": "center",
      "caption": "Performance Chart"
    }
  ]
}
[/block]

#### Step 4 - Data Integrity

The performance drop could be due to a change in the quality of the data. To check that we can go to the ‘Data Integrity’ tab to look for Missing Value Violations, Type Violations, Range Violations, etc. We can see the columns ‘Category’ suffers range violations. Since this is a ‘categorical’ column, there is likely a new value that the model did not encounter during training.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/eef991e-DataIntegrity1.png",
        "DataIntegrity1.png",
        3260
      ],
      "align": "center",
      "caption": "Data Integrity"
    }
  ]
}
[/block]

#### Step 5 - Check the impact of drift

We can go back to the ‘Data Drift’ tab to measure how much the data integrity issue has impacted the prediction. We can select the bin in which the drift increased. The table below shows the Feature Impact, Feature Drift, and Prediction Drift Impact values for the selected bin. We can see that even though the Feature Impact for ‘Category’ value is less than the ‘Amt’ (Amount) value, because of the drift, its Prediction Drift Impact is more. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/328c6b6-DriftImpact1.png",
        "DriftImpact1.png",
        3300
      ],
      "align": "center",
      "caption": "Drift Impact"
    }
  ]
}
[/block]

We will now move on to check the difference between the production and baseline data for this bin. For this, we can click on ‘Export bin and feature to Analyze’. Which will land us on the Analyze tab.

#### Step 6 - Root Cause Analysis in the ‘Analyze’ tab

The analyze tab pre-populated the left side of the tab with the query based on our selection. We can also write custom queries to slice the data for analysis.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/31a6110-RCA2.jpg",
        "RCA2.jpg",
        1226
      ],
      "align": "center",
      "caption": "Analyze Tab"
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a3e4b27-RCA3.png",
        "RCA3.png",
        1660
      ],
      "align": "center",
      "caption": "Analyze Query"
    }
  ]
}
[/block]

On the right-hand side of the tab we can build charts on the tabular data based on the results of our custom query. For this RCA we will build a ‘Feature Distribution’ chart on the ‘Category’ column to check the distinct values and also measure the percentage of each value. We can see there are 15 distinct values along with their percentages.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4996cad-RCA4.png",
        "RCA4.png",
        1634
      ],
      "align": "center",
      "caption": "Feature Distribution - Production"
    }
  ]
}
[/block]

Next, we will compare the Feature Distribution chart in production data vs the baseline data to find out about the data integrity violation. We can modify the query to obtain data for baseline data and produce a ‘Feature Distribution’ chart for the same.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/303c243-RCA5.png",
        "RCA5.png",
        1600
      ],
      "align": "center",
      "caption": "Feature Distribution - Baseline"
    }
  ]
}
[/block]

We can see that the baseline data has just 14 unique values and ‘insurance’ is not present in baseline data. This ‘Category’ value wasn’t present in the training data and crept in production data likely causing performance degradation.  
Next, we can perform a ‘point explanation’ for one such case where the ‘Category’ value was ‘Insurance’ and the prediction was incorrect to measure how much the ‘Category’ column contributed to the prediction by looking at its SHAP value.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c1c1c81-RCA6.png",
        "RCA6.png",
        1650
      ],
      "align": "center",
      "caption": "Mislabelled Data Point"
    }
  ]
}
[/block]

We can click on the bulb sign beside the row to produce a point explanation. If we look at example 11, we can see that the output probability value was 0 (predicted as fraud according to the threshold of 0.5) but the actual value was ‘not fraud’. 

The bulb icon will take us to the ‘Explain’ tab. Here we can see that the ‘category’ value contributed to the model predicting the case as ‘fraud’.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/16d1150-RCA7.png",
        "RCA7.png",
        3330
      ],
      "align": "center",
      "caption": "Point Explanation"
    }
  ]
}
[/block]

#### Step 7 - Actions

We discovered that the prediction drift and performance drop were due to the introduction of a new value in the ‘Category’ column. We can take steps so that we could identify this kind of issue in the future before it can result in business impact.

##### Setting up Alerts

In the ‘Analyze’ tab, we can set up alerts to notify us of as soon as a certain data issue happens. For example, for the case we discussed, we can set up alerts as shown below to alert us when the range violation increases beyond a certain threshold (e.g.-5%).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f7ece9a-Alert2.png",
        "Alert2.png",
        1386
      ],
      "align": "center",
      "caption": "Setting up Alerts"
    }
  ]
}
[/block]

These alerts can further influence the retraining of the ML model, we can retrain the model including the new data so the newly trained model contains the ‘insurance’ category value. This should result in improved performance.

#### Data Insights

Below we can see the confusion matrix for February 16, 2019 (before drift starts). We can observe a good performance with Recall at 100% and 0.1% FP

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/09c82f2-FraudInsights2.png",
        "FraudInsights2.png",
        1574
      ],
      "align": "center",
      "caption": "Slice Evaluation - Feb 17"
    }
  ]
}
[/block]

Below we can see the confusion matrix for February 17, 2019 (after drift starts). We can observe a performance drop with Recall at 50% and 9% FP

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c1c6e39-FraudInsights1.png",
        "FraudInsights1.png",
        1574
      ],
      "align": "center",
      "caption": "Slice Evaluation - Feb 16"
    }
  ]
}
[/block]

### Conclusion

Undetected fraud cases can lead to losses for the company and customers, not to mention damage reputation and relationship with customers. The Fiddler AI Observability platform can be used to identify the pitfalls in your ML model and mitigate them before they have an impact on your business.

In this walkthrough, we investigated one such issue with a fraud detection model where a data integrity issue caused the performance of the ML model to drop. 

Fiddler can be used to keep the health of your fraud detection model up by:  

1. Monitoring the drift of the performance metric
2. Monitoring various performance metrics associated with the model
3. Monitoring data integrity issues that could harm the model performance
4. Investigating the features which have drifted/ compromised and analyzing them to mitigate the issue
5. Performing a root cause analysis to identify the exact cause and fix it
6. Diving into point explanations to identify how much the issue has an impact on a particular data point
7. Setting up alerts to make sure the issue does not happen again

We discovered there was an issue with the ‘Category’ column, wherein a new value was discovered in the production data. This led to the performance drop in the data likely due to the range violation. We suggest two steps to mitigate this issue:

1. Setting up ‘alerts’ to identify similar issues in data integrity
2. Retraining the ML model after including the new data (with the ground truth labels) to teach the model of the new values