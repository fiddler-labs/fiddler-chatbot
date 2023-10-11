---
title: "Monitoring"
slug: "monitoring"
hidden: false
createdAt: "2022-04-19T20:24:28.175Z"
updatedAt: "2022-06-13T19:49:28.474Z"
---
Fiddler Monitoring helps you identify issues with the performance of your ML models after deployment. Fiddler Monitoring has five main features:

1. **Data Drift**
2. **Performance**
3. **Data Integrity**
4. **Service Metrics**
5. **Alerts**
[block:api-header]
{
  "title": "Integrate with Fiddler Monitoring"
}
[/block]
Integrating Fiddler monitoring is a four step process:

1. **Upload dataset**

	Fiddler needs a dataset to be used as a baseline for monitoring. A dataset can be uploaded to Fiddler using our UI and Python package. For more information, see:

	* [client.upload_dataset()](ref:clientupload_dataset) 

2. **Register model**

	Fiddler needs some specifications about your model in order to help you troubleshoot production issues. Fiddler supports a wide variety of model formats. For more information, see:

	* [client.register_model()](ref:clientregister_model) 

3. **Configure monitoring for this model**

	You will need to configure bins and alerts for your model. These will be discussed in details below.

4. **Send traffic from your live deployed model to Fiddler**

	Use the Fiddler SDK to send us traffic from your live deployed model.
[block:api-header]
{
  "title": "Publish events to Fiddler"
}
[/block]
In order to send traffic to Fiddler, use the [`publish_event`](https://api.fiddler.ai/#client-publish_event) API from the Fiddler SDK. Here is a sample of the API call:

[block:code]
{
  "codes": [
    {
      "code": "import fiddler as fdl\n\tfiddler_api = fdl.FiddlerApi(url=url, org_id=org_id, auth_token=token)\n\t# Publish an event\n\tfiddler_api.publish_event(\n\t\tproject_id='bank_churn',\n\t\tmodel_id='bank_churn',\n\t\tevent={\n\t\t\t\"CreditScore\": 650,      # data type: int\n\t\t\t\"Geography\": \"France\",   # data type: category\n\t\t\t\"Gender\": \"Female\",\n\t\t\t\"Age\": 45,\n\t\t\t\"Tenure\": 2,\n\t\t\t\"Balance\": 10000.0,      # data type: float\n\t\t\t\"NumOfProducts\": 1,\n\t\t\t\"HasCrCard\": \"Yes\",\n\t\t\t\"isActiveMember\": \"Yes\",\n\t\t\t\"EstimatedSalary\": 120000,\n\t\t\t\"probability_churned\": 0.105\n\t\t},\n\t\tevent_id=’some_unique_id’, #optional\n\t\tupdate_event=False, #optional\n\t\tevent_timestamp=1511253040519 #optional\n\t)",
      "language": "python",
      "name": "Publish Event"
    }
  ]
}
[/block]
The `publish_event` API can be called in real-time right after your model inference. 
[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "You can also publish events as part of a batch call after the fact using the `publish_events_batch` API (click [here](https://api.fiddler.ai/#client-publish_events_batch) for more information). In this case, you will need to send Fiddler the original event timestamps as to accurately populate the time series charts."
}
[/block]
Following is a description of all the parameters for `publish_event`:

* `project_id`: Project ID for the project this event belongs to.
* `model_id`: Model ID for the model this event belongs to.
* `event`: The actual event as an array. The event can contain:

	* inputs
	* outputs
	* target
	* decisions (categorical only)
	* metadata

* `event_id`: A user-generated unique event ID that Fiddler can use to join inputs/outputs to targets/decisions/metadata sent later as an update.
* `update_event`: A flag indicating if the event is a new event (insertion) or an update to an existing event. When updating an existing event, it's required that the user sends an `event_id`.
* `event_timestamp`: The timestamp at which the event (or update) occurred, represented as a UTC timestamp in milliseconds. When updating an existing event, use the time of the update, i.e., the time the target/decision were generated and not when the model predictions were made.
[block:api-header]
{
  "title": "Updating events"
}
[/block]
Fiddler supports partial updates of events for **decision**, **metadata**, and **target** columns. This can be useful when you don’t have access to all this data at the time the model's prediction is made. Inputs and outputs can only be sent at insertion time (with `update_event=False`).

Set `update_event=True` to indicate that you are updating an existing event. You only need to provide the decision, metadata, and/or target fields that you want to change—any fields you leave out will remain as they were before the update.

**Example**

Here’s an example of using the publish event API to update an existing event:

[block:code]
{
  "codes": [
    {
      "code": "import fiddler as fdl\n\nfiddler_api = fdl.FiddlerApi(\n\turl=url,\n\torg_id=org_id,\n\tauth_token=token\n)\n\nfiddler_api.publish_event(\n\tproject_id='bank_churn',\n\tmodel_id='bank_churn',\n\tevent = {\n\t\t'LoanStatus': 'Approved',    # data type: category\n\t\t'ModelDecision': 'Approved', # data type: category\n\t},\n\tevent_id=’some_unique_id’, #optional\n\tupdate_event=True, #optional\n\tevent_timestamp=1511253040519 #optional\n)",
      "language": "python",
      "name": "Update Existing Event"
    }
  ]
}
[/block]
The above `publish_event` call will tell Fiddler to add a target (`LoanStatus=Approved`) and a decision (`ModelDecision=Approved`) to an existing event  (`event_id=’some_unique_id’`).

Once you’ve used the SDK to send Fiddler your live event data, that data will show up under the **Monitor** tab in the Fiddler UI:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/978d0c7-Monitor_dashboard.png",
        "Monitor_dashboard.png",
        3164,
        1526,
        "#fbfcfd"
      ]
    }
  ]
}
[/block]
**Reference**

* See our article on [*The Rise of MLOps Monitoring*](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*