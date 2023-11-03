---
title: "client.update_webhook"
slug: "clientupdate_webhook"
excerpt: "To update a webhook, by changing name, url or provider."
hidden: false
createdAt: "2023-09-19T20:47:55.714Z"
updatedAt: "2023-10-24T04:14:06.836Z"
---
| Input Parameters | Type | Default | Description                                                                   |
| :--------------- | :--- | :------ | :---------------------------------------------------------------------------- |
| name             | str  | None    | A unique name for the webhook.                                                |
| url              | str  | None    | The webhook url used for sending notification messages.                       |
| provider         | str  | None    | The platform that provides webhooks functionality. Only ‘SLACK’ is supported. |
| uuid             | str  | None    | The unique system generated identifier for the webook.                        |

```python Usage
client.update_webhook(uuid='e20bf4cc-d2cf-4540-baef-d96913b14f1b',
                      name='drift_violation',
                      url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
                      provider='SLACK')
```

| Return Type                   | Description                            |
| :---------------------------- | :------------------------------------- |
| [fdl.Webhook](ref:fdlwebhook) | Details of Webhook after modification. |

Example Response:

```Text Response
Webhook(uuid='e20bf4cc-d2cf-4540-baef-d96913b14f1b',
        name='drift_violation', organization_name='some_org_name',
        url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d',
        provider='SLACK')
```