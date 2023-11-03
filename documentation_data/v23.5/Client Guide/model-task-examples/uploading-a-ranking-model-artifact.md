---
title: "Ranking Model Package.py"
slug: "uploading-a-ranking-model-artifact"
hidden: false
createdAt: "2022-10-31T21:23:47.193Z"
updatedAt: "2023-10-19T20:59:24.691Z"
---
> 🚧 Note
> 
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

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
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def predict(self, input_df):
        pred = self.model.predict(input_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

Here, we are assuming that the model prediction column that has been specified in the [`fdl.ModelInfo`](ref:fdlmodelinfo) object is called `score`.

Please checkout this [quickstart notebook](doc:ranking-model) to work through an example of onboarding a ranking model on to Fiddler.