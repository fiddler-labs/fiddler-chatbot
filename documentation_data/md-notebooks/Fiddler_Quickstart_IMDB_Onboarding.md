# Onboarding IMDB Movie Reviews for NLP Explainability

In this notebook, we present the steps for onboarding a model artifact to Fiddler that predicts the sentiment of IMDB movie reviews.  Fiddler is able to explain complex models with a variety of input types like unstructured text, images, and multi-modal.  

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these four quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact (plus any other files needed to load the model)**
4. Explain your model

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'imdb_explainability'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we have a model that **predicts sentiment for movie reviews**.  
  
**Fiddler needs a small  sample of data that can serve as a baseline**.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/imdb_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'imdb_baseline'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have the assets required to load the model and a package.py script that tells Fiddler how to call the model's prediction endpoint.  It doesn't matter what this directory is called, but for this example we will call it **/model**.  We also need a few subdirectories to house other assets needed to load the model.


```python
import os
os.makedirs("model")
os.makedirs("model/saved_model")
os.makedirs("model/saved_model/variables")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** and other files required to load the model
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
target = 'polarity'
features = ['sentence']
output = ['sentiment']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TEXT,
    model_task=fdl.ModelTask.BINARY_CLASSIFICATION,
    outputs=output,
    display_name='IMDB Sentiment Classifier',
    description='imdb rnn sentiment classifier',
    preferred_explanation_method=fdl.ExplanationMethod.IG_FLEX
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'imdb_rnn'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pathlib
import pickle

from tensorflow.keras.preprocessing import sequence

from fiddler.packtools import project_attributions_helpers, template_model

# Name the output of your model here - this will need to match the model schema we define in the next notebook
OUTPUT_COL = ['sentiment']

# These are the names of the inputs of your TensorFlow model
FEATURE_LABEL = 'sentence'

MODEL_ARTIFACT_PATH = 'saved_model'

TOKENIZER_PATH = 'tokenizer.pkl'

ATTRIBUTABLE_LAYER_NAMES_MAPPING = {'embedding': ['sentence']}
EMBEDDING_NAMES = ['embedding']

MAX_SEQ_LENGTH = 150

BATCH_INPUT_SHAPE_LIST = [(None, 150, 64)]


class FiddlerModel(template_model.TemplateKerasTF2Model):
    def __init__(
        self,
        model_artifact_path,
        tokenizer_path,
        attributable_layer_names_mapping,
        embedding_names,
        batch_input_shape_list,
        output_col,
    ):

        self.model_dir = pathlib.Path(__file__).parent
        super().__init__(
            self.model_dir,
            model_artifact_path,
            attributable_layer_names_mapping,
            output_col,
            embedding_names,
            batch_input_shape_list,
        )

        with open(str(self.model_dir / tokenizer_path), 'rb') as f:
            self.tokenizer = pickle.load(f)

    def get_ig_baseline(self, input_df):
        """This method is used to generate the baseline against which to compare the input.
        It accepts a pandas DataFrame object containing rows of raw feature vectors that
        need to be explained (in case e.g. the baseline must be sized according to the explain point).
        Must return a pandas DataFrame that can be consumed by the predict method described earlier.
        """
        baseline_df = input_df.copy()
        baseline_df[FEATURE_LABEL] = input_df[FEATURE_LABEL].apply(lambda x: '')

        return baseline_df

    def _transform_input(self, input_df):
        """Helper function that accepts a pandas DataFrame object containing rows of raw feature vectors.
        The output of this method can be any Python object. This function can also
        be used to deserialize complex data types stored in dataset columns (e.g. arrays, or images
        stored in a field in UTF-8 format).
        """
        sequences = self.tokenizer.texts_to_sequences(input_df[FEATURE_LABEL])
        sequences_matrix = sequence.pad_sequences(
            sequences, maxlen=MAX_SEQ_LENGTH, padding='post'
        )
        return sequences_matrix.tolist()

    def project_attributions(self, input_df, attributions):
        proj_attr = project_attributions_helpers.IGTextAttributionsTF2Keras(
            input_df, OUTPUT_COL
        )
        word_tokens = proj_attr.text_to_tokens_keras(
            self.tokenizer, MAX_SEQ_LENGTH, FEATURE_LABEL
        )

        return proj_attr.get_project_attribution(
            attributions, self.tokenizer, word_tokens, EMBEDDING_NAMES[0], FEATURE_LABEL
        )


def get_model():
    return FiddlerModel(
        model_artifact_path=MODEL_ARTIFACT_PATH,
        tokenizer_path=TOKENIZER_PATH,
        attributable_layer_names_mapping=ATTRIBUTABLE_LAYER_NAMES_MAPPING,
        embedding_names=EMBEDDING_NAMES,
        batch_input_shape_list=BATCH_INPUT_SHAPE_LIST,
        output_col=OUTPUT_COL,
    )
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's binary file, other required assets and our requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/imdb/tokenizer.pkl", "model/tokenizer.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/imdb/saved_model/keras_metadata.pb", "model/saved_model/keras_metadata.pb")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/imdb/saved_model/saved_model.pb", "model/saved_model/saved_model.pb")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/imdb/saved_model/variables/variables.data-00000-of-00001", "model/saved_model/variables/variables.data-00000-of-00001")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/imdb/saved_model/variables/variables.index", "model/saved_model/variables/variables.index")
```

### 3.4 Define Model Parameters 

Fiddler provides extreme flexibility when onboarding a model artifact for explainability.  Each model runs in its own container with the libraries it needs as defined in the requirement.txt file.  The container is built from a base image and we can specify the compute needs our model requires.  This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/deep-learning:1.0.0",
                                                cpu=1000,
                                                memory=1300,
                                                replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Explain your model

**You're all done!**
  
Now just head to your Fiddler environment's UI and check out NLP explainability for this model.  You can also run the explanation from the Fiddler client.


```python
#grab a row from the baseline to run an explanation on
row = baseline_df.to_dict(orient='records')[0]
row
```


```python
explanation = client.get_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_data_source=fdl.RowDataSource(row=row),
    explanation_type='FIDDLER_SHAP'
)
explanation
```


```python
predictions = client.get_predictions(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_df=baseline_df.iloc[:5],
)
predictions
```



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
