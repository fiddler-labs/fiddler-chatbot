---
title: "Uploading a TensorFlow HDF5 Model Artifact"
slug: "tensorflow-hdf5"
hidden: false
createdAt: "2022-04-19T20:14:00.253Z"
updatedAt: "2023-04-07T14:33:03.011Z"
---
> 🚧 Note
> 
> For more information on uploading a model artifact to Fiddler, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

Suppose you would like to upload a model artifact for a **TensorFlow (HDF5) model**.

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
        self.model = tf.keras.models.load_model(PACKAGE_PATH / 'model.h5')

    def predict(self, input_df):
        
        # Store predictions in a DataFrame
        return pd.DataFrame(self.model.predict(input_df), columns=OUTPUT_COLUMN)

def get_model():
    return MyModel()
```