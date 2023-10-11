---
title: "About Baselines"
slug: "about-baselines"
excerpt: "A baseline is the reference data used to compare model performance for monitoring. Baselines also help us understand our data better."
hidden: true
createdAt: "2022-10-21T23:28:06.367Z"
updatedAt: "2022-11-03T16:14:23.081Z"
---
To compare model performance and root cause performance degradation, our model needs a baseline.

A baseline is a reference data set used to compare our current data with. The training dataset that we used to train the model is usually a good baseline dataset to start with. For deeper analysis we may be interested in a static time period or rolling window on production events.

At Fiddler by default, the baseline for all the monitoring metrics is the training dataset associated with the model at model registration time. It can be updated to different baselines using the python client APIs.