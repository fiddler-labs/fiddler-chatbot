---
title: "client.get_triggered_alerts"
slug: "clientget_triggered_alerts"
excerpt: "To get a list of all triggered alerts for given alert rule and time period"
hidden: false
createdAt: "2022-11-01T07:26:54.379Z"
updatedAt: "2023-04-18T08:03:48.784Z"
---
| Input Parameters | Type                 | Default    | Description                                                                                                       |
| :--------------- | :------------------- | :--------- | :---------------------------------------------------------------------------------------------------------------- |
| alert_rule_uuid  | str                  | None       | The unique system generated identifier for the alert rule.                                                        |
| start_time       | Optional[datetime]   | 7 days ago | Start time to filter trigger alerts in yyyy-MM-dd format, inclusive.                                              |
| end_time         | Optional[datetime]   | today      | End time to filter trigger alerts in yyyy-MM-dd format, inclusive.                                                |
| offset           | Optional[int]        | None       | Pointer to the starting of the page index                                                                         |
| limit            | Optional[int]        | None       | Number of records to be retrieved per page, also referred as page_size                                            |
| ordering         | Optional\[List[str]] | None       | List of Alert Rule fields to order by. Eg. [‘alert_time_bucket’] or [‘- alert_time_bucket’] for descending order. |

> 📘 Info
> 
> The Fiddler client can be used to get a list of triggered alerts for given alert rule and time duration.

```python Usage

trigerred_alerts = client.get_triggered_alerts(
    alert_rule_uuid = "588744b2-5757-4ae9-9849-1f4e076a58de",
    start_time = "2022-05-01",
    end_time = "2022-09-30",
  	ordering = ['alert_time_bucket'], #['-alert_time_bucket'] for descending
    limit= 4, ## to set number of rules to show in one go
    offset = 0, # page offset
)
```



| Return Type           | Description                                                      |
| :-------------------- | :--------------------------------------------------------------- |
| List[TriggeredAlerts] | A List containing TriggeredAlerts objects returned by the query. |