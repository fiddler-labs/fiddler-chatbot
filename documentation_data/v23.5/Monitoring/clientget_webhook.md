---
title: "client.get_webhook"
slug: "clientget_webhook"
excerpt: "To get details of a webhook."
hidden: false
createdAt: "2023-09-19T10:58:51.958Z"
updatedAt: "2023-10-24T04:14:06.837Z"
---
| Input Parameters | Type | Default | Description                                            |
| :--------------- | :--- | :------ | :----------------------------------------------------- |
| uuid             | str  | None    | The unique system generated identifier for the webook. |

```python Usage

client.get_webhook(
    alert_rule_uuid = "a5f085bc-6772-4eff-813a-bfc20ff71002",
)
```

| Return Type                   | Description         |
| :---------------------------- | :------------------ |
| [fdl.Webhook](ref:fdlwebhook) | Details of Webhook. |

Example responses:

```python Response
Webhook(uuid='a5f085bc-6772-4eff-813a-bfc20ff71002',
        name='binary_classification_alerts_channel',
        organization_name='some_org',
        url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d,
        provider='SLACK')
```