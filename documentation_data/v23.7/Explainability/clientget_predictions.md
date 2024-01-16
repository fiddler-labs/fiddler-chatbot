---
title: "client.get_predictions"
slug: "clientget_predictions"
excerpt: "Runs a model on a pandas DataFrame and returns the predictions."
hidden: false
createdAt: "Wed Aug 16 2023 11:19:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type          | Default | Description                                                            |
| :-------------- | :------------ | :------ | :--------------------------------------------------------------------- |
| project_id      | str           | None    | A unique identifier for the project.                                   |
| model_id        | str           | None    | A unique identifier for the model.                                     |
| input_df        | pd.DataFrame  | None    | A pandas DataFrame containing model input vectors as rows.             |
| chunk_size      | Optional[int] | 10000   | The chunk size for fetching predictions. Default is 10_000 rows chunk. |

```python Usage
import pandas as pd

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

input_df = pd.read_csv('example_data.csv')

# Example without chunk size specified:
predictions = client.get_predictions(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_df=input_df,
)


# Example with chunk size specified:
predictions = client.get_predictions(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_df=input_df,
    chunk_size=1000,
)
```

| Return Type  | Description                                                                  |
| :----------- | :--------------------------------------------------------------------------- |
| pd.DataFrame | A pandas DataFrame containing model predictions for the given input vectors. |
