---
title: "fdl.WeightingParams"
slug: "fdlweightingparams"
hidden: false
createdAt: "2022-07-06T13:41:14.177Z"
updatedAt: "2023-05-03T21:59:01.207Z"
---
Holds weighting information for class imbalanced models which can then be passed into a [fdl.ModelInfo](/reference/fdlmodelinfo) object. Please note that the use of weighting params requires the presence of model outputs in the baseline dataset.

| Input Parameters              | Type        | Default | Description                                                                                            |
| :---------------------------- | :---------- | :------ | :----------------------------------------------------------------------------------------------------- |
| class_weight                  | List[float] | None    | List of floats representing weights for each of the classes. The length must equal the no. of classes. |
| weighted_reference_histograms | bool        | True    | Flag indicating if baseline histograms must be weighted or not when calculating drift metrics.         |
| weighted_surrogate_training   | bool        | True    | Flag indicating if weighting scheme should be used when training the surrogate model.                  |

```python Usage
import pandas as pd
import sklearn.utils
import fiddler as fdl

df = pd.read_csv('example_dataset.csv')
computed_weight = sklearn.utils.class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(df[TARGET_COLUMN]),
        y=df[TARGET_COLUMN]
    ).tolist()
weighting_params =  fdl.WeightingParams(class_weight=computed_weight)
dataset_info = fdl.DatasetInfo.from_dataframe(df=df)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    features=[
        'feature_1',
        'feature_2',
        'feature_3'
    ],
    outputs=['output_column'],
    target='target_column',
    weighting_params=weighting_params,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.BINARY_CLASSIFICATION
)
```