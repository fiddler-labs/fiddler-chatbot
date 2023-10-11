---
title: "Surrogate Models - Client Guide"
slug: "surrogate-models-client-guide"
hidden: false
createdAt: "2022-12-13T22:22:39.933Z"
updatedAt: "2022-12-13T22:22:39.933Z"
---
Fiddler’s explainability features require a model on the backend that can generate explanations for you.

> 📘 If you don't want to or cannot upload your actual model file, Surrogate Models serve as a way for Fiddler to generate approximate explanations.

A surrogate model **will be built automatically** for you when you call  [`add_model_surrogate`](/reference/clientadd_model_surrogate).  
You just need to provide a few pieces of information about how your model operates.

## What you need to specify

- Your model’s task (regression, binary classification, etc.)
- Your model’s target column (ground truth labels)
- Your model’s output column (model predictions)
- Your model’s feature columns