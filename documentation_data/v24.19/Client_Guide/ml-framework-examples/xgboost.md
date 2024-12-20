---
title: Uploading an XGBoost Model Artifact
slug: xgboost
excerpt: ''
createdAt: Tue Apr 19 2022 20:13:35 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)
---

# Xgboost

> 🚧 Note
>
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](../uploading-model-artifacts.md).

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
        return xgb.DMatrix(input_df)

    def predict(self, input_df):
        
        # Apply data transformation
        transformed_input = self.transform_input(input_df)
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict(transformed_input), columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

