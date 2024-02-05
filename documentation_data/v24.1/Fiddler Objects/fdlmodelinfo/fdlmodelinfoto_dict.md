---
title: "fdl.ModelInfo.to_dict"
slug: "fdlmodelinfoto_dict"
excerpt: "Converts a Model object to a dictionary."
hidden: false
createdAt: "Tue May 24 2022 15:54:52 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Return Type | Description                                                                              |
| :---------- | :--------------------------------------------------------------------------------------- |
| dict        | A dictionary containing information from the [fdl.ModelInfo()](ref:fdlmodelinfo) object. |

```python Usage
import pandas as pd

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(
    df=df
)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    features=[
        'feature_1',
        'feature_2',
        'feature_3'
    ],
    outputs=[
        'output_column'
    ],
    target='target_column',
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.BINARY_CLASSIFICATION
)

model_info_dict = model_info.to_dict()
```

```python Response
{
    'name': 'Example Model',
    'input-type': 'structured',
    'model-task': 'binary_classification',
    'inputs': [
        {
            'column-name': 'feature_1',
            'data-type': 'float'
        },
        {
            'column-name': 'feature_2',
            'data-type': 'int'
        },
        {
            'column-name': 'feature_3',
            'data-type': 'bool'
        },
        {
            'column-name': 'target_column',
            'data-type': 'int'
        }
    ],
    'outputs': [
        {
            'column-name': 'output_column',
            'data-type': 'float'
        }
    ],
    'datasets': [],
    'targets': [
        {
            'column-name': 'target_column',
            'data-type': 'int'
        }
    ],
    'custom-explanation-names': []
}
```
