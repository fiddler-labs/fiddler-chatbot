---
title: "Model Task Types"
slug: "task-types"
hidden: false
createdAt: "2022-11-15T18:06:58.284Z"
updatedAt: "2023-02-10T16:29:14.851Z"
---
Fiddler currently supports four model tasks. These include:

- Binary Classification
- Multi-class Classification
- Regression
- Ranking

**Binary classification** is the task of classifying the elements of an outcome set into two groups (each called class) on the basis of a classification rule. Typical binary classification problems include:

- Determining whether a customer will churn or not. Here the outcome set has two outcomes: The customer will churn or the customer will not. Further, the outcome can only belong to either of the two classes.
- Determining whether a patient has a disease or not. Here the outcome set has two outcomes: the patient has the disease or does not.

**Multiclass classification** is the task of classifying the elements of an outcome set into three or more groups (each called class) on the basis of a classification rule. Typical multiclass classification problems include:

- Determining whether an image is a cat, a dog, or a bird. Here the outcome set has more than two outcomes. Further, the image can only be determined to be one of the three outcomes and it's thus a multiclass classification problem.

**Regression** is the task of predicting a continuous numeric quantity. Typical regression problems include:

- Determining the average home price based on a given set of housing related features such as it's square footage, number of beds and bath, it's location etc.
- Determining the income of an individual based on features such as their age, work location, their job sector etc.

**Ranking** is the task of constructing a rank ordered list of items given a particular query that seeks some information. Typical ranking problems include:

- Ranking documents in information retrieval systems.
- Ranking relevancy of advertisements based on user search queries.