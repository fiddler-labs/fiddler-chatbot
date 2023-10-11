---
title: "client.get_predictions"
slug: "clientget_predictions"
excerpt: "Runs a model on a pandas DataFrame and returns the predictions."
hidden: true
createdAt: "2023-08-01T12:14:19.261Z"
updatedAt: "2023-08-01T13:50:35.335Z"
---
| Input Parameter | Type            | Default | Description                                                                                                                     |
| :-------------- | :-------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------ |
| project_name    | str             | None    | The unique identifier for the project.                                                                                          |
| model_name      | str             | None    | A unique identifier for the model.                                                                                              |
| input_df        | pd.DataFrame    | None    | A pandas DataFrame containing model input vectors as rows.                                                                      |
| chunk_size      | Optional[int]   | None    | The chunk size for fetching predictions.                                                                                        |
| project_id      | str             | None    | `Deprecated` The unique identifier for the project.                                                                             |
| model_id        | str             | None    | `Deprecated` A unique identifier for the model.                                                                                 |
| df              | pd.DataFrame    | None    | `Deprecated` A pandas DataFrame containing model input vectors as rows.                                                         |
| log_events      | Optional [bool] | False   | If True, the rows of df along with the model predictions will be logged as production events.                                   |
| casting_type    | Optional [bool] | False   | If True, will try to cast the data in the events to be in line with the data types defined in the model's **ModelInfo** object. |

```python Usage
import pandas as pd

PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

input_df = pd.read_csv('example_data.csv')

predictions = client.run_model(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    input_df=input_df
)
```

| Return Type  | Description                                                                  |
| :----------- | :--------------------------------------------------------------------------- |
| pd.DataFrame | A pandas DataFrame containing model predictions for the given input vectors. |