---
title: "fdl.Webhook"
slug: "fdlwebhook"
excerpt: "Represents the Webhook Config."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Thu Sep 21 2023 12:48:43 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter   | Type | Default | Description                                                                   |
| :---------------- | :--- | :------ | :---------------------------------------------------------------------------- |
| name              | str  | None    | A unique name for the webhook.                                                |
| url               | str  | None    | The webhook url used for sending notification messages.                       |
| provider          | str  | None    | The platform that provides webhooks functionality. Only ‘SLACK’ is supported. |
| uuid              | str  | None    | A unique identifier for the webhook.                                          |
| organization_name | str  | None    | The name of the organization in which the webhook is created.                 |

```python Usage
webhook = fdl.Webhook(
    name='data_integrity_violations_channel',
    url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
    provider='SLACK',
  	uuid='74a4fdcf-34eb-4dc3-9a79-e48e14cca686',
    organization_name='some_org',
)
```

Example Response:

```python Response
Webhook(name='data_integrity_violations_channel',
    url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
    provider='SLACK',
  	uuid='74a4fdcf-34eb-4dc3-9a79-e48e14cca686',
    organization_name='some_org',
)
```