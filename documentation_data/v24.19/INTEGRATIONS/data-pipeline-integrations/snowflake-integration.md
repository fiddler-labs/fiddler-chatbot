---
title: "Snowflake Integration"
slug: "snowflake-integration"
excerpt: ""
hidden: false
createdAt: "Wed Jun 22 2022 14:51:45 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Using Fiddler on your ML data stored in Snowflake

In this article, we will be looking at loading data from Snowflake tables and using the data for the following tasks-

1. Uploading baseline data to Fiddler
2. Onboarding a model to Fiddler and creating a surrogate
3. Publishing production data to Fiddler

### Import data from Snowflake

In order to import data from Snowflake to Jupyter notebook, we will use the snowflake library, this can be installed using the following command in your Python environment.

```python
pip install snowflake-connector-python
```

Once the library is installed, we would require the following to establish a connection to Snowflake

- Snowflake Warehouse
- Snowflake Role
- Snowflake Account
- Snowflake User
- Snowflake Password

These can be obtained from your Snowflake account under the ‘Admin’ option in the Menu as shown below or by running the queries -

- Warehouse - select CURRENT_WAREHOUSE()
- Role - select CURRENT_ROLE()
- Account - select CURRENT_ACCOUNT()

'User' and 'Password' are the same as one used for logging into your Snowflake account.

![](../../.gitbook/assets/c2f4cf4-Screen_Shot_2022-06-14_at_4.17.36_PM.png "Screen Shot 2022-06-14 at 4.17.36 PM.png")

Once you have this information, you can set up a Snowflake connector using the following code -

```python
# establish Snowflake connection
connection = connector.connect(
  user=snowflake_username,
  password=snowflake_password,
  account=snowflake_account,
  role=snowflake_role,
  warehouse=snowflake_warehouse
)
```

You can then write a custom SQL query and import the data to a pandas dataframe.

```python
# sample SQL query
sql_query = 'select * from FIDDLER.FIDDLER_SCHEMA.CHURN_BASELINE LIMIT 100'

# create cursor object
cursor = connection.cursor()

# execute SQL query inside Snowflake
cursor.execute(sql_query)

baseline_df = cursor.fetch_pandas_all()
```

### Publish Production Events

In order to publish production events from Snowflake, we can load the data to a pandas dataframe and publish it to fiddler using _fdl.Model.publish_ api.

Now that we have data imported from Snowflake to a jupyter notebook, we can refer to the following notebooks to

- [Upload baseline data and onboard a model](../../Client_Guide/creating-a-baseline-dataset.md)
- [Publish production events](../../Client_Guide/publishing-production-data/publishing-batches-of-events.md)
