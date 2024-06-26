---
title: "Model Task Types"
slug: "task-types"
excerpt: ""
hidden: false
createdAt: "Tue Nov 15 2022 18:06:58 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:42:57 GMT+0000 (Coordinated Universal Time)"
---
From 23.5 and onwards, Fiddler supports **six** model tasks. These include:

- Binary Classification
- Multi-class Classification
- Regression
- Ranking
- LLM
- Not set

**Binary classification** is the task of classifying the elements of an outcome set into two groups (each called class) on the basis of a classification rule. 

[Onboarding](doc:onboarding-a-model) a Binary classification task in Fiddler requires the following:

- A single output column of type float (range 0-1) which represents the soft output of the model. This column has to be defined.
- A single target column that represents the true outcome. This column has to be defined.
- A list of input features has to be defined.

Typical binary classification problems include:

- Determining whether a customer will churn or not. Here the outcome set has two outcomes: The customer will churn or the customer will not. Further, the outcome can only belong to either of the two classes.
- Determining whether a patient has a disease or not. Here the outcome set has two outcomes: the patient has the disease or does not.

**Multiclass classification** is the task of classifying the elements of an outcome set into three or more groups (each called class) on the basis of a classification rule. 

[Onboarding](doc:onboarding-a-model) a Multiclass classification task in Fiddler requires the following:

- Multiple output columns (one per class) of type float (range 0-1) which represent the soft outputs of the model. Those columns have to be defined.
- A single target column that represents the true outcome. This column has to be defined.
- A list of input features has to be defined.

Typical multiclass classification problems include:

- Determining whether an image is a cat, a dog, or a bird. Here the outcome set has more than two outcomes. Further, the image can only be determined to be one of the three outcomes and it's thus a multiclass classification problem.

**Regression** is the task of predicting a continuous numeric quantity. 

[Onboarding](doc:onboarding-a-model) a Regression task in Fiddler requires the following:

- A single numeric output column that represents the output of the model. This column has to be defined.
- A single numeric target column that represents the true outcome. This column has to be defined.
- A list of input features has to be defined.

Typical regression problems include:

- Determining the average home price based on a given set of housing-related features such as its square footage, number of beds and baths, its location, etc.
- Determining the income of an individual based on features such as age, work location, job sector, etc.

**Ranking** is the task of constructing a rank-ordered list of items given a particular query that seeks some information. 

[Onboarding](doc:onboarding-a-model) a Ranking task in Fiddler requires the following:

- A single numeric output column that represents the output of the model. This column has to be defined.
- A single target column that represents the true outcome. This column has to be defined.
- A list of input features has to be defined.

Typical ranking problems include:

- Ranking documents in information retrieval systems.
- Ranking relevancy of advertisements based on user search queries.

**LLM** is the task dedicated for Large Language Models, a type of transformer model. It represents a deep learning model that can process human languages. 

[Onboarding](doc:onboarding-a-model) an LLM task in Fiddler doesn't require any specific format with regards to the targets/outputs/inputs definition. Those can be defined or not, with any type and no minimum or maximum column has to be defined. However, in that setting, Fiddler doesn't offer XAI functionalities or performance metrics.

Typical LLM problems include:

- Chatbots and Virtual assistants that can answer questions.
- Content creation like articles, blog posts, etc.

**Not set** is the task to choose if a use-case is not covered by the previous tasks or the use-case doesn't need performance metrics. In this setting, the user doesn't have to specify the required data as discussed above to onboard their model.

[Onboarding](doc:onboarding-a-model) a `NOT_SET` task in Fiddler doesn't require any specific format with regards to the targets/outputs/inputs definition Those can be defined or not, with any type and no minimum or maximum column has to be defined. However, in that setting, Fiddler doesn't offer XAI functionalities or performance metrics.

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
