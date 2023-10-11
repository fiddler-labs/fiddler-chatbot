---
title: "Surrogate Models"
slug: "surrogate-models"
hidden: false
createdAt: "2022-04-19T20:25:57.279Z"
updatedAt: "2022-12-13T23:00:13.880Z"
---
Fiddler’s explainability features require a model on the backend that can generate explanations for you.

A surrogate model is an approximation of your model using gradient boosted trees (LightGBM), trained with a general, predefined set of hyperparameters. It serves as a way for Fiddler to generate approximate explanations without you having to upload your actual model artifact.

***



A surrogate model **will be built automatically** for you when you call  [`add_model_surrogate`](/reference/clientadd_model_surrogate).  
You just need to provide a few pieces of information about how your model operates.

## What you need to specify

- Your model’s task (regression, binary classification, etc.)
- Your model’s target column (ground truth labels)
- Your model’s output column (model predictions)
- Your model’s feature columns