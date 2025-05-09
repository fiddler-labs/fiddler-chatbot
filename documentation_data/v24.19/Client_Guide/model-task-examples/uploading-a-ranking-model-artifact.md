---
title: Ranking Model Package.py
slug: uploading-a-ranking-model-artifact
excerpt: ''
createdAt: Mon Oct 31 2022 21:23:47 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)
---

# Uploading A Ranking Model Artifact

> 🚧 Note
>
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](../uploading-model-artifacts.md).

Suppose you would like to upload a model artifact for a **ranking model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        self.output_columns = ['score']
        with open('{PACKAGE_PATH}/model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def predict(self, input_df):
        pred = self.model.predict(input_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

Here, we are assuming that the model prediction column that has been specified in the [`fdl.ModelSpec`](../../Python\_Client\_3-x/api-methods-30.md#modelspec) object is called `score`.

Please checkout this [quickstart notebook](../../QuickStart\_Notebooks/ranking-model.md) to work through an example of onboarding a ranking model on to Fiddler.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

