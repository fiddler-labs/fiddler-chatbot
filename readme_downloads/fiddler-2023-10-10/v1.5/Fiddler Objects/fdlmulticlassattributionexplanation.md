---
title: "fdl.MulticlassAttributionExplanation"
slug: "fdlmulticlassattributionexplanation"
excerpt: "A collection of AttributionExplanation objects explaining several classes' predictions in a multiclass classification setting"
hidden: false
createdAt: "2023-01-30T21:32:33.900Z"
updatedAt: "2023-01-30T21:43:21.980Z"
---
| Attribute    | Type                                                                                                                  | Description                                                                                        |
| :----------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| classes      | Tuple[str]                                                                                                            | The name of the classes of the given model                                                         |
| explanations | Dict\[str, [fdl.AttributionExplanation](https://dash.readme.com/project/fiddler/v1.5/refs/fdlattributionexplanation)] | A dictionary with key the class name and value the corresponding **AttributionExplanation** object |

```python Example result
MulticlassAttributionExplanation(
  classes=('setosa', 'versicolor', 'virginica'),
  explanations={
    'setosa': AttributionExplanation(
      algorithm='fiddler_shapley_values',
      inputs=['PetalLength', 'PetalWidth','SepalLength', 'SepalWidth'], 
      attributions=[-0.29891895198300644, -0.029399436726888717, 
                    -0.010604933732387386, 0.006137669307288268],
      misc={'background_dataset_size': 120,
            'baseline_prediction': 0.34611477140901986, 
            'explanation_ci': {
              'PetalLength': 0.06498514016006027,
              'PetalWidth': 0.004539074445475087, 
              'SepalLength': 0.0025581061345517075,
              'SepalWidth': 0.002523419484882248
            },
            'explanation_ci_level': 0.95, 
            'model_prediction': 0.013329118274025406
           }
    ),
    'versicolor': AttributionExplanation(
      algorithm='fiddler_shapley_values',
      inputs=['PetalLength', 'PetalWidth', 'SepalLength', 'SepalWidth'],
      attributions=[0.07843931782133946, 
                    -0.08974773072813652,
                    -0.0038978622941771663,
                    -0.023759445425497003], 
      misc={'background_dataset_size': 120,
            'baseline_prediction': 0.32917743999090765,
            'explanation_ci': {
              'PetalLength': 0.033888521062995114,
              'PetalWidth': 0.008470895846885117,
              'SepalLength': 0.004947730104071637, 
              'SepalWidth': 0.005134879385578174
            }, 
            'explanation_ci_level': 0.95,
            'model_prediction': 0.29021171936443646
           }
    ),
    'virginica': AttributionExplanation(
      algorithm='fiddler_shapley_values',
      inputs=['PetalLength', 'PetalWidth', 'SepalLength', 'SepalWidth'], 
      attributions=[0.22047963416166733,
                    0.11914716745502503,
                    0.014502796026564489,
                    0.017621776118208702],
      misc={'background_dataset_size': 120, 
            'baseline_prediction': 0.32470778860007266, 
            'explanation_ci': {
              'PetalLength': 0.03880995606758349,
              'PetalWidth': 0.011875959565576195,
              'SepalLength': 0.007051209191437458,
              'SepalWidth': 0.0031140002491094245
            },
            'explanation_ci_level': 0.95,
            'model_prediction': 0.696459162361538
           }
    )
  }
)
```