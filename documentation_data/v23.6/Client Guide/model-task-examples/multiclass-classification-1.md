---
title: "Multi-class Classification Model Package.py"
slug: "multiclass-classification-1"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:12:40 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
> 🚧 Note
> 
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-a-model-artifact).

Suppose you would like to upload a model artifact for a **multiclass classification model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

OUTPUT_COLUMNS = ['probability_0', 'probability_1', 'probability_2']

class MyModel:

    def __init__(self):
        
        # Load the model
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as pkl_file:
            self.model = pickle.load(pkl_file)

    def predict(self, input_df):
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict_proba(input_df), columns=OUTPUT_COLUMNS)

def get_model():
    return MyModel()
```

Here, we are assuming that the model prediction columns that have been specified in the [`fdl.ModelInfo`](ref:fdlmodelinfo) object are called `probability_0`, `probability_1`, and `probability_2`.