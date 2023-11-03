---
title: "Baselines"
slug: "fiddler-baselines"
excerpt: "A baseline is a set of reference data that is used to compare the performance of our model for monitoring purposes."
hidden: false
createdAt: "2023-01-19T22:47:23.862Z"
updatedAt: "2023-10-19T20:59:24.670Z"
---
A model needs a baseline dataset for comparing its performance and identifying any degradation. A baseline is a set of reference data that is used to compare with our current data. 

The dataset that was used to train the model is often a good starting point for a baseline. For more in-depth analysis, we may want to use a specific time period or a rolling window of production events. 

In Fiddler, **the default baseline for all monitoring metrics is the training dataset **that was associated with the model during registration. Use this default baseline if you do not anticipate any differences between training and production. [New baselines can be added to existing models using the Python client APIs](ref:add_baseline).