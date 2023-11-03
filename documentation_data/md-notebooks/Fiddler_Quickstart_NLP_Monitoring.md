# Monitoring NLP data using Fiddler Vector Monotoring

In this notebook we present the steps for using Fiddler NLP monitoring. Fiddler employs a vector-based monitoring approach that can be used to monitor data drift in multi-dimensional data such as NLP embeddings and images. In this notebook we show a use case for monitoring NLP embeddings to detect drift in text data.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Load and vectorize 20Newsgroup data
2. Upload the vectorized baseline dataset
3. Add metadata about your model
4. Publish production events
5. Get insights

## Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Now just run the following code block to connect to the Fiddler API!


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'simple_nlp_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Load and vectorize 20Newsgroup data

In order to get insights into the model's performance, **Fiddler needs a small sample of data that can serve as a baseline** for making comparisons with production inferences (aka. events).

For this model's baseline dataset, we will use the __"20 newsgroups text dataset"__.  This dataset contains around 18,000 newsgroups posts on 20 topics. This dataset is available as one of the standard scikit-learn real-world datasets and can be be fechted directly using scikit-learn.

Let's first load our baseline dataset into a dataframe and then squeeze the "news" column into a Series to ready it for vectorization.


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/newsgroup20_baseline_gold.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
base_series = baseline_df['news'].squeeze()
base_series
```

Great!  Now let's vectorize this NLP data using one of the two methods below.

### Vectorization

Fiddler monitors NLP and CV data by using encoded data in the form of embeddings, or **vectors**.  Before we load our baseline or our event data into the Fiddler platform for monitoring purposes, we must *vectorize* the raw NLP input.  

The follow section provides two methods of vectorizing the NLP data: *TF-IDF vectorization* and *word2vec*.  Please run only 1 method.

***Method 1: TF-IDF vectorization***


```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(sublinear_tf=True, max_features=300, min_df=0.01, max_df=0.9, stop_words='english')
vectorizer.fit(base_series)
tfidf_baseline_sparse = vectorizer.transform(base_series)

# Trasnform our sparse matrix of TFIDF values into a dataframe with an embedding vector as a list of values
df = pd.DataFrame(tfidf_baseline_sparse.toarray().tolist())
columns_to_combine = df.columns  
df_embeddings = df.apply(lambda row: row[columns_to_combine].tolist(), axis=1).to_frame()
df_embeddings = df_embeddings.rename(columns={df_embeddings.columns[0]: 'embeddings'})
df_embeddings
```


***Method 2: word2vec by Spacy***

The following lines show how to use ***word2vec*** embedding from Sacy. In order to run the following cell, you need to install spacy and its pre-trained models like 'en_core_web_lg'. See: https://spacy.io/usage


```python
# import spacy
# nlp = spacy.load('en_core_web_lg')

# s = time.time()
# base_embeddings = base_series.apply(lambda sentence: nlp(sentence).vector)
# print(f' Time to compute embeddings {time.time() - s}')

# baseline_df = pd.DataFrame(base_embeddings.values.tolist())
# baseline_df = baseline_df.rename(columns = {c:'f'+str(c+1) for c in baseline_df.columns})
```

Now that we've vectorized our data, let's drop the unstructured "news" column and snap the vectorized data to our original baseline dataframe.


```python
baseline_df = pd.concat([baseline_df, df_embeddings], axis=1)
baseline_df
```

# 3. Upload the vectorized baseline dataset to Fiddler

Next, let's create a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to describe our baseline dataset and then [upload_dataset()](https://docs.fiddler.ai/reference/clientupload_dataset) to Fiddler.


```python
DATASET_ID = 'simple_newsgroups_1'  # The dataset name in Fiddler platform
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df)

if not DATASET_ID in client.list_datasets(project_id=PROJECT_ID):
    print(f'Upload dataset {DATASET_ID}')
    
    client.upload_dataset(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        dataset={'baseline': baseline_df},
        info=dataset_info
    )
    
else:
    print(f'Dataset: {DATASET_ID} already exists in Project: {PROJECT_ID}.\n'
               'The new dataset is not uploaded. (please use a different name.)') 
```

# 4. Add metadata about the model

Next we must tell Fiddler a bit more about our model.  This is done by calling [.add_model()](https://docs.fiddler.ai/reference/clientadd_model).  When calling [.add_model()](https://docs.fiddler.ai/reference/clientadd_model), we must pass in a [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object to tell Fiddler about our model.  This [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object will tell Fiddler about our model's task, inputs, output, target and which features are apart of the NLP vector created above.

Let's first define our NLP vector using a custom feature of type TextEmbedding.  The custom feature will be called *text_embedding* which groups together our embedding vector column, *embeddings*, and our raw source column, *news*.


```python
CF1 = fdl.TextEmbedding(
    name='text_embedding',
    column='embeddings',
    source_column='news',
    n_clusters=6
)
```

Now let's define our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.


```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
    
# Specify column types
target = 'target'
outputs = ['predicted_score']
features = baseline_df.columns.drop(['target', 'predicted_score']).tolist()

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info = dataset_info,
    dataset_id = DATASET_ID,
    features = features,
    target = target,
    outputs = outputs,
    custom_features = [CF1],
    model_task=model_task,
    description='An example model to showcase monitoring NLP data by vectorizing the unstructured data.',
    binary_classification_threshold=0.5 #optional
)
model_info
```

And call [.add_model()](https://docs.fiddler.ai/reference/clientadd_model) to tell Fiddler about our model.


```python
MODEL_ID = 'newsgroup_model_v1' # choose a different model ID

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

# 5. Publish production events

Let's publish some production events into Fiddler.  This .csv file already has some manufactured drift introduced to the NLP data by sampling from the newsgroup20 dataset more heavily in certain topics.  


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/newsgroup20_events_gold.csv'

events_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# in the csv file the embeddings are stored in different columns. let's combine them into a list in a new column called 'embeddings'
columns_to_combine = [col for col in events_df.columns if col.startswith('f')]
events_df['embeddings'] = events_df.apply(lambda row: row[columns_to_combine].tolist(), axis=1)
events_df = events_df.drop(columns=columns_to_combine)
events_df
```

Now let's time shift the timestamps in this event dataset so that they are as recent as today's date.


```python
from datetime import datetime

# Timeshifting the timestamp column in the events file so the events are as recent as today
ts_col = 'timestamp'
events_df[ts_col]  = pd.to_datetime(events_df[ts_col], origin='unix', unit='ms')
max_dt = events_df[ts_col].max()
delta = datetime.now() - max_dt
events_df[ts_col] = events_df[ts_col] + pd.to_timedelta(delta.total_seconds(), unit='s')
events_df
```

And, finally, publish our events as a batch.


```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source=events_df,
    timestamp_field= ts_col
)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment and start getting enhanced observability into your model's performance.

<table>
    <tr>
        <td><img src="https://github.com/fiddler-labs/fiddler-examples/raw/main/quickstart/images/nlp_monitoring_1.png" /></td>
    </tr>
</table>

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
