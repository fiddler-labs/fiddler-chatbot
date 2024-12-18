---
title: Product Concepts
slug: product-concepts
excerpt: Learn the key concept of the Fiddler product
createdAt: Tue Nov 15 2022 18:06:28 GMT+0000 (Coordinated Universal Time)
updatedAt: Tue Apr 30 2024 20:50:32 GMT+0000 (Coordinated Universal Time)
---

# Product Concepts

### What is ML Observability?

ML observability is the modern practice of gaining comprehensive insights into your AI application's performance throughout its lifecycle. It goes beyond simple indicators of good and bad performance by empowering all model stakeholders to understand why a model behaves in a certain manner and how to enhance its performance.\
ML Observability starts with monitoring and alerting on performance issues, but goes much deeper into guiding model owners towards the underlying root cause of model performance issues.

### What is LLM Observability?

LLM observability is the practice of evaluating, monitoring, analyzing, and improving Generative AI or LLM based application across their lifecycle.\
Fiddler provides real-time monitoring on safety metrics like toxicity, bias, and PII and correctness metrics like hallucinations, faithfulness and relevancy.

### Projects

A project within Fiddler represents your organization's distinct AI applications or use cases. It houses all of the model schemas that have been onboarded to Fiddler for the purpose of AI observability. Projects are typically specific to a given business unit, ML application, or use case.\
They serve as a jumping-off point for Fiddler's model monitoring and explainability features.

Additionally, Fiddler projects serve as the primary access control or authorization mechanism. Different users and teams are given access to view model data within Fiddler at the project level.

### Models

#### Model Schemas

In Fiddler, A model schema is the metadata about a model that is being observed.\
Model schemas are onboarded to Fiddler so that Fiddler understand the data under observation.\
Fiddler does not require the model artifact itself to properly observe the performance of the model; however, [model artifacts](explainability/artifacts-and-surrogates.md#Model-Artifacts) can be uploaded to Fiddler to unlock advanced explainability features.\
Instead, we may just need adequate information about the model's schema, or [the model's specification](../Python\_Client\_3-x/api-methods-30.md#modelspec) in order to monitor the model.

> 📘 **Working with Model Artifacts**
>
> You can [upload your model artifacts](../Client\_Guide/uploading-model-artifacts.md) to Fiddler to unlock high-fidelity explainability for your model. However, it is not required. If you do not wish to upload your artifact but want to explore explainability with Fiddler, we can build a [surrogate model](explainability/artifacts-and-surrogates.md#surrogate-model) on the backend to be used in place of your artifact.

#### Model Versions

Fiddler offers [model versions](monitoring-platform/model-versions.md) to organize related models, streamlining processes such as model retraining or conducting champion vs. challenger analyses. When retraining a model, instead of uploading a new model instance, you can create a new version of the existing model, retaining its core structure while accommodating necessary updates. These updates can include modifications to the schema, such as adding or removing columns, modifying data types, adjusting value ranges, updating the model specifications, and even refining task parameters or Explainable AI (XAI) settings.

### Data

#### Environments

Within Fiddler, each model is associated with two environments; **pre-production** and **production**.\
These environments assign purpose to the data published to Fiddler, allowing it to distinguish between:

```
* Non-time series data (pre-production datasets, eg. training data)
* Time-series data (production data, eg. inference logs)
```

**Pre-Production Environment**

The pre-production environment contains non-time series chunks of data, called **datasets**.\
Datasets are used primarily for point-in-time analysis or as static baselines for comparison against production data.

**Production Environment**

The production environment contains time series data such as production or inference logs which are the _digital exhaust_ emitted by each decision a model makes.\
This time series data provides the inputs and outputs of each model inference/decision and is what Fiddler analyses and compares against the pre-production data to determine if the model's performance is degrading.

#### Datasets

Datasets within Fiddler are static sets of data that have been uploaded to Fiddler for the purpose of establishing _baselines_.\
A common dataset that is uploaded to Fiddler is the model's training data.

#### Baselines

[Baselines](../Client\_Guide/creating-a-baseline-dataset.md) are derived from datasets and used by Fiddler to compare the expected data distributions with the live data published to Fiddler.\
A baseline in Fiddler is a set of reference data used to compare the performance of a model for monitoring purposes. The default baseline for all monitoring metrics in Fiddler is typically the model's training data.\
Additional baselines can be added to existing models that are derived from other datasets, historical inferences, or rolling baselines that refer back to data distributions using historical inferences.

#### Segments

[Segments](monitoring-platform/segments.md) are custom filters applied to your data that enable you to analyze metrics for specific subsets of your data population, for example "People under 50". Segments help you focus on relevant data for more precise insights. Additionally, you can set alerts on these Segments to stay informed about important changes or trends within these defined subsets.

### Metrics

Metrics are computations performed on data received. Fiddler supports the ability to specify custom user-defined metrics [Custom Metrics](monitoring-platform/custom-metrics.md) in addition to five out-of-the-box metric types:

* Data Integrity
* Data Drift
* Performance
* Statistics
* Traffic

### Alerts

[Alerts](monitoring-platform/alerts-platform.md) are user-specified rules which trigger when some condition is met by production data received in Fiddler. Alert rule notifications are sent via email, Slack, custom webhooks, or any combination thereof.

### Enrichments

[Enrichments](llm-monitoring/enrichments-private-preview.md) augment existing columns with additional metrics to monitor different aspects of LLM applications. The new metrics are available for use within the analyze, charting, and alerting functionalities in Fiddler.

### Dashboards and Charts

Fiddler uses customizable [Dashboards](monitoring-platform/dashboards-platform.md) for monitoring and sharing model behavior. A Dashboard is comprised of [Charts](monitoring-platform/monitoring-charts-platform.md) which provide three distinct types of visualizations: monitoring charts, embedding visualizations, and performance analytics. Dashboards consolidate visualizations in one place offering a detailed overview of model performance as well as an entry point for deeper data analysis and root cause identification.

#### Monitoring Charts

Monitoring charts provide a comprehensive view of model performance and support model to model performance analysis. With intuitive displays for data drift, performance metrics, data integrity, traffic patterns, and more, monitoring charts empower users to maintain model accuracy and reliability with ease.

#### Embedding Visualizations

Embedding visualization is a powerful charting tool used to understand and interpret complex relationships in high-dimensional data. Reducing the dimensionality of custom features into a 2D or 3D space makes it easier to identify patterns, clusters, and outliers.

### Jobs

Fiddler [Jobs](https://docs.fiddler.ai/api-integration/api\_guidelines/jobs) are a feature used to track operations such as data publishing or adding model assets such as user artifacts. Jobs are created automatically and can be observed both in the Fiddler UI and polled using the API. Upon successful job completion, the new data or model asset is available for use in the monitoring, alerting, and charting functionalities. If the job fails, users can navigate to the Jobs page and click on "failure" for more details on the job failure. Users can then remediate the cause of error or contact the Fiddler team for more support.

### Bookmarks

Bookmarking enables quick access to projects, models, charts, and dashboards. The comprehensive bookmark page enhances your convenience and efficiency in navigating Fiddler.

{% include "../.gitbook/includes/main-doc-footer.md" %}

