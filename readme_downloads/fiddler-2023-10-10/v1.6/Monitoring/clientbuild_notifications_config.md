---
title: "client.build_notifications_config"
slug: "clientbuild_notifications_config"
excerpt: "To build notification configuration to be used while creating alert rules."
hidden: false
createdAt: "2022-11-01T07:37:44.381Z"
updatedAt: "2022-11-01T07:38:00.974Z"
---
| Input Parameters   | Type          | Default | Description                                    |
| :----------------- | :------------ | :------ | :--------------------------------------------- |
| emails             | Optional[str] | None    | Comma separated emails list                    |
| pagerduty_services | Optional[str] | None    | Comma separated pagerduty services list        |
| pagerduty_severity | Optional[str] | None    | Severity for the alerts triggered by pagerduty |

> 📘 Info
> 
> The Fiddler client  can be used to build notification configuration to be used while creating alert rules.

```python Usage

notifications_config = client.build_notifications_config(
    emails = "name@abc.com",
)

```
```Text Usage with pagerduty
notifications_config = client.build_notifications_config(
  emails = "name1@abc.com,name2@email.com",
  pagetduty_services = 'pd_service_1',
  pagerduty_severity = 'critical'
)

```



| Return Type                 | Description                                                                                   |
| :-------------------------- | :-------------------------------------------------------------------------------------------- |
| Dict\[str, Dict[str, Any]]: | dict with emails and pagerduty dict. If left unused, will store empty string for these values |