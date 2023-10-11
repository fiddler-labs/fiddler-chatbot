---
title: "Uploading a TensorFlow SavedModel Model Artifact"
slug: "tensorflow-savedmodel"
hidden: false
createdAt: "2022-04-19T20:13:41.335Z"
updatedAt: "2022-06-08T15:37:37.074Z"
---
[block:callout]
{
  "type": "warning",
  "title": "Note",
  "body": "For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-a-model-artifact)."
}
[/block]
Suppose you would like to upload a model artifact for a **TensorFlow (SavedModel) model**.

Following is an example of what the `package.py` script may look like.

```python
import pickle
from pathlib import Path
import pandas as pd
import tensorflow as tf

PACKAGE_PATH = Path(__file__).parent

OUTPUT_COLUMN = ['probability_over_50k']

class MyModel:

    def __init__(self):
        
        # Load the model
        self.model = tf.keras.models.load_model(PACKAGE_PATH / 'saved_model')

    def predict(self, input_df):
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict(input_df), columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```