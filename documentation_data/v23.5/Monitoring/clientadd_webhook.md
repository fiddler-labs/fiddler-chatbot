---
title: "client.add_webhook"
slug: "clientadd_webhook"
excerpt: "To create a webhook."
hidden: false
createdAt: "2023-09-19T10:08:44.356Z"
updatedAt: "2023-10-24T04:14:06.830Z"
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