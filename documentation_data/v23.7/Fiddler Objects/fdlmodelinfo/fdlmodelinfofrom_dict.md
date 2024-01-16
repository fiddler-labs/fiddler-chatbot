---
title: "fdl.ModelInfo.from_dict"
slug: "fdlmodelinfofrom_dict"
excerpt: "Converts a dictionary to a ModelInfo object."
hidden: false
createdAt: "Tue May 24 2022 15:56:13 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters  | Type | Default | Description                           |
| :---------------- | :--- | :------ | :------------------------------------ |
| deserialized_json | dict |         | The dictionary object to be converted |

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

new_model_info = fdl.ModelInfo.from_dict(
    deserialized_json={
        'model': model_info_dict
    }
)
```

| Return Type   | Description                                                                   |
| :------------ | :---------------------------------------------------------------------------- |
| fdl.ModelInfo | A [fdl.ModelInfo()](ref:fdlmodelinfo) object constructed from the dictionary. |
