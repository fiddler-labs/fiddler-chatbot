---
title: "client.get_webhook"
slug: "clientget_webhook"
excerpt: "To get details of a webhook."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Sep 19 2023 10:58:51 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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