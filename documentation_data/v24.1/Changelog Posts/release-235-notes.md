---
title: "Release 23.5 Notes"
slug: "release-235-notes"
type: ""
createdAt: {}
hidden: false
---
This page enumerates the new features and updates in Release 23.5 of the Fiddler platform.

## Release of Fiddler platform version 23.5:

- Support for new `Vector` data type

- Support for new `Frequency` statistics metric

- Support for new `NOT_SET` task type

- New standalone bookmarks page

- Contact your customer success team to get access and documentation to the below:
  - Addition of LLM task
  - Auto embeddings on Text (Prompt, Response, etc) and Image data 
  - Auto enrichments of Toxicity, PII, and Hallucination on LLM task
  - 3D UMAP visualization of high-dimensional embeddings
  - Support for user-defined metrics -> Custom metrics.  Alerts can be set on these custom metrics and plotted in charts and dashboards.

## What's New and Improved:

- **New Vector input type**
  - You can now create custom features from Vector data type
  - The DI violation functionality on vector data types is now available to quickly detect any issues in your data pipelines. As vector and embedding pipelines are complex and prone to errors, we hope this functionality will be of value.
    - Violation of value - Dimension does not match the expected dimension
    - Violation of nullable - Vector length equals zero or received NULL value
    - Violation of type - Value is not of the type of VECTOR or VECTOR contains a non-numerical type
  - Clusters of Text Embeddings have a short summary to understand which of your clusters have the most problematic drift.
  - Events of a particular cluster can be queried in the 'Analyze' tab of the model. This can be used to pinpoint the most problematic prompts/responses in an LLM scenario or images in a CV scenario. This information can be used to improve your models. 
- **New Task Type for Task-less Models**
  - You can now add models without a task by choosing the `NOT_SET` task type when onboarding your model.
  - Note that task-less models have no restrictions on output and target columns, but performance metrics are disabled when a task is not specified.
- **Standalone Bookmarks Page**
  - Access all your bookmarked projects, models, datasets, charts, and dashboards through the Bookmarks page in the navigation bar.
  - Learn more on the [Product Tour](doc:product-tour)

### Client Version

Client version 2.1+ is required for the updates and features mentioned in this release.