---
title: "fdl.AttributionExplanation"
slug: "fdlattributionexplanation"
excerpt: "The results of an attribution explanation run by the Fiddler engine"
hidden: false
createdAt: "2023-01-30T21:44:20.501Z"
updatedAt: "2023-01-31T13:24:34.374Z"
---
| Attribute    | Type           | Description                                                                                                                                                                                 |
| :----------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| algorithm    | str            | The name of the explanation method                                                                                                                                                          |
| inputs       | List[str]      | List of input features                                                                                                                                                                      |
| attributions | List[float]    | List of attributions                                                                                                                                                                        |
| misc         | Optional[dict] | misc will have different details based on the explanation type. For example model prediction, baseline prediction, confidence interval for the explanation, size of background dataset, ... |

```python Example result
AttributionExplanation(
  algorithm='fiddler_shapley_values',
  inputs=['Age', 'Balance', 'CreditScore', 'EstimatedSalary',
          'Gender', 'Geography', 'HasCrCard', 'IsActiveMember',
          'NumOfProducts', 'Tenure'],
  attributions=[0.15160113491423066, 0.031480978762930156,
                0.1831941120167941, -0.0070094998168561155,
                -0.003002888334429402, 0.029338303601551853,
                -0.005787066742637167, -0.0452038935301122,
                0.14073604489745767, -0.012805550127150742],
  misc={'background_dataset_size': 200,
        'baseline_prediction': 0.18426200542835106,
        'explanation_ci': {'Age': 0.012645587534114936,
                           'Balance': 0.009587602106958078, 
                           'CreditScore': 0.009863703930511359, 
                           'EstimatedSalary': 0.0023364778612537935, 
                           'Gender': 0.0016714116997844039, 
                           'Geography': 0.006029320586649526, 
                           'HasCrCard': 0.002847070811544292,
                           'IsActiveMember': 0.008268189814243227,
                           'NumOfProducts': 0.02431611472372665,
                           'Tenure': 0.0022312720267721868}, 
        'explanation_ci_level': 0.95, 
        'model_prediction': 0.6468036810701299
       }
)
```