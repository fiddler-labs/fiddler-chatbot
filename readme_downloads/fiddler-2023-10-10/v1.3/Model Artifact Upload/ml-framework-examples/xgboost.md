---
title: "Uploading an XGBoost Model Artifact"
slug: "xgboost"
hidden: false
createdAt: "2022-04-19T20:13:35.640Z"
updatedAt: "2022-06-08T15:37:26.137Z"
---
[block:callout]
{
  "type": "warning",
  "title": "Note",
  "body": "For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-a-model-artifact)."
}
[/block]
Suppose you would like to upload a model artifact for a **XGBoost model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd
import xgboost as xgb

PACKAGE_PATH = Path(__file__).parent

OUTPUT_COLUMN = ['probability_over_50k']

class MyModel:

    def __init__(self):
        
        # Load the model
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as pkl_file:
            self.model = pickle.load(pkl_file)

    def transform_input(self, input_df):
        
        # Convert DataFrame to XGBoost DMatrix
        transformed_input = xgb.DMatrix(input_df)

    def predict(self, input_df):
        
        # Apply data transformation
        transformed_input = self.transform_input(input_df)
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict(transformed_input), columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```