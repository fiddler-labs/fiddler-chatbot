---
title: "Publishing Events With Complex Data Formats"
slug: "publishing-events-with-complex-data-formats"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 20:15:51 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
> 📘 Info
> 
> See [`client.publish_events_batch_schema`](ref:clientpublish_events_batch_schema) for detailed information on function usage.

## Using a mapping to transform event data

Fiddler supports publishing batches of events that are stored in unconventional formats.

These formats include:

- [CSVs with unlabeled columns](#unlabeled-tabular-data)
- [Nested structures (JSON/Avro)](#nested-data-formats)
- [Files with events for multiple models](#publishing-to-multiple-models-from-the-same-file)

To handle complex data formats, Fiddler offers the ability to transform event data prior to ingestion.  
The function [`client.publish_events_batch_schema`](ref:clientpublish_events_batch_schema) accepts a "schema" containing a mapping which will be used to transform production data according to your needs.

Here's an example of what one of these schemas may look like:

```python
publish_schema = {
    "__static": {
        "__project": "example_project",
        "__model": "example_model"
    },
    "__dynamic": {
        "__timestamp": "column0",
        "feature0": "column1",
        "feature1": "column2",
        "feature2": "column3",
        "model_output": "column4",
        "model_target": "column5"
    }
}
```

The above schema allows us to take unlabeled columns (named `column0` through `column4`) and map them to the names that Fiddler expects (specified in [`fdl.ModelInfo`](ref:fdlmodelinfo)).

Some notes about the above schema:

- `__static` fields are hard-coded. They do not reference anything within the structure.
- `__dynamic` fields point to a location within the structure. We can use forward slashes (/) to indicate traversal of the nested structure.
- `__project` refers to the project ID for the project to which we would like to publish events.
- `__model` refers to the model ID for the model to which we would like to publish events.
- `__timestamp` must refer to the timestamp field within the file structure. If it is not specified, you’ll need to include `__default_timestamp` in the `__static` section.
- You can set the default timestamp to the current time by setting `"__default_timestamp": "CURRENT_TIME"` in the `__static` section.

Once you have a schema, you can publish a batch of events using the [`client.publish_events_batch_schema`](ref:clientpublish_events_batch_schema) function:

```python
client.publish_events_batch_schema(
    publish_schema=publish_schema,
    batch_source='example_batch.csv'
)
```

## Unlabeled tabular data

You can use one of these schemas in the case where you have a CSV file with no column headers.  
The mapping will allow you to reference columns by index rather than name.

Suppose we took the above example, except this time the columns had no headers.  
We could use the following schema to map the columns to the necessary names.

```python
publish_schema = {
    "__static": {
        "__project": "example_project",
        "__model": "example_model"
    },
    "__dynamic": {
        "__timestamp": "[0]",
        "feature0": "[1]",
        "feature1": "[2]",
        "feature2": "[3]",
        "model_output": "[4]",
        "model_target": "[5]"
    }
}
```

## Nested data formats

Fiddler supports publishing batches of events that are stored in non-tabular formats.  
For JSON/Avro nested structures, you can provide a mapping dictionary that will extract the fields you want to monitor and flatten them prior to upload.f

Suppose you have some nested data that’s structured as follows.  
Here, `value0` through `value7` are the fields we want to monitor.

```json
{
    "data": {
        "value0": 0,
        "value1": 1,
        "more_data": {
            "value2": 2,
            "value3": 3,
            "even_more_data": [
                {
                    "value4": 4,
                    "value5": 5
                },
                {
                    "value6": 6,
                    "value7": 7
                }
            ]
        }
    }
}
```

For Fiddler to extract these six inputs, we can use the following mapping to flatten the data.

```python
publish_schema = {
    "__static": {
        "__project": "example_project",
        "__model": "example_model",
        "__default_timestamp": "CURRENT_TIME"
    },
    "__dynamic": {
        "value0": "data/value0",
        "value1": "data/value1",
        "value2": "data/more_data/value2",
        "value3": "data/more_data/value3",
        "value4": "data/more_data/even_more_data[0]/value4",
        "value5": "data/more_data/even_more_data[0]/value5",
        "value6": "data/more_data/even_more_data[-1]/value6",
        "value7": "data/more_data/even_more_data[-1]/value7"
    }
}
```

## Using iterators for multiple events stored in the same row

We can also use mappings to extract multiple events contained in a single JSON/Avro row.  
For this, we will look for "iterators" in the row, which are just lists/arrays containing the multiple events we would like to extract.

- `__iterator` fields point to the location of a list of subtrees we would like to iterate over to obtain multiple records. For each tree within the iterator, additional dynamic fields can be specified. Those fields will be joined with the fields outside of the iterator.
  - Note that an `__iterator_key` must be specified for iterators. This should contain the path to the list containing items to be iterated over.

Suppose you have some nested data that’s structured as follows.  
Here, `value0` through `value5` are the fields we want to monitor.

```json
{
    "data": {
        "value0": 0,
        "value1": 1,
        "more_data": [
            {
                "value2": 2,
                "value3": 3,
                "even_more_data": [
                    {
                        "value4": 4,
                        "value5": 5
                    },
                    {
                        "value4": 6,
                        "value5": 7
                    }
                ]
            },
            {
                "value2": 8,
                "value3": 9,
                "even_more_data": [
                    {
                        "value4": 10,
                        "value5": 11
                    },
                    {
                        "value4": 12,
                        "value5": 13
                    }
                ]
            }
        ]
    }
}
```

Notice that we have four records contained within identical subtrees of the structure. Fiddler will perform a join on the values within the subtrees and the values outside of the subtrees.

```python
publish_schema = {
    "__static": {
        "__project": "example_project",
        "__model": "example_model",
        "__default_timestamp": "CURRENT_TIME"
    },
    "__dynamic": {
        "value0": "data/value0",
        "value1": "data/value1"
    },
    "__iterator": {
        "__iterator_key": "more_data",
        "__dynamic": {
            "value2": "value2",
            "value3": "value3"
        },
        "__iterator": {
            "__iterator_key": "even_more_data",
            "__dynamic": {
                "value4": "value4",
                "value5": "value5"
            }
        }
    }
}
```

To clarify, this is the output we will see once the values from above example are flattened.  
Note that the outermost fields have been duplicated across all the records.

![](https://files.readme.io/bba09c8-publish_schema_df.png "publish_schema_df.png")

## Publishing to multiple models from the same file

Fiddler allows you to publish a single file containing events for multiple models using one API call.

To do this, you can include conditional keys in the schema, which can be used to tell Fiddler which project/model to publish to.

Here's an example of what these conditionals looks like within a schema:

```python
publish_schema = {
    "__static": {
        "__default_timestamp": "CURRENT_TIME"
    },
    "__dynamic": {
        "__timestamp": "column0",
        "__project": "column1"
        "__model": "column2",

        "!example_project_1,example_model_1": {
            "feature0": "column3",
            "feature1": "column4",
            "model_output": "column6",
            "model_target": "column7"
        },

        "!example_project_1,example_model_2": {
            "feature0": "column4",
            "feature1": "column5",
            "model_output": "column6",
            "model_target": "column7"
        },

        "!example_project_2,example_model_3": {
            "feature0": "column3",
            "feature1": "column5",
            "model_output": "column6",
            "model_target": "column7"
        }
    }
}
```

In the above schema, we use the `"!example_project_1,example_model_1"` conditional to tell Fiddler to publish the events to the `example_project_1` project and `example_model_1` model, using the schema defined for that conditional.

> 🚧 Note
> 
> In order to use this conditional functionality, you'll need to specify the `__project` and `__model` **outside** of the conditional.
