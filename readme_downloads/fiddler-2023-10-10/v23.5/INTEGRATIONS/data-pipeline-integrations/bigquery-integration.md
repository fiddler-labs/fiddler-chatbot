---
title: "BigQuery Integration"
slug: "bigquery-integration"
hidden: false
createdAt: "2022-05-20T18:53:49.606Z"
updatedAt: "2023-06-13T19:09:07.072Z"
---
## Using Fiddler on your ML data stored in BigQuery

In this article, we will be looking at loading data from BigQuery tables and using the data for the following tasks-

1. Uploading baseline data to Fiddler
2. Onboarding a model to Fiddler and creating a surrogate
3. Publishing production data to Fiddler

## Step 1 - Enable BigQuery API

Before looking at how to import data from BigQuery to Fiddler, we will first see how to enable BigQuery API. This can be done as follows - 

1. In the GCP platform, Go to the navigation menu -> click APIs & Services. Once you are there, click + Enable APIs and Services (Highlighted below). In the search bar, enter BigQuery API and click Enable.

![](https://files.readme.io/75ca647-Screen_Shot_2022-05-19_at_1.26.33_PM.png "Screen Shot 2022-05-19 at 1.26.33 PM.png")

![](https://files.readme.io/3dd5deb-Screen_Shot_2022-05-19_at_3.33.43_PM.png "Screen Shot 2022-05-19 at 3.33.43 PM.png")

2. In order to make a request to the API enabled in Step#1, you need to create a service account and get an authentication file for your Jupyter Notebook. To do so, navigate to the Credentials tab under APIs and Services console and click Create Credentials tab, and then Service account under dropdown.

![](https://files.readme.io/ea63eca-Screen_Shot_2022-05-19_at_3.34.24_PM.png "Screen Shot 2022-05-19 at 3.34.24 PM.png")

3. Enter the Service account name and description. You can use the BigQuery Admin role under Grant this service account access to the project. Click Done. You can now see the new service account under the Credentials screen. Click the pencil icon beside the new service account you have created and click Add Key to add auth key. Please choose JSON and click CREATE. It will download the JSON file with auth key info. (Download path will be used to authenticate)

![](https://files.readme.io/662315e-Screen_Shot_2022-05-19_at_3.39.24_PM.png "Screen Shot 2022-05-19 at 3.39.24 PM.png")

## Step 2 - Import data from BigQuery

We will now use the generated key to connect to BigQuery tables from Jupyter Notebook. 

1. Install the following libraries in the python environment and load them to jupyter-

- Google-cloud
- Google-cloud-bigquery[pandas]
- Google-cloud-storage

2. Set the environment variable using the key that was generated in Step 1

```python
#Set environment variables for your notebook
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '<path to json file>'
```

3. Import Google cloud client and initiate BigQuery service

```python
#Imports google cloud client library and initiates BQ service
from google.cloud import bigquery
bigquery_client = bigquery.Client()
```

4. Specify the query which will be used to import the data from BigQuery

```python
#Write Query on BQ
QUERY = """
SELECT * FROM `fiddler-bq.fiddler_test.churn_prediction_baseline` 
  """
```

5. Read the data using the query and write the data to a pandas dataframe

```python
#Run the query and write result to a pandas data frame
Query_Results = bigquery_client.query(QUERY)
baseline_df = Query_Results.to_dataframe()
```

Now that we have data imported from BigQuery to a jupyter notebook, we can refer to the following notebooks to

1. [Upload baseline data and onboard a model ](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/bigquery/Fiddler-BigQuery%20Integration%20-%20Model%20Registration.ipynb)
2. [Publish production events ](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/bigquery/Fiddler-BigQuery%20Integration%20-%20Event%20Publishing.ipynb)