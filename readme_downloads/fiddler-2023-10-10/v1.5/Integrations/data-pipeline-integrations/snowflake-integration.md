---
title: "Snowflake Integration"
slug: "snowflake-integration"
hidden: false
createdAt: "2022-06-22T14:51:45.373Z"
updatedAt: "2022-06-22T14:51:45.373Z"
---
## Using Fiddler on your ML data stored in Snowflake

In this article, we will be looking at loading data from Snowflake tables and using the data for the following tasks-
1. Uploading baseline data to Fiddler
2. Registering a surrogate model to Fiddler
3. Publishing production data to Fiddler

### Import data from Snowflake

In order to import data from Snowflake to Jupyter notebook, we will use the snowflake library, this can be installed using the following command in your Python environment.

[block:code]
{
  "codes": [
    {
      "code": "pip install snowflake-connector-python",
      "language": "python"
    }
  ]
}
[/block]
Once the library is installed, we would require the following to establish a connection to Snowflake
  * Snowflake Warehouse
  * Snowflake Role
  * Snowflake Account
  * Snowflake User
  * Snowflake Password

These can be obtained from your Snowflake account under the ‘Admin’ option in the Menu as shown below or by running the queries - 
  * Warehouse - select CURRENT_WAREHOUSE()
  * Role - select CURRENT_ROLE()
  * Account - select CURRENT_ACCOUNT()

'User' and 'Password' are the same as one used for logging into your Snowflake account.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c2f4cf4-Screen_Shot_2022-06-14_at_4.17.36_PM.png",
        "Screen Shot 2022-06-14 at 4.17.36 PM.png",
        1873,
        653,
        "#faf7f7"
      ]
    }
  ]
}
[/block]
Once you have this information, you can set up a Snowflake connector using the following code -
[block:code]
{
  "codes": [
    {
      "code": "# establish Snowflake connection\nconnection = connector.connect(user=snowflake_username, \n                               password=snowflake_password, \n                               account=snowflake_account, \n                               role=snowflake_role, \n                               warehouse=snowflake_warehouse\n                              )",
      "language": "python"
    }
  ]
}
[/block]
You can then write a custom SQL query and import the data to a pandas dataframe.
[block:code]
{
  "codes": [
    {
      "code": "# sample SQL query\nsql_query = 'select * from FIDDLER.FIDDLER_SCHEMA.CHURN_BASELINE LIMIT 100'\n\n# create cursor object\ncursor = connection.cursor()\n\n# execute SQL query inside Snowflake\ncursor.execute(sql_query)\n\nbaseline_df = cursor.fetch_pandas_all()",
      "language": "python"
    }
  ]
}
[/block]
### Publish Production Events
In order to publish production events from Snowflake, we can load the data to a pandas dataframe and publish it to fiddler using *client.publish_events_batch* api.

Now that we have data imported from Snowflake to a jupyter notebook, we can refer to the following notebooks to
  * [Upload baseline data and register model ](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/snowflake/Fiddler-Snowflake%20Integration%20-%20Model%20Registration.ipynb)
  * [Publish production events](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/snowflake/Fiddler-Snowflake%20Integration%20-%20Event%20Publishing.ipynb)