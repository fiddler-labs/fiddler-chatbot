---
title: ML Monitoring - CV Inputs
slug: cv-monitoring
metadata:
  title: 'Quickstart: CV Monitoring | Fiddler Docs'
  description: >-
    This document is a guide on using Fiddler for monitoring computer vision
    models and detecting drift in image data using Fiddler's Vector Monitoring
    approach.
  robots: index
icon: notebook
---

# ML Monitoring - CV Inputs

This guide will walk you through the basic steps required to use Fiddler for monitoring computer vision (CV) models. In this notebook we demonstrate how to detect drift in image data using model embeddings using Fiddler's unique Vector Monitoring approach.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Image_Monitoring.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Image_Monitoring.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Monitoring Image data using Fiddler Vector Monitoring

In this notebook we present the steps for monitoring images. Fiddler employs a vector-based monitoring approach that can be used to monitor data drift in high-dimensional data such as NLP embeddings, images, video etc. In this notebook we demonstrate how to detect drift in image data using model embeddings and determine the cause of that drift.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**.
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's Image monitoring ***in minutes*** by following these quick steps:

1. Connect to Fiddler
2. Load and generate embeddings for CIFAR-10 dataset
3. Upload the vectorized baseline dataset
4. Add metadata about your model
5. Inject data drift and publish production events
6. Get insights

## Imports


```python
!pip install torch==2.0.0
!pip install torchvision==0.15.1
!pip install -q fiddler-client
```


```python
import io
import numpy as np
import pandas as pd
import random
import time
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import requests

import fiddler as fdl
print(f"Running Fiddler client version {fdl.__version__}")
```

## 2. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our API client.


---


**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your authorization token

These can be found by navigating to the **Settings** page of your Fiddler environment.


```python
URL = ''  # Make sure to include the full URL (including https://).
TOKEN = ''
```

Now just run the following code block to connect to the Fiddler API!


```python
fdl.init(
    url=URL,
    token=TOKEN
)
```

Once you connect, you can create a new project by calling a Project's `create` method.


```python
PROJECT_NAME = 'image_monitoring'

project = fdl.Project(
    name=PROJECT_NAME
)

project.create()
```

## 2. Generate Embeddings for CIFAR-10 data

In this example, we'll use the popular CIFAR-10 classification dataset and a model based on Resnet-18 architecture. For the purpose of this example we have pre-trained the model.
  
In order to compute data and prediction drift, **Fiddler needs a sample of data that can serve as a baseline** for making comparisons with data in production. When it comes to computing distributional shift for images, Fiddler relies on the model's intermediate representations also known as activations or embeddings. You can read more about our approach [here](https://www.fiddler.ai/blog/monitoring-natural-language-processing-and-computer-vision-models-part-1).

In the the following cells we'll extract these embeddings.


```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Device to be used: {device}')
```

Let us load the pre-trained model


```python
MODEL_URL='https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/resnet18_cifar10_epoch5.pth'
MODEL_PATH='resnet18_cifar10_epoch5.pth'

def load_model(device):
    """Loads the pre-trained CIFAR-10 model"""
    model = resnet18()
    model.fc = nn.Sequential(
        nn.Linear(512, 128),
        nn.ReLU(),
        nn.Linear(128, 10),
    )

    r = requests.get(MODEL_URL)
    with open(MODEL_PATH,'wb') as f:
        f.write(r.content)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device(device)))
    model.to(device)
    return model

resnet_model = load_model(device)

```

We'll load four tranches of [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) data for this example.  "reference" – corresponding to train-time reference data, and three "production" sets with diffrent transformations applied to simulate drift from the model's training data. Note that running the cell below will download the CIFAR-10 data and load them using torch's dataloaders.


```python
BATCH_SIZE = 32

transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ])

DATA_BASE_URL = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/cv_monitoring/'

# download file from URL
DATA_URLS = {
 'reference' : DATA_BASE_URL + 'reference/image_data.npz',
'production_1': DATA_BASE_URL + 'production_1/image_data.npz', # Undrifted
'production_2': DATA_BASE_URL + 'production_2/image_data.npz', # Blurred
'production_3': DATA_BASE_URL + 'production_3/image_data.npz'} # Darkened


def get_dataloader(dataset):
  response = requests.get(DATA_URLS[dataset])
  data = np.load(io.BytesIO(response.content))

  images = [transform(x) for x in data['arr_0']]
  labels = data['arr_1']

  tuple_list = list(zip(images, labels))

  return torch.utils.data.DataLoader(
      tuple_list,
      batch_size=BATCH_SIZE,
      shuffle=False,
      num_workers=2
  )

# let's test it
get_dataloader('reference')
```

***In the cell below we define functions that will extract the 128-dimensional embedding from the FC1 layer of the model and package them in a dataframe along with predictions, ground-truth labels, and image URLs***


```python
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

torch.manual_seed(0)

CIFAR_CLASSES = (
    'plane', 'car', 'bird', 'cat',
    'deer', 'dog', 'frog',
    'horse', 'ship', 'truck',
)

global view_fc1_output_embeds

def fc1_hook_func(model, input, output):
    global view_fc1_output_embeds
    view_fc1_output_embeds = output

def idx_to_classes(target_arr):
    return [CIFAR_CLASSES[int(i)] for i in target_arr]

def generate_embeddings(model, device, dataset_name):
    """Generate embeddings for the inout images"""

    dataloader = get_dataloader(dataset_name)

    fc1_embeds = []
    output_scores = []
    target = []

    with torch.no_grad():
        model = model.eval()
        fc1_module = model.fc[0]
        fc1_hook = fc1_module.register_forward_hook(fc1_hook_func)
        correct_preds = 0
        total_preds = 0

        try:
            for inputs, labels in dataloader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                outputs_smax = F.softmax(outputs, dim=1)
                _, preds = torch.max(outputs, 1)
                correct_preds += torch.sum(preds == labels.data).cpu().numpy()
                total_preds += len(inputs)

                fc1_embeds.append(view_fc1_output_embeds.cpu().detach().numpy())
                output_scores.append(outputs_smax.cpu().detach().numpy())
                target.append(labels.cpu().detach().numpy())

            fc1_embeds = np.concatenate(fc1_embeds)
            output_scores = np.concatenate(output_scores)
            target = np.concatenate(target)

        except Exception as e:
            fc1_hook.remove()
            raise

        print(f'{correct_preds}/{total_preds}: {100*correct_preds/total_preds:5.1f}% correct predictions.')

    embs = deepcopy(fc1_embeds)
    labels = idx_to_classes(target)
    embedding_cols = ['emb_'+str(i) for i in range(128)]
    baseline_embeddings = pd.DataFrame(embs, columns=embedding_cols)

    columns_to_combine = baseline_embeddings.columns
    baseline_embeddings = baseline_embeddings.apply(lambda row: row[columns_to_combine].tolist(), axis=1).to_frame()
    baseline_embeddings = baseline_embeddings.rename(columns={baseline_embeddings.columns[0]: 'embeddings'})

    baseline_predictions = pd.DataFrame(output_scores, columns=CIFAR_CLASSES)
    baseline_labels = pd.DataFrame(labels, columns=['target'])
    embeddings_df = pd.concat(
        [baseline_embeddings, baseline_predictions, baseline_labels],
        axis='columns',
        ignore_index=False
    )

    embeddings_df['image_url'] = embeddings_df.apply(lambda row:DATA_BASE_URL + dataset_name + '/' + str(row.name) + '.png', axis=1)


    return embeddings_df

```

We'll now extract the embeddings for training data which will serve as baseline for monitoring.


```python
sample_df = generate_embeddings(resnet_model, device, 'reference')
sample_df.head()
```

# 4. Add metadata about the model

Next we must tell Fiddler a bit more about our model.  This is done by by creating defining some information about our model's task, inputs, output, target and which features form the image embedding and then creating a `Model` object.

Let's first define our Image vector using the API below.


```python
image_embedding_feature = fdl.ImageEmbedding(
    name='image_feature',
    source_column='image_url',
    column='embeddings',
)
```

Now let's define a `ModelSpec` object with information about the columns in our data sample.


```python
model_spec = fdl.ModelSpec(
    inputs=['embeddings'],
    outputs=CIFAR_CLASSES,
    targets=['target'],
    metadata=['image_url'],
    custom_features=[image_embedding_feature],
)

timestamp_column = 'timestamp'
```

Then let's specify some information about the model task.


```python
model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=list(CIFAR_CLASSES))
```

Then we create a `Model` schema using the example data.


```python
MODEL_NAME = 'resnet18'

model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=fdl.Project.from_name(PROJECT_NAME).id,
    source=sample_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params,
    event_ts_col=timestamp_column
)

model.create()
```

Additionally, let's publish the baseline data so we can use it as a reference for measuring drift and to compare production data with in Embedding Visualization for root-cause analysis.


```python
model.publish(
    source=sample_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name='train_time_reference',
)
```

# 5. Publish events to Fiddler
We'll publish events over past 3 weeks.

- Week 1: We publish CIFAR-10 test set, which would signify no distributional shift
- Week 2: We publish **blurred** CIFAR-10 test set
- Week 3: We publish **brightness reduced** CIFAR-10 test set


```python
for i, dataset_name in enumerate(['production_1', 'production_2', 'production_3']):
    week_days = 6
    prod_df = generate_embeddings(resnet_model, device, dataset_name)
    week_offset = (2-i)*7*24*60*60*1e3
    day_offset = 24*60*60*1e3
    print(f'Publishing events from {dataset_name} transformation for week {i+1}.')
    for day in range(week_days):
        now = time.time() * 1000
        timestamp = int(now - week_offset - day*day_offset)
        events_df = prod_df.sample(1000)
        events_df['timestamp'] = timestamp
        model.publish(events_df)
```

## 6. Get insights

**You're all done!**
  
You can now head to your Fiddler URL and start getting enhanced observability into your model's performance.

Fiddler can now track your image drift over time based on the embedding vectors of the images published into the platform.

While we saw performace degrade for the various drifted data sets in the notebook when publishing (which can also be plotted in the Monitoring chart), embedding drift doesn't require ground-truth labels and often serves as a useful proxy that can indicate a problem or degraded performance.  Data drift is indicated by nonzero Jensen-Shannon Distance measured with respect to a reference sample.

Please visit your Fiddler environment upon completion to check this out for yourself.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/image_monitoring_2024_12_1.png" />
        </td>
    </tr>
</table>

In order to identify the root cause of data drift, Fiddler allows you to "drill-down" into time windows where embedding drift is measured.  As indicated in blue in the image above, by selecting a time bin and clicking the "Embeddings" button, you'll be take to an Embedding Visualization chart where data from that time window is compared against reference data (e.g. `train_time_reference` that we published above) in an interactive 3D UMAP plot.

In the image below, the embedded images in the drifted time period are semantically distinct to your model from those in the train-time sample.  By investigating these differenes, it's easy to determine that the third "production" sample is systematically darkened.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/image_monitoring_2024_12_2.png" />
        </td>
    </tr>
</table>



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
