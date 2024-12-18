---
title: Uploading a scikit-learn Model Artifact
slug: scikit-learn
excerpt: ''
createdAt: Tue Apr 19 2022 20:13:31 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)
---

# Scikit Learn

> 🚧 Note
>
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](../uploading-model-artifacts.md).

Suppose you would like to upload a model artifact for a **scikit-learn model**.

Following is an example of what the `package.py` script might look like.

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

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

