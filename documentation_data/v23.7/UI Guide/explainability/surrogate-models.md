---
title: "Surrogate Models"
slug: "surrogate-models"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 20:25:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:49:04 GMT+0000 (Coordinated Universal Time)"
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

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
