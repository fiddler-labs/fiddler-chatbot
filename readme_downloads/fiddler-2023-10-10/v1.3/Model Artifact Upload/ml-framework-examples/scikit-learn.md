---
title: "Uploading a scikit-learn Model Artifact"
slug: "scikit-learn"
hidden: false
createdAt: "2022-04-19T20:13:31.741Z"
updatedAt: "2022-06-08T15:37:16.330Z"
---
[block:callout]
{
  "type": "warning",
  "title": "Note",
  "body": "For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-a-model-artifact)."
}
[/block]
Suppose you would like to upload a model artifact for a **scikit-learn model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression

PACKAGE_PATH = Path(__file__).parent

OUTPUT_COLUMN = ['probability_over_50k']

class MyModel:

    def __init__(self):
        
        # Load the model
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as pkl_file:
            self.model = pickle.load(pkl_file)

    def predict(self, input_df):
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict_proba(input_df)[:, 1], columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```