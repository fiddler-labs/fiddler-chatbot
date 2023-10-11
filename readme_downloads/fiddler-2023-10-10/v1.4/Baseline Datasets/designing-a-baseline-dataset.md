---
title: "Designing a Baseline Dataset"
slug: "designing-a-baseline-dataset"
hidden: false
createdAt: "2022-05-23T16:30:17.415Z"
updatedAt: "2022-11-10T18:04:33.761Z"
---
In order for Fiddler to monitor drift or data integrity issues in incoming production data, it needs something to compare this data to.

A baseline dataset is a **representative sample** of the kind of data you expect to see in production. It represents the ideal form of data that your model works best on.

*For this reason,* ***it should be sampled from your model’s training set.***

***

**A few things to keep in mind when designing a baseline dataset:**

* It’s important to include **enough data** to ensure you have a representative sample of the training set.
* If you are interested in prediction drift and don't provide your own model, you will need to include the model's prediction(s) for each instance in the baseline dataset.
* When you provide your own model and don't provide predictions in the baseline dataset, Fiddler will compute and store all predictions.
* You may want to consider **including extreme values (min/max)** of each column in your training set so you can properly monitor range violations in production data. However, if you choose not to, you can manually specify these ranges before uploading see [Customizing Your Dataset Schema](doc:customizing-your-dataset-schema).