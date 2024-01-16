---
title: "Advanced Explainability"
slug: "advanced-explainability-1"
excerpt: "Support for Complex Use Cases"
hidden: true
createdAt: "Thu Dec 01 2022 19:13:50 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
As a prerequisite for this section, you should be familiar with the [basic model upload](https://dash.readme.com/project/fiddler/v1.3/docs/advanced-explainability) and the components of a Fiddler model package.

# Introduction

Modern machine learning frameworks are extremely flexible and Fiddler's users build powerful models in unique form factors.  "Advanced Explainability" in Fiddler refers to a set of capabilities in the model ingestion workflow that support the following less common, but often more interesting and high-value scenarios:

### Multi-Modal Model Inputs

While some models have simple inputs, like "structured" vectors of numerical and categorical features, or single text strings; others expect a combination of different data types and shapes. 

Examples Include:

- models evaluating an image based on a text prompt
- credit underwriting models that combine dense tabular features with sequences encoding recent bank transactions or credit history events to make a lending decision

### Unstructured Input Types

Data inputs to models may not conform to simple data types and need to be serialized and deserialized by user code without the expectation that the Fiddler platform understands what that data represents.

Examples Include:

- sparse representations of vectors produced by term-frequency preprocessing
- nested and arbitrary length lists representing event sequences
- encoded binary images or waveform data. 

### Large Feature Counts

Models with large numbers of inputs can make precise aproximations of Shaply values computationally prohibitive.  Additionally, representing these inputs in a tabular format may exceed column count limitations or produce unnecessarily large workloads computing sketches of many features whose individual characteristics are not useful.

Examples Include:

- computer vsision models where model inputs are pixels
- language models with large token counts
- unstructured models with arbitrary-length sequential inptus
- inputs more efficiently represented as sparse vectors (e.g. TFIDF vectors; especially when n-grams with n>1 is included).

### Custom Explanations

While Fiddler implements general-purpose explainers, there are some situations where a model developer might prefer to instrument their model with their own explanation algorighm and surface that  explation in the FIddler UI and through Fiddler's APIs:

Examples include:

- A model developer instruments a PyTorch deep-learning model with the [Captum](https://captum.ai/) library during development and chooses to make those explanations available to other stakeholders
- It may be preferable to use a architecture-specific explainer for performance reasons – like using TreeSHAP for a decision tree or GBM.
- Running arbitrary explainability algorithms might be contractually or practically off-limits for a vendor model, but some explainability mechanism is provided by the vendor.

### Explanation Display Customization

# Advanced Explanation Types

# "GEM" – Generalized Explanation Markup

- Helpers + gem.py
- Custom Example: Ice cream sales
- IG Example: Hybrid Churn
