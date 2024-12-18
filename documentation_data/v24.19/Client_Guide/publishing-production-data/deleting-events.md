# Deleting Events

Fiddler supports deleting previously published production events. 
Starting from the 24.19 release, this capability is only available via the REST API on [events DELETE](../../api-integration/api_guidelines/events.md) endpoint.
**Note:** This action is irreversible.

Set `update_metrics=True` to indicate existing metrics should be re-computed. Otherwise, only the raw events will be deleted, and the existing monitoring metrics will continue to reflect the deleted events.

There are two methods to identify the events for deletion:
- **Delete by time range**: Passing in the range start time and range end time(`event timestamp` i.e. [model](../../Python_Client_3-x/api-methods-30.md#model).`event_ts_col`)
  - All events that fall into the specified time range are deleted. `update_metrics` can be configured either to `True` or `False`. The most common use case is recall events published by mistake; in this case, set `update_metrics=True` to recompute the monitoring metrics for accuracy.
- **Delete specific events**: passing in the list of event identifiers(`event_ids`, i.e. [model](../../Python_Client_3-x/api-methods-30.md#model).`event_id_col`))
  - All events matching the passed event_ids are deleted. `update_metrics=False` is enforced. The monitoring metrics won't be recomputed. The most common use case is for compliance concern.
You can specify either one of the modes by passing the corresponding parameters in the request, but not both at the same time. 


**Usage params**

| Parameter      | Type            | Default | Description                                                                                                                                             |
|----------------|-----------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| model_id       | UUID            | -       | Unique identifier for the model from which production events are deleted.                                                                               |
| time_range     | Optional\[dict] | -       | A dictionary with `start_time`(inclusive) and `end_time`(exclusive), indicating the range of events to be deleted. (i.e. `start_time` ≤ t < `end_time`) |
| event_ids      | Optional\[list] | -       | List of event_ids to be deleted.                                                                                                                        |
| update_metrics | Optional\[bool] | False   | Determines if the monitoring metrics are updated following the deletion.                                                                                                   |


***

### Example: Deleting Events by Time Range


```python
import requests
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
data = {'model_id': model.id,
        'time_range':{
            'start_time':'2024-09-27 17:00:00',
            'end_time':'2024-09-27 17:30:00',
            },
        'update_metrics':True,
        }
response = requests.delete(
    url=f'{url}/v3/events',
    headers=headers,
    json=data,
)

```


### Example: Deleting Events by Event IDs

```python
import requests
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
data = {
         'model_id': model.id,
         'event_ids': ['event_id1', 'event_id2'],
         'update_metrics':False,
      }
response = requests.delete(
  url=f'{url}/v3/events',
  headers=headers,
  json=data,
)

```

Refer to our [REST API documentation](../../api-integration/api_guidelines/events.md) for more details.

> 📘 Please delete events with caution when `update_metrics=True`. We recommend not deleting events while there is an ongoing publish or update operation within the same data range.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}
