---
title: "Analytics"
slug: "analytics"
hidden: false
createdAt: "2022-04-19T20:24:49.443Z"
updatedAt: "2022-09-14T20:03:36.100Z"
---
## Introduction

Fiddler’s industry-first model analytics tool, called Slice and Explain, allows you to perform an exploratory or targeted analysis of model behavior.

1. **_Slice_** — Identify a selection, or slice, of data. Or, you can start with the entire dataset for global analysis.
2. **_Explain_** — Analyze model behavior on that slice using Fiddler’s visual explanations and other data insights.

Slice and Explain is designed to help data scientists, model validators, and analysts drill down into a model and dataset to see global, local, or instance-level explanations for the model’s predictions.

Slice and Explain can help you answer questions like:

- What are the key drivers of my model output in a subsection of the data?
- How are the model inputs correlated to other inputs and to the output?
- Where is my model underperforming?
- How is my model performing across the classes in a protected group?

Access Slice and Explain from the Analyze tab for your model. Slice and Explain currently supports all tabular models.

## Interface

The **Analyze** tab has three parts:

1. **_Slice Query box_** _(top-left)_ — Accepts a SQL query as input, allowing quick access to the slice.
2. **_Data table_** _(bottom-left)_ — Lets you browse instances of data returned by the query.
3. **_Explanations column_** _(right)_ — Allows you to view explanations for the slice and choose from a range of rich visualizations for different data insights.

![](https://files.readme.io/f2daf80-S_E_Landing.png "S_E_Landing.png")



**Workflow**

1. Write a SQL query in the **Slice Query** box and click **Run**.

![](https://files.readme.io/a76a852-S_E_Step_2.png "S_E_Step_2.png")



2. View the data returned by the query in the **Data** table.

![](https://files.readme.io/8771686-S_E_Step_3.png "S_E_Step_3.png")



3. Explore a variety of visualizations using the **Explanations** column on the right.

![](https://files.readme.io/3d16c4e-S_E_Step_4.png "S_E_Step_4.png")



## SQL Queries

![](https://files.readme.io/80c4bfe-S_E_First_Time.png "S_E_First_Time.png")



The **Slice Query** box lets you:

1. Write a SQL query
2. Search and auto-complete field names (i.e. your dataset, the names of your inputs or outputs)
3. Run the SQL query

In the UI, you will see examples for different types of queries:

- Example query to analyze your dataset:

```
select * from "your_dataset_id" limit 100
```



- Example query to analyze your model:

```
select * from "your_dataset_id.your_model_id" limit 100
```



- Example query to analyze production traffic:

```
select * FROM production."your_model_id"
where fiddler_timestamp between '2020-10-20 00:00:00' AND '2020-10-20 12:00:00'limit 100
```



> 🚧 Note
> 
> Only read-only SQL operations are supported. Slices are auto-detected based on your model, dataset, and query. Certain SQL operations like aggregations and joins might not result in a valid slice.

## Data

If the query successfully returns a slice, the results display in the **Data** table below the **Slice Query** box.

![](https://files.readme.io/1d7dd42-S_E_Data.png "S_E_Data.png")



You can view all data rows and their values or download the data as a CSV file to plug it into another system. By clicking on **Explain** (light bulb icon) in any row in the table, you can access explanations for that individual input (more on this in the next section).

## Explanations

The Analyze tab offers a variety of powerful visualizations to quickly let you analyze and explain slices of your dataset.

1. [**Feature Correlation**](#feature-correlation) — View the correlation between model inputs and/or outputs.
2. [**Feature Distribution**](#feature-distribution) — Visualize the distribution of an input or output.
3. [**Feature Impact**](#feature-impact) — Understand the aggregate impact of model inputs to the output.
4. [**Partial Dependence Plot**](#partial-dependence-plot-pdp) — Understand the aggregate impact of a single model input in its output.
5. [**Slice Evaluation**](#slice-evaluation) — View the model metrics for a given slice.
6. [**Dataset Details**](#dataset-details) — Analyze statistical qualities of the dataset.

You can also access the following _point explanation methods_ by clicking on **Explain** (light bulb icon) for a given data point:

1. [**Point Overview**](#point-overview) — Get an overview of the model inputs responsible for a prediction.
2. [**Feature Attribution**](#feature-attribution) — Understand how responsible each model input is for the model output.
3. [**Feature Sensitivity**](#feature-sensitivity) – Understand how changes in the model’s input values will impact the model’s output.

> 📘 Info
> 
> For more information on point explanations, click [here](doc:point-explainability).

## Feature Correlation

The feature correlation visualization plots a single variable against another variable. This plot helps identify any visual clusters that might be useful for further analysis. This visualization supports integer, float, and categorical variables.

![](https://files.readme.io/e36a237-S_E_Correlation.png "S_E_Correlation.png")



## Feature Distribution

The feature distribution visualization is one of the most basic plots, used for viewing how the data is distributed for a particular variable. This plot helps surface any data abnormalities or data insights to help root-cause issues or drive further analysis.

![](https://files.readme.io/26e2658-S_E_Distribution.png "S_E_Distribution.png")



## Feature Impact

This visualization provides the feature impact of the dataset (global explanation) or the selected slice (local explanation), showcasing the overall sensitivity of the model output to each feature (more on this in the [Global Explainability](explainability/global-explainability.md) section). We calculate Feature Impact by randomly intervening on every input using ablations and noting the average absolute change in the prediction.

A high impact suggests that the model’s behavior on a particular slice is sensitive to changes in feature values. Feature impact only provides the absolute impact of the input—not its directionality. Since positive and negative directionality can cancel out, we recommend using a Partial Dependence Plot (PDP) to understand how an input impacts the output in aggregate.

![](https://files.readme.io/09cb939-S_E_FeatureImpact.png "S_E_FeatureImpact.png")



## Partial Dependence Plot (PDP)

Partial dependence plots show the marginal effect of a selected model input on the model output. This plot helps understand whether the relationship between the input and the output is linear, monotonic, or more complex.

![](https://files.readme.io/e1c0f84-PDP.png "PDP.png")



## Slice Evaluation

The slice evaluation visualization gives you key model performance metrics and plots, which can be helpful to identify performance issues or model bias on protected classes. In addition to key metrics, you get a confusion matrix along with precision recall, ROC, and calibration plots. This visualization supports classification, regression, and multi-class models.

![](https://files.readme.io/96aa3d0-Slice_Evaluation.png "Slice_Evaluation.png")



## Dataset Details

This visualization provides statistical details of your dataset to help you understand the data’s distribution and correlations.

Select a target variable to see the dependence between that variable and the others, measured by [mutual information (MI)](https://en.wikipedia.org/wiki/Mutual_information). A low MI is an indicator of low correlation between two variables, and can be used to decide if particular variables should be dropped from the model.

![](https://files.readme.io/69f1a0a-Dataset_details_1.png "Dataset_details_1.png")



![](https://files.readme.io/d3a97a8-Dataset_details_2.png "Dataset_details_2.png")



![](https://files.readme.io/cd0b499-Dataset_details_3.png "Dataset_details_3.png")



## Point Overview

> 📘 Info
> 
> To view this visualization, click on **Explain** (light bulb icon) for any row in the **Data** table.

This visualization provides a human-readable overview of a point explanation.

![](https://files.readme.io/335714a-Explain_Overview.png "Explain_Overview.png")



## Feature Attribution

> 📘 Info
> 
> To view this visualization, click on **Explain** (light bulb icon) for any row in the **Data** table.

Feature attributions can help you understand which model inputs were responsible for arriving at the model output for a particulat prediction.

When you want to check how the model is behaving for one prediction instance, use this visualization first.

More information is available on the [Point Explainability](doc:point-explainability) page.

![](https://files.readme.io/08d409f-Explain_Chart.png "Explain_Chart.png")



## Feature Sensitivity

> 📘 Info
> 
> To view this visualization, click on **Explain** (light bulb icon) for any row in the **Data** table.

This visualization helps you understand how changes in the model’s input values could impact the model’s prediction for this instance.

**_ICE plots_**

On initial load, the visualization shows an Individual Conditional Expectation (ICE) plot for each model input.

![](https://files.readme.io/ac5f0b2-WhatIF_Chart.png "WhatIF_Chart.png")



ICE plots shows how the model prediction is affected by changes in an input for a particular instance. They’re computed by changing the value of an input—while keeping all other inputs constant—and plotting the resulting predictions.

Recall the [partial dependence plots](#partial-dependence-plot-pdp) discussed earlier, which showed the average effect of the feature across the entire slice. In essence, the PDP is the average of all the ICE plots. The PDP can mask interactions at the instance level, which an ICE plot will capture.

You can update any input value to see its impact on the model output, and then view the updated ICE plots for the changed input values.

This is a powerful technique for performing counterfactual analysis of a model prediction. When you plot the updated ICE plots, you’ll see two lines (or sets of bars in the case of categorical inputs).

In the image below, the solid line is the original ICE plot, and the dotted line is the ICE plot using the updated input values. Comparing these two sets of plots can help you understand if the model’s behavior changes as expected with a hypothetical model input.

![](https://files.readme.io/9311aea-WhatIF_After.png "WhatIF_After.png")



## Dashboard

Once visualizations are created, you can pin them to the project dashboard, which can be shared with others.

To pin a chart, click on the thumbtack icon and click **Send**. If the **Update with Query** option is enabled, the pinned chart will update automatically whenever the underlying query is changed on the **Analyze** tab.

![](https://files.readme.io/c4247d1-Pinning_Chart.png "Pinning_Chart.png")



[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_