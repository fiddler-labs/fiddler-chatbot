---
title: "client.get_webhooks"
slug: "clientget_webhooks"
excerpt: "To get a list of all webhooks for an organization."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Sep 19 2023 20:02:50 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type          | Default | Description                                 |
| :--------------- | :------------ | :------ | :------------------------------------------ |
| limit            | Optional[int] | 300     | Number of records to be retrieved per page. |
| offset           | Optional[int] | 0       | Pointer to the starting of the page index.  |

```python Usage
response = client.get_webhooks()
```

| Return Type                          | Description                 |
| :----------------------------------- | :-------------------------- |
| List\[[fdl.Webhook](ref:fdlwebhook)] | A List containing webhooks. |

Example Response

```python Response
[
  Webhook(uuid='e20bf4cc-d2cf-4540-baef-d96913b14f1b', name='model_1_alerts', organization_name='some_org', url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d', provider='SLACK'),
 	Webhook(uuid='bd4d02d7-d1da-44d7-b194-272b4351cff7', name='drift_alerts_channel', organization_name='some_org', url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d', provider='SLACK'),
 	Webhook(uuid='761da93b-bde2-4c1f-bb17-bae501abd511', name='project_1_alerts', organization_name='some_org', url='https://hooks.slack.com/services/T9EAVLUQ5/P982J/G8ISUczk37hxQ15C28d', provider='SLACK')
]
```