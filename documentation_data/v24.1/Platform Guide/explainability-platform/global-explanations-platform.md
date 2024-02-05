---
title: "Global Explanations"
slug: "global-explanations-platform"
excerpt: "Platform Guide"
hidden: true
createdAt: "Mon Dec 19 2022 19:29:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:41:52 GMT+0000 (Coordinated Universal Time)"
---
Fiddler provides powerful visualizations to describe the impact of features in your model. Feature impact and importance can be found in either the Explain or Analyze tab.

Global explanations are available in the UI for **structured (tabular)** and **natural language (NLP)** models, for both classification and regression. They are also supported via API using the Fiddler Python package. Global explanations are available for both production and dataset queries.

## Tabular Models

For tabular models, Fiddler’s Global Explanation tool shows the impact/importance of the features in the model.

Two global explanation methods are available:

- **_Feature impact_** — Gives the average absolute change in the model prediction when a feature is randomly ablated (removed).
- **_Feature importance_** — Gives the average change in loss when a feature is randomly ablated.

## Language (NLP) Models

For language models, Fiddler’s Global Explanation performs ablation feature impact on a collection of text samples, determining which words have the most impact on the prediction.

> 📘 Info
> 
> For speed performance, Fiddler uses a random corpus of 200 documents from the dataset. When using the [`run_feature_importance`](https://api.fiddler.ai/#client-run_feature_importance) function from the Fiddler API client, the argument `n_inputs` can be changed to use a bigger corpus of texts.

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
