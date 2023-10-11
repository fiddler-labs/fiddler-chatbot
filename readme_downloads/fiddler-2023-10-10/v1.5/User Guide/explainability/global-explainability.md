---
title: "Global Explainability"
slug: "global-explainability"
hidden: false
createdAt: "2022-04-19T20:25:47.634Z"
updatedAt: "2022-09-14T20:03:24.048Z"
---
Fiddler provides powerful visualizations to describe the impact of features in your model. Feature impact and importance can be found in either the Explain or Analyze tab.

Global explanations are available in the UI for **structured (tabular)** and **natural language (NLP)** models, for both classification and regression. They are also supported via API using the Fiddler Python package. Global explanations are available for both production and dataset queries.

## Tabular Models

For tabular models, Fiddler’s Global Explanation tool shows the impact/importance of the features in the model.

Two global explanation methods are available:

- **_Feature impact_** — Gives the average absolute change in the model prediction when a feature is randomly ablated (removed).
- **_Feature importance_** — Gives the average change in loss when a feature is randomly ablated.

Feature impact and importance are displayed as percentages of all attributions.

The following is an example of feature impact for a model predicting the likelihood of successful loan repayment:

![](https://files.readme.io/2548d18-Global-Expln-Tabular.png "Global-Expln-Tabular.png")



## Language (NLP) Models

For language models, Fiddler’s Global Explanation performs ablation feature impact on a collection of text samples, determining which words have the most impact on the prediction.

> 📘 Info
> 
> For speed performance, Fiddler uses a random corpus of 200 documents from the dataset. When using the [`run_feature_importance`](https://api.fiddler.ai/#client-run_feature_importance) function from the Fiddler API client, the argument `n_inputs` can be changed to use a bigger corpus of texts.

Two types of visualization are available:

- **_Word cloud_** — Displays a word cloud of top 150 words from a collection of text for this model. Fiddler provides three options:
  - **Average change**: The average impact of a word in the corpus of documents. This takes into account the impact's directionality.
  - **Average absolute feature impact**:  The average absolute impact of a word in the corpus of documents. This only takes the absolute impact of the word into account, and not its directionality.
  - **Occurrences**: The number of times a word is present in the corpus of text.

- **_Bar chart_** — Displays the impact for the **Top N** words. By default, only words with at least 15 occurrences are displayed. This number can be modified in the UI and will be reflected in real time in the bar chart. Fiddler provides two options:
  - **Average change**: The average impact of a word in the corpus of documents. This takes into account the impact's directionality. Since positive and negative directionalities can cancel out, Fiddler provides a histogram of the individual impact, which can be found by clicking on the word.
  - **Average absolute feature impact**: The average absolute impact of a word in the corpus of documents. This only takes the absolute impact of the word into account, and not its directionality.

The following image shows an example of word impact for a sentiment analysis model:

![](https://files.readme.io/b4e104b-Global-Expln-NLP.png "Global-Expln-NLP.png")



[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_