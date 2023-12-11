---
title: "Global Explainability"
slug: "global-explainability-platform"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Fri Nov 18 2022 22:57:28 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
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
> For speed performance, Fiddler uses a random corpus of 200 documents from the dataset. When using the [`get_feature_importance`](ref:clientget_feature_importance) function from the Fiddler API client, the argument `num_refs` can be changed to use a bigger corpus of texts.

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/trial?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/af83f1a-fiddler-docs-cta-trial.png\" alt=\"Fiddler Free Trial\"></a>\n</div>"
}
[/block]