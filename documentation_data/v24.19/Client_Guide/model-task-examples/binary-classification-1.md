---
title: Binary Classification Model Package.py
slug: binary-classification-1
excerpt: ''
createdAt: Tue Apr 19 2022 20:12:34 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 21:08:14 GMT+0000 (Coordinated Universal Time)
---

# Binary Classification 1

> 🚧 Note
>
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](../uploading-model-artifacts.md).

Suppose you would like to upload a model artifact for a **binary classification model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

OUTPUT_COLUMN = ['probability_over_50k']

class MyModel:

    def __init__(self):
        
        # Load the model
        with open(f'{PACKAGE_PATH}/model.pkl', 'rb') as pkl_file:
            self.model = pickle.load(pkl_file)

    def predict(self, input_df):
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict_proba(input_df)[:, 1], columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```

Here, we are assuming that the model prediction column that has been specified in the [ModelSpec](../../Python\_Client\_3-x/api-methods-30.md#modelspec) object is called `probability_over_50k`.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

