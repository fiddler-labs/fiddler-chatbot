---
title: "client.run_model"
slug: "clientrun_model"
excerpt: "Runs a model on a pandas DataFrame and returns the predictions."
hidden: false
createdAt: "2022-05-23T20:56:16.995Z"
updatedAt: "2023-08-01T12:43:52.465Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Use _client.model_names()_ instead.  
> Reference: [client.get_predictions](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_predictions)

| Input Parameter | Type            | Default | Description                                                                                                                     |
| :-------------- | :-------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------ |
| project_id      | str             | None    | The unique identifier for the project.                                                                                          |
| model_id        | str             | None    | A unique identifier for the model.                                                                                              |
| df              | pd.DataFrame    | None    | A pandas DataFrame containing model input vectors as rows.                                                                      |
| log_events      | Optional [bool] | False   | If True, the rows of df along with the model predictions will be logged as production events.                                   |
| casting_type    | Optional [bool] | False   | If True, will try to cast the data in the events to be in line with the data types defined in the model's **ModelInfo** object. |

```python Usage
import pandas as pd

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

df = pd.read_csv('example_data.csv')

predictions = client.run_model(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    df=df
)
```

| Return Type  | Description                                                                  |
| :----------- | :--------------------------------------------------------------------------- |
| pd.DataFrame | A pandas DataFrame containing model predictions for the given input vectors. |