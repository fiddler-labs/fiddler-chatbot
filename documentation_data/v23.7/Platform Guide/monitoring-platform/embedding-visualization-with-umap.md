---
title: "Embedding Visualization with UMAP"
slug: "embedding-visualization-with-umap"
excerpt: ""
hidden: false
createdAt: "Tue Nov 14 2023 04:38:29 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Introduction to embedding visualization

Embedding visualization is a powerful technique used to understand and interpret complex relationships in high-dimensional data. Reducing the dimensionality of custom features into a 2D or 3D space makes it easier to identify patterns, clusters, and outliers.

In Fiddler, high-dimensional data like embeddings and vectors are ingested as a [Custom feature](ref:fdlcustomfeaturetype).

Our goal in this document is to visualize these custom features.

## UMAP Technique for embedding visualization

We utilize the [UMAP](https://umap-learn.readthedocs.io/en/latest/) (Uniform Manifold Approximation and Projection) technique for embedding visualizations. UMAP is a dimension reduction technique that is particularly good at preserving the local structure of the data, making it ideal for visualizing embeddings. We reduce the high-dimensional embeddings to a 3D space.

UMAP is supported for both Text and Image embeddings in [Custom feature](ref:fdlcustomfeaturetype).

> 📘 To create an embedding visualization chart
> 
> Follow the UI Guide on [creating the embedding visualization chart here.](doc:embedding-visualization-chart-creation)
