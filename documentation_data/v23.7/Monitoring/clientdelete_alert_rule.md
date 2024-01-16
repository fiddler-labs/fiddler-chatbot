---
title: "client.delete_alert_rule"
slug: "clientdelete_alert_rule"
excerpt: "To delete an alert rule"
hidden: false
createdAt: "Tue Nov 01 2022 07:31:30 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type | Default | Description                                                |
| :--------------- | :--- | :------ | :--------------------------------------------------------- |
| alert_rule_uuid  | str  | None    | The unique system generated identifier for the alert rule. |

> 📘 Info
> 
> The Fiddler client can be used to get a list of triggered alerts for given alert rule and time duration.

```python Usage

client.delete_alert_rule(
    alert_rule_uuid = "588744b2-5757-4ae9-9849-1f4e076a58de",
)
```

| Return Type | Description |
| :---------- | :---------- |
| None        |             |
