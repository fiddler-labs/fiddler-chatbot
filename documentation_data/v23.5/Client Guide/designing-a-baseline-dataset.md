---
title: "Designing a Baseline Dataset"
slug: "designing-a-baseline-dataset"
hidden: false
createdAt: "2022-05-23T16:30:17.415Z"
updatedAt: "2023-10-19T20:59:24.644Z"
---
In order for Fiddler to monitor drift or data integrity issues in incoming production data, it needs something to compare this data to.

A baseline dataset is a **representative sample** of the kind of data you expect to see in production. It represents the ideal form of data that your model works best on.

*For this reason,* ***it should be sampled from your model’s training set.***

***

**A few things to keep in mind when designing a baseline dataset:**

* It’s important to include **enough data** to ensure you have a representative sample of the training set.
* You may want to consider **including extreme values (min/max)** of each column in your training set so you can properly monitor range violations in production data. However, if you choose not to, you can manually specify these ranges before upload (see [Customizing Your Dataset Schema])(doc:customizing-your-dataset-schema).