---
title: Customizing Your Model Schema
slug: customizing-your-model-schema
excerpt: ''
createdAt: Mon May 23 2022 16:36:05 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 21:05:55 GMT+0000 (Coordinated Universal Time)
---

# Customizing your Model Schema

There can be occasions when the `fdl.ModelSchema` object generated by `fdl.Model.from_data` infers a column's data type **differently than the type intended** by the model developer. In these cases you can modify the ModelSchema columns as needed prior to creating the model in Fiddler.

Let's walk through an example of how to do this.

***

Suppose you've loaded in a dataset as a pandas DataFrame.

```python
import pandas as pd

df = pd.read_csv('example_dataset.csv')
```

Below is an example of what is displayed upon inspection.

![](../.gitbook/assets/3ffd956-example\_df\_1.png)

***

You then create a `fdl.Model` object by inferring the column schema details from this DataFrame.

```python
model = fdl.Model.from_data(
  name='my_model',
  project_id=PROJECT_ID,
  source=df
)
```

Below is an example of what is displayed upon inspection of `model.schema`.

![](../.gitbook/assets/8be7229-Screen\_Shot\_2024-04-22\_at\_2.26.13\_PM.png)

```json
```

Upon inspection you may notice that **a few things are off**:

1. The [value range](customizing-your-model-schema.md#modifying-a-columns-value-range) of `output_column` is set to `[0.01, 0.99]`, when it should really be `[0.0, 1.0]`.
2. There are no [possible values](customizing-your-model-schema.md#modifying-a-columns-possible-values) set for `feature_3`.
3. The [data type](customizing-your-model-schema.md#modifying-a-columns-data-type) of `feature_3` is set to [`fdl.DataType.STRING`](../Python\_Client\_3-x/api-methods-30.md#datatype), when it should really be [`fdl.DataType.CATEGORY`](../Python\_Client\_3-x/api-methods-30.md#datatype).

What's the downside of not making sure that ranges and categories are reviewed and properly set? A production traffic event that encodes a number outside of the specified value range or a category value that is not in the set of valid category values will further down the line be flagged as a so-called Data Integrity violation. Depending on the alerting config, this may result in an alert. It's also worth noting however that an event which has a violation in its columns is still processed, and metrics that can be generated are still generated.

The below examples demonstrate how to address each of the issues noted:

### Modifying a Column’s Value Range

Let's say we want to modify the range of `output_column` in the above `fdl.Model` object to be `[0.0, 1.0]`.

You can do this by setting the `min` and `max` of the `output_column` column.

```python
model.schema['output_column'].min = 0.0
model.schema['output_column'].max = 1.0
```

### Modifying a Column’s Possible Values

Let's say we want to modify the possible values of `feature_3` to be `['Yes', 'No']`.

You can do this by setting the `categories` of the `feature_3` column.

```python
model.schema['feature_3'].categories = ['Yes', 'No']
```

### Modifying a Column’s Data Type

Let's say we want to modify the data type of `feature_3` to be [`fdl.DataType.CATEGORY`](../Python\_Client\_3-x/api-methods-30.md#datatype).

You can do this by setting the `data_type` of the `feature_3` column.

```python
model.schema['feature_3'].data_type = fdl.DataType.CATEGORY
```

**Note**: when converting a column to a CATEGORY, you must also set the the list of unique possible values:

```python
model.schema['feature_3'].categories = ['Yes', 'No']
```

**Note**: if converting a column from numeric (integer or float) to a category, you must also remove the min/max numeric range values that were automatically calculated from the sample data.

```python
model.schema['output_column'].min = None
model.schema['output_column'].max = None
```

A complete example might look like this:

```python
sample_data_df = pd.read_csv('some.csv')

# configure your ModelSpec here
# model_spec = ...

# configure your ModelTask here, or use NOT_SET
# model_task = ...

# Infer your model's schema from a sample of data
ml_model = fdl.Model.from_data(
  source=sample_data_df,
  name=MODEL_NAME,
  version=VERSION_NAME,
  project_id=project.id,
  spec=model_spec,
  task=model_task
)

# Make any adjustmens to the inferred ModelSchema BEFORE creating the model
ml_model.schema['feature_3'].data_type = fdl.DataType.CATEGORY
ml_model.schema['feature_3'].categories = ['0', '1']

# The original datatype was inferred as an integer, but we preferred a category.
# Clear out the min and max values derived from the sample data as it does not apply to categories
ml_model.schema['output_column'].min = None
ml_model.schema['output_column'].max = None

# Now create the model with the inferred schema and your overrides
ml_model.create()
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}
