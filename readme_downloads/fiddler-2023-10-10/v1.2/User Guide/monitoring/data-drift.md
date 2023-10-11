---
title: "Data Drift"
slug: "data-drift"
hidden: false
createdAt: "2022-04-19T20:25:14.478Z"
updatedAt: "2022-06-24T19:54:36.779Z"
---
Model performance can be poor if models trained on a specific dataset encounter different data in production. This is called data drift. In the **Monitor** tab for your model, Fiddler gives you a visual way to explore data drift and identify what data is drifting, when it’s drifting, and how it’s drifting. This is the first step in identifying possible model performance issues.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0d04342-Monitoring-DataDrift.png",
        "Monitoring-DataDrift.png",
        3390,
        1998,
        "#fafafb"
      ]
    }
  ]
}
[/block]
You can change the time range using the controls in the upper-right:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d5809f8-Monitoring-TimeRange.png",
        "Monitoring-TimeRange.png",
        1770,
        126,
        "#f4f7fc"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "What is being tracked?"
}
[/block]
* ***Drift Metrics***
  * **Jensen–Shannon distance (JSD)**
    * A distance metric calculated between the distribution of a field in the baseline dataset and that same distribution for the time period of interest.
    * For more information on JSD, click [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jensenshannon.html).
  * **Population Stability Index (PSI)**
    * A drift metric based on the multinomial classification of a variable into bins or categories. The differences in each bin between the baseline and the time period of interest are then utilized to calculate it as follows:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0baeb90-psi_calculation.png",
        "psi_calculation.png",
        1502,
        156,
        "#f0f0f0"
      ]
    }
  ]
}
[/block]
Here, `B` is the total number of bins, `ActualProp(b)` is the proportion of counts within bin `b` from the target distribution, and `ExpectedProp(b)` is the proportion of counts within bin `b` from the reference distribution. Thus, PSI is a number that ranges from zero to infinity and has a value of zero when the two distributions exactly match.
[block:callout]
{
  "type": "warning",
  "title": "Note",
  "body": "Since there is a possibility that a particular bin may be empty, PSI can shoot to infinity. To avoid this, PSI calculation in Fiddler is done such that each bin count is incremented with a base_count=1. Thus, there might be a slight difference in the PSI values obtained from manual calculations."
}
[/block]
* ***Average Values*** – The mean of a field (feature or prediction) over time. This can be thought of as an intuitive drift score.
* ***Drift Analytics*** – You can drill down into the features responsible for the prediction drift using the table at the bottom.
  * ***Feature Impact***: The contribution of a feature to the model’s predictions, averaged over the baseline dataset. The contribution is calculated using random ablation feature impact.
  * ***Feature Drift***: Drift of the feature, calculated using the drift metric of choice.
  * ***Prediction Drift Impact***: A heuristic calculated using the product of the feature impact and the feature drift. The higher the score, the more this feature is likely to have contributed to the prediction drift.

In the Drift Analytics table, you can select a feature to see the feature distribution for both the time period under consideration and the baseline dataset. If it’s a numerical feature, you will also see a time series of the average feature value over time.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/63a452e-Monitor_DriftAnaly.png",
        "Monitor_DriftAnaly.png",
        3158,
        1690,
        "#fafafc"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Why is it being tracked?"
}
[/block]
* Data drift is a great proxy metric for **performance decline**, especially if there is delay in getting labels for production events. (e.g. In a credit lending use case, an actual default may happen after months or years.)
* Monitoring data drift also helps you stay informed about **distributional shifts in the data for features of interest**, which could have business implications even if there is no decline in model performance.
[block:api-header]
{
  "title": "What do I do next with this information?"
}
[/block]
* High drift can occur as a result of *data integrity issues* (bugs in the data pipeline), or as a result of *an actual change in the distribution of data* due to external factors (e.g. a dip in income due to COVID). The former is more in our control to solve directly. The latter may not be solvable directly, but can serve as an indicator that further investigation (and possible retraining) may be needed.
* You can drill down deeper into the data by examining it in the Analyze tab. 

The image below shows how to open the Analyze view for a specific feature and time range identified in the Data Drift page.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8a699e1-Monitor_DDrift_Analyze.png",
        "Monitor_DDrift_Analyze.png",
        3128,
        1646,
        "#fafafb"
      ]
    }
  ]
}
[/block]
This will bring you to the Analyze tab, where you can then use SQL to slice and dice the data.  You can then apply visualizations upon these slices to analyze the model’s behavior.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/25eca03-Monitor_Analyze.png",
        "Monitor_Analyze.png",
        3166,
        1662,
        "#fbfcfc"
      ]
    }
  ]
}
[/block]
**Reference**

* See our article on [_The Rise of MLOps Monitoring_](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*