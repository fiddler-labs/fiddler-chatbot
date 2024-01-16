---
title: "client.add_webhook"
slug: "clientadd_webhook"
excerpt: "To create a webhook."
hidden: false
createdAt: "Tue Sep 19 2023 10:08:44 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type | Default | Description                                                                   |
| :--------------- | :--- | :------ | :---------------------------------------------------------------------------- |
| name             | str  | None    | A unique name for the webhook.                                                |
| url              | str  | None    | The webhook url used for sending notification messages.                       |
| provider         | str  | None    | The platform that provides webhooks functionality. Only ‘SLACK’ is supported. |

```python Usage

client.add_webhook(
        name='range_violation_channel',
        url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
        provider='SLACK')
)
```

| Return Type                   | Description                     |
| :---------------------------- | :------------------------------ |
| [fdl.Webhook](ref:fdlwebhook) | Details of the webhook created. |

Example responses:

```python Response
Webhook(uuid='df2397d3-23a8-4eb3-987a-2fe43b758b08',
        name='range_violation_channel', organization_name='some_org_name',
        url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
        provider='SLACK')
```
