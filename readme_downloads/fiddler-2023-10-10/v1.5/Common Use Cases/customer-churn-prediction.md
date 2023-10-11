---
title: "Customer Churn Prediction"
slug: "customer-churn-prediction"
hidden: false
createdAt: "2022-05-17T19:12:12.382Z"
updatedAt: "2022-09-07T14:05:19.918Z"
---
Churn prediction is a common use case in the machine learning domain. Churn means “leaving the company”. It is very critical for a business to have an idea about why and when customers are likely to churn. Having a robust and accurate churn prediction model helps businesses to take action to prevent customers from leaving the company. Machine learning models have proved to be effective in detecting churn. However, if left unattended, the performance of churn models can degrade over time leading to losing customers. 

The Fiddler MPM platform provides a variety of tools which can be used to monitor, explain, analyze, and improve the performance of your machine learning based churn model.

In this article we will go over a churn example and how we can mitigate a performance degradation in a churn machine learning model.

Refer to the [colab notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/business-use-cases/churn-usecase/Fiddler_Churn_Use_Case.ipynb) to learn how to -

1. Register model on the Fiddler platform
2. Publish events on the Fiddler platform
3. Use the Fiddler API to run explanations

### Example - Model Performance Degradation due to Data Integrity Issues

#### Step 1 - Setting up baseline and publishing production events

Please refer to our [Getting Started guide](https://docs.fiddler.ai/pages/getting-started/product-tour/) for a step-by-step walkthrough of how to upload baseline and production data to the Fiddler platform.

#### Step 2 - Monitor Drift

When we check the monitoring dashboard, we notice a drop in predicted churn value and a rise in predicted churn drift value. Our next step is to check if this has resulted in a drop in performance.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/2f20fd2-Churn-image1-monitor-drift.png",
        "Churn-image1-monitor-drift.png",
        1999
      ],
      "caption": "Monitor Drift"
    }
  ]
}
[/block]

#### Step 3 - Monitor Performance Metrics

We use **precision, recall, and F1-score** as accuracy metrics for this example. We’re choosing these metrics as they are suited for classification problems and help us in identifying the quantity of false positives and false negatives. We notice that although the precision has remained constant, there is a drop in the F1-score and recall, which means that there are a few customers who are likely to churn but the model is not able to predict their outcome correctly. 

There could be a number of reason for drop in performance, some of them are-

1. Cases of extreme events (Outliers)
2. Data distribution changes
3. Model/Concept drift
4. Pipeline health issues

While **Pipeline health issues** could be due to a component in the Data pipeline failing, the first 3 could be due to changes in data. In order to check that we can go to the **Data Integrity** tab to first check if the incoming data is consistent with the baseline data.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/bb02793-churn-image2-monitor-performance-metrics.png",
        "churn-image2-monitor-performance-metrics.png",
        1999
      ],
      "caption": "Monitor Performance Metrics"
    }
  ]
}
[/block]

#### Step 4 - Data Integrity

Our next step would be to check if this could be due to any data integrity issues. On navigating to the **Data Integrity** tab under the **Monitor** tab, we see that there has been a range violation. On selecting the bins which have the range violations, we notice it is due to the field `numofproducts`. 

It is advised to check all the fields which cause data integrity violations. Since we see a range violation, we can check how much the data has drifted.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/5819966-churn-image3-data-integrity.png",
        "churn-image3-data-integrity.png",
        1999
      ],
      "sizing": "smart",
      "caption": "Data Integrity"
    }
  ]
}
[/block]

#### Step 5 - Check the impact of drift on ‘numofproducts’ features

Our next step would be to go back to the **Data Drift** tab to measure the amount of drift in the field `numofproducts`. The drift is calculated using **Jensen Shannon Divergence**, which compares the distributions of the two data sets being compared. 

We can select the bin where we see an increase in average value as well as drift. We see a significant increase in the `numofproducts` average value and drift. We can also see there is a difference in the distribution of the baseline and production data which leads to a drift. 

Next step could be to find out if the change in distribution was only for a subsection of data or was it due to other factors like time (seasonality etc.), fault in data reporting (sensor data), change in the unit in which the metric is reported etc.  
Seasonality could be observed by plotting the data across time (provided we have enough data), a fault in data reporting would mean missing values, and change in unit of data would mean change in values for all subsections of data.

In order to investigate if the change was only for a subsection of data, we will go to the **Analyze** tab. We can do this by clicking **Export bin and feature to Analyze**. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1d1a5b3-churn-image4-impact-of-drift.png",
        "churn-image4-impact-of-drift.png",
        1999
      ],
      "caption": "Impact of Drift"
    }
  ]
}
[/block]

#### Step 6 - Root Cause Analysis in the ‘Analyze’ tab

In the analyze tab, we will have an auto-generated SQL query based on our selection in the **Monitor** tab, we can also write custom SQL queries to investigate the data. 

We check the distribution of the field `numofproducts` for our selection. We can do this by selecting **Chart Type - Feature Distribution** on the RHS of the tab. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/9b1f7d1-Churn-image5-analyze-rca-1.png",
        "Churn-image5-analyze-rca-1.png",
        1999
      ],
      "caption": "Root Cause Analysis - 1"
    }
  ]
}
[/block]

We further check the performance of the model for our selection by selecting the **Chart Type - Slice Evaluation**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/350aef8-Churn-image6-analyze-rca-2.png",
        "Churn-image6-analyze-rca-2.png",
        1578
      ],
      "caption": "Root Cause Analysis - 2"
    }
  ]
}
[/block]

In order to check if the change in the range violation has occurred for a subsection of data, we can plot it against the categorical variable. In our case, we can check distribution of `numofproducts` against `age` and `geography`. For this we can plot a feature correlation plot for two features by querying data and selecting **Chart type - Feature Correlation**.

On plotting the feature correlation plot of `gender` vs `numofprodcuts`, we observe the distribution to be similar.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4f73274-churn-image6-analyze-rca-2-1.png",
        "churn-image6-analyze-rca-2-1.png",
        512
      ],
      "caption": "Root Cause Analysis - 3"
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/aff3dbf-churn-image6-analyze-rca-2-2.png",
        "churn-image6-analyze-rca-2-2.png",
        464
      ],
      "caption": "Root Cause Analysis - 4"
    }
  ]
}
[/block]

For the sake of this example, let’s say that state of Hawaii (which is a value in the `geography` field in the data) announced that it has eased restrictions on number of loans, since loans is one of products, our hypothesis is the `numofproducts` would be higher for the state. To test this we will check the feature correlation between `geography` and `numofproducts`.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e1c31a1-churn-image6-analyze-rca-2-3.png",
        "churn-image6-analyze-rca-2-3.png",
        463
      ],
      "caption": "Root Cause Analysis - 5"
    }
  ]
}
[/block]

We do see higher values for the state of Hawaii as compared to other states. We can further check distribution for the field `numofproducts` just for the state of Hawaii. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6664850-churn-image7--analyze-rca-3.png",
        "churn-image7--analyze-rca-3.png",
        1999
      ],
      "caption": "Root Cause Analysis - 6"
    }
  ]
}
[/block]

On checking performance for the subset of Hawaii, we see a huge performance drop.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/974b118-churn-image8--analyze-rca-4.png",
        "churn-image8--analyze-rca-4.png",
        1624
      ],
      "caption": "Root Cause Analysis - 7"
    }
  ]
}
[/block]

On the contrary, we see a good performance for the subset of data without the ‘Hawaii’. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ee29b35-churn-image6-analyze-rca-4-1-1.png",
        "churn-image6-analyze-rca-4-1-1.png",
        924
      ],
      "caption": "Root Cause Analysis - 8"
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/fc54636-churn-image9--analyze-rca-5.png",
        "churn-image9--analyze-rca-5.png",
        1606
      ],
      "caption": "Root Cause Analysis - 9"
    }
  ]
}
[/block]

#### Step 7 - Measuring the impact of the ‘numofproducts’ feature

In order to measure the impact of features - `numofproducts`, we can navigate back to the **Monitor** tab. We can see that the prediction drift impact is highest for `numofproducts` due to its high drift value, which means it is contributing the most to the prediction drift.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e78d838-churn-image10-impact1.png",
        "churn-image10-impact1.png",
        1999
      ],
      "caption": "Feature Impact - 1"
    }
  ]
}
[/block]

We can further measure the attribution of the feature - `numofproducts` for a single data point. We can select a data point which was incorrectly predicted to not churn (false negative). We can check point explanations for a point from the **Analyze** by running a query or from the **Explain** tab. Below we check point explanations for a data point form analyze tab by clicking the **bulb** symbol from the query results. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/026d5cb-churn-image11-impact2.png",
        "churn-image11-impact2.png",
        1654
      ],
      "caption": "Feature Impact - 2"
    }
  ]
}
[/block]

We see that the feature - `numofproducts` attributes significantly towards the data point being predicted not to churn.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/65fd05d-churn-image12-impact3.png",
        "churn-image12-impact3.png",
        1999
      ],
      "caption": "Feature Impact - 3"
    }
  ]
}
[/block]

We have seen that the performance of the churn model drops due to range violation in one of the features. We can improve the performance by retraining the model with new data but before that we must perform mitigation actions which would help us in preemptively detecting the model performance degradation and inform our retraining frequency.

#### Step 8 - Mitigation Actions

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6190a63-churn-image13-mitigate.png",
        "churn-image13-mitigate.png",
        1618
      ],
      "caption": "Add to dashboard"
    }
  ]
}
[/block]

1. **Add to dashboard**  
   We can add the chart generated to the dashboard by clicking on **Pin this chart** on the RHS of the Analyze tab. This would help us in monitoring importance aspects of the model.

2. **Add alerts**  
   We can alert users to make sure we are notified the next time there is a performance degradation. For instance, in this example, there was a performance degradation due to range data integrity violation. To mitigate this, we can set up an alert which would notify us in case the percentage range violation exceeds a certain threshold (10% would be a good number in our case). We can also set up alerts on drift values for prediction etc. Check out this [link](https://docs.fiddler.ai/pages/user-guide/data-science-concepts/monitoring/alerts/) to learn how to set up alerts on Fiddler platform.