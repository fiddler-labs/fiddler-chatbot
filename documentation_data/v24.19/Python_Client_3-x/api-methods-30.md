---
title: API Methods
slug: api-methods-30
excerpt: ''
createdAt: Mon Mar 18 2024 13:41:35 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu May 09 2024 15:48:54 GMT+0000 (Coordinated Universal Time)
---

## Alerts

## AlertRule

AlertRule object contains the below fields.

| Parameter           | Type                                                            | Default | Description                                                                                                                                   |
| ------------------- | --------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| id                  | UUID                                                            | -       | Unique identifier of the AlertRule.                                                                                                         |
| name                | str                                                             | -       | Unique name of the AlertRule.                                                                                                                |
| model               | [Model](api-methods-30.md#model)                                | -       | The associated model details.                                                                                                                         |
| project             | [Project](api-methods-30.md#project)                            | -       | The associated project details                                                                                         |
| baseline            | Optional\[[Baseline](api-methods-30.md#baseline)]               | None    | The associated baseline.                                                                                                        |
| segment             | Optional\[[Segment](api-methods-30.md#segment)]                | None    | Details of segment for the alert.                                                                                                             |
| priority            | Union\[str, [Priority](api-methods-30.md#priority)]             | -       | <p>To set the priority for the AlertRule. Select from:<br>1. Priority.LOW<br>2. Priority.MEDIUM<br>3. Priority.HIGH.</p>                     |
| compare\_to         | Union\[str, [CompareTo](api-methods-30.md#compareto)]                                          | -       | <p>Select from the two:<br>1. CompareTo.RAW_VALUE<br>2. CompareTo.TIME_PERIOD</p>                                                             |
| metric\_id          | Union\[str, UUID]                                               | -       | Type of alert metric UUID or string denoting [metric](#alert-metric-id) ID.                                                                                     |
| critical\_threshold | float                                                           | -       | Critical alert is triggered when this value satisfies the condition to the selected metric_id.                                                          |
| condition           | Union\[str, [AlertCondition](api-methods-30.md#alertcondition)] | -       | <p>Select from:<br>1. AlertCondition.LESSER<br>2. AlertCondition.GREATER</p>                                                                  |
| bin\_size           | Union\[str, [BinSize](api-methods-30.md#binsize)]               | -       | Bin size for example fdl.BinSize.HOUR.                                                                                                               |
| columns             | Optional\[List\[str]]                                           | None    | List of 1 or more column names for the rule to evaluate. Use ['\_\_ANY\_\_'] to evaluate all columns.                                 |
| baseline\_id        | Optional\[UUID]                                                 | None    | UUID of the baseline for the alert.                                                                                                           |
| segment\_id         | Optional\[UUID]                                                 | None    | UUID of segment for the alert                                                                                                                 |
| compare\_bin\_delta | Optional\[int]                                                  | None    | Indicates previous period for comparison e.g. for fdl.BinSize.DAY, compare_bin_delta=1 will compare 1 day back, compare_bin_delta=7 will compare 7 days back.                                                                          |
| warning\_threshold  | Optional\[float]                                                | None    | Warning alert is triggered when this value satisfies the condition to the selected metric_id.                                                           |
| created\_at         | datetime                                                        | -       | The creation timestamp.                                                                                                         |
| updated\_at         | datetime                                                        | -       | The timestamp of most recent update.                                                                                                  |
| evaluation\_delay   | int                                                             | 0       | Specifies a delay in hours before AlertRule is evaluated. The delay period must not exceed one year(8760 hours). |

### constructor()

Initialize a new AlertRule on Fiddler Platform.

**Parameters**

| Parameter           | Type                                                            | Default | Description                                                                                                                                   |
| ------------------- | --------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| name                | str                                                             | -       | Unique name of the model                                                                                                                      |
| model\_id           | UUID                                                            | -       | Details of the model.                                                                                                                         |
| metric\_id          | Union\[str, UUID]                                               | -       | Type of alert metric UUID or enum.                                                                                                            |
| columns             | Optional\[List\[str]]                                           | None    | List of column names on which AlertRule is to be created. It can take \['\_\_ANY\_\_'] to check for all columns.                                 |
| baseline\_id        | Optional\[UUID]                                                 | None    | UUID of the baseline for the alert.                                                                                                           |
| segment\_id         | Optional\[UUID]                                                 | None    | UUID of the segment for the alert.                                                                                                            |
| priority            | Union\[str, [Priority](api-methods-30.md#priority)]             | -       | <p>To set the priority for the AlertRule. Select from:<br>1. Priority.LOW<br>2. Priority.MEDIUM<br>3. Priority.HIGH.</p>                     |
| compare\_to         | Union\[str, [CompareTo](api-methods-30.md#compareto)]                                          | -       | <p>Select from the two:<br>1. CompareTo.RAW_VALUE (absolute alert)<br>2. CompareTo.TIME_PERIOD (relative alert)</p>                           |
| compare\_bin\_delta | Optional\[int]                                                  | None    | Compare the metric to a previous time period in units of bin\_size.                                                                           |
| warning\_threshold  | Optional\[float]                                                | None    | Threshold value to crossing which a warning level severity alert will be triggered.                                                           |
| critical\_threshold | float                                                           | -       | Threshold value to crossing which a critical level severity alert will be triggered.                                                          |
| condition           | Union\[str, [AlertCondition](api-methods-30.md#alertcondition)] | -       | <p>Select from:<br>1. AlertCondition.LESSER<br>2. AlertCondition.GREATER</p>                                                                  |
| bin\_size           | Union\[str, [BinSize](api-methods-30.md#binsize)]               | -       | Size of the bin for AlertRule.                                                                                                               |
| evaluation\_delay   | int                                                             | 0       | To introduce a delay in the evaluation of the alert, specifying the duration in hours. The delay period must not exceed one year(8760 hours). |

**Usage**

```python
MODEL_NAME = 'test_model'
PROJECT_NAME = 'test_project'
BASELINE_NAME = 'test_baseline'
SEGMENT_NAME = 'test_segment'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
baseline = fdl.Baseline.from_name(name=BASELINE_NAME, model_id=model.id)
segment = fdl.Segment.from_name(name=SEGMENT_NAME, model_id=model.id)

alert_rule = fdl.AlertRule(
    name='Bank Churn Drift Hawaii Region',
    model_id=model.id,
    baseline_id=baseline.id,
    metric_id='jsd',
    priority=fdl.Priority.HIGH,
    compare_to=fdl.CompareTo.TIME_PERIOD,
    compare_bin_delta=1,
    condition=fdl.AlertCondition.GREATER,
    bin_size=fdl.BinSize.DAY,
    critical_threshold=0.5,
    warning_threshold=0.1,
    columns=['gender', 'creditscore'],
    segment_id=segment.id,
    evaluation_delay=1
)
```

***

### create()

Create a new AlertRule.

**Parameters**

No

**Usage**

```python
MODEL_NAME = 'test_model'
PROJECT_NAME = 'test_project'
BASELINE_NAME = 'test_baseline'
SEGMENT_NAME = 'test_segment'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
baseline = fdl.Baseline.from_name(name=BASELINE_NAME, model_id=model.id)
segment = fdl.Segment.from_name(name=SEGMENT_NAME, model_id=model.id)

alert_rule = fdl.AlertRule(
    name='Bank Churn Drift Hawaii Region',
    model_id=model.id,
    baseline_id=baseline.id,
    metric_id='jsd',
    priority=fdl.Priority.HIGH,
    compare_to=fdl.CompareTo.TIME_PERIOD,
    compare_bin_delta=1,
    condition=fdl.AlertCondition.GREATER,
    bin_size=fdl.BinSize.DAY,
    critical_threshold=0.5,
    warning_threshold=0.1,
    columns=['gender', 'creditscore'],
    segment_id=segment.id,
    evaluation_delay=1
).create()
```

**Returns**

| Return Type                               | Description          |
| ----------------------------------------- | -------------------- |
| [AlertRule](api-methods-30.md#alert-rule) | AlertRule instance. |

### get()

Get a single AlertRule.

**Parameters**

| Parameter | Type | Default | Description                           |
| --------- | ---- | ------- | ------------------------------------- |
| id\_      | UUID | -       | Unique identifier for the AlertRule. |

**Usage**

```python
ALERT_RULE_ID='ed8f18e6-c319-4374-8884-71126a6bab85'

alert = fdl.AlertRule.get(id_=ALERT_RULE_ID)
```

**Returns**

| Return Type                               | Description          |
| ----------------------------------------- | -------------------- |
| [AlertRule](api-methods-30.md#alert-rule) | AlertRule instance. |

**Raises**

| Error code | Issue                                                               |
| ---------- | ------------------------------------------------------------------- |
| NotFound   | AlertRule with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of AlertRule. |

***

### list()

Get a list of AlertRules .

**Parameters**

| Parameter    | Type                  | Default | Description                                                                                                             |
| ------------ | --------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| model\_id    | Union\[str, UUID]     | None    | Unique identifier for the model to which AlertRule belongs.                                                            |
| project\_id  | Optional\[UUID]       | None    | Unique identifier for the project to which AlertRule belongs                                                           |
| metric\_id   | Optional\[UUID]       | None    | Type of alert metric UUID or enum.                                                                                      |
| columns      | Optional\[List\[str]] | None    | List of column names on which AlertRule is to be created. It can take \['**ANY**'] to check for all columns.           |
| baseline\_id | Optional\[UUID]       | None    | UUID of the baseline for the AlertRule.                                                                                     |
| ordering     | Optional\[List\[str]] | None    | List of AlertRule fields to order by. Eg. \[‘alert\_time\_bucket’] or \[‘- alert\_time\_bucket’] for descending order. |

**Usage**

```python
MODEL_ID = '299c7b40-b87c-4dad-bb94-251dbcd3cbdf'

alerts = fdl.AlertRule.list(model_id=MODEL_ID)
```

**Returns**

| Return Type                                                 | Description                       |
| ----------------------------------------------------------- | --------------------------------- |
| Iterator\[[AlertRule](api-methods-30.md#alertrule)] | Iterator of AlertRule instances. |

***

### delete()

Delete an existing AlertRule.

**Parameters**

| Parameter | Type | Default | Description                     |
| --------- | ---- | ------- | ------------------------------- |
| id\_      | UUID | -       | Unique UUID of the AlertRule . |

**Usage**

```python
MODEL_ID = '299c7b40-b87c-4dad-bb94-251dbcd3cbdf'
ALERT_RULE_NAME = 'Testing Alert API'

alert_rules = fdl.AlertRule.list(model_id=MODEL_ID)

for alert_rule in alert_rules:
    if alert_rule.name == ALERT_RULE_NAME:
        alert_rule.delete()
        break
```

**Returns**

No

**Raises**

| Error code | Issue                                                               |
| ---------- | ------------------------------------------------------------------- |
| NotFound   | AlertRule with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of AlertRule. |

***

### enable\_notifications()

Enable an AlertRule's notification.

**Parameters**

| Parameter | Type | Default | Description                     |
| --------- | ---- | ------- | ------------------------------- |
| id\_      | UUID | -       | Unique UUID of the AlertRule . |

**Usage**

```python
ALERT_NAME = "YOUR_ALERT_NAME"
MODEL_ID = '299c7b40-b87c-4dad-bb94-251dbcd3cbdf'

alerts_list = fdl.AlertRule.list(model_id=MODEL_ID)
for alert_rule in alerts_list:
    if ALERT_NAME == alert.name:
        alert_rule.enable_notifications()
        break
```

**Returns**

None

**Raises**

| Error code | Issue                                                               |
| ---------- | ------------------------------------------------------------------- |
| NotFound   | AlertRule with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of AlertRule. |

***

### disable\_notifications()

Disable notifications for an AlertRule.

**Parameters**

| Parameter | Type | Default | Description                     |
| --------- | ---- | ------- | ------------------------------- |
| id\_      | UUID | -       | Unique UUID of the AlertRule . |

**Usage**

```python
ALERT_NAME = "YOUR_ALERT_NAME"
MODEL_ID = '299c7b40-b87c-4dad-bb94-251dbcd3cbdf'

alerts_list = fdl.AlertRule.list(model_id=MODEL_ID)
for alert_rule in alerts_list:
    if ALERT_NAME == alert.name:
        alert_rule.disable_notifications()
```

**Returns**

None

**Raises**

| Error code | Issue                                                               |
| ---------- | ------------------------------------------------------------------- |
| NotFound   | AlertRule with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of AlertRule. |

***

## Alert Notifications

Alert notifications for an AlertRule.

| Parameter           | Type                   | Default | Description                                                |
| ------------------- | ---------------------- | ------- | ---------------------------------------------------------- |
| emails              | Optional\[List\[str]]  | None    | List of emails to send notification to.                    |
| PagerDuty\_services | Optional\[List\[str]]  | None    | List of PagerDuty services to trigger the alert to.        |
| PagerDuty\_severity | Optional\[str]         | None    | Severity of PagerDuty.                                     |
| webhooks            | Optional\[List\[UUID]] | None    | List of [webhook](api-methods-30.md#webhook-object) UUIDs. |

### set\_notification\_config()

Set NotificationConfig for an AlertRule.

**Parameters**

| Parameter           | Type                   | Default | Description                                                |
| ------------------- | ---------------------- | ------- | ---------------------------------------------------------- |
| emails              | Optional\[List\[str]]  | None    | List of emails to send notification to.                    |
| PagerDuty\_services | Optional\[List\[str]]  | None    | List of PagerDuty services to trigger the alert to.        |
| PagerDuty\_severity | Optional\[str]         | None    | Severity of PagerDuty.                                     |
| webhooks            | Optional\[List\[UUID]] | None    | List of [webhook](api-methods-30.md#webhook-object) UUIDs. |

**Usage**

```python
ALERT_RULE_ID = '72e8835b-cde2-4dd2-a435-a35d4b51196b'
rule = fdl.AlertRule.get(id_=ALERT_RULE_ID)

rule.set_notification_config(
  emails=['abc@xyz.com', 'admin@xyz.com'],
  webhooks=['8b403d99-530a-4c5a-a519-89688d65ddc1'], # Webhook UUID
  PagerDuty_services = ['PagerDuty_service_1','PagerDuty_service_2'], # PagerDuty service names
  PagerDuty_severity = 'critical' # Only applies to PagerDuty, ignored otherwise
)

```

**Returns**

| Return Type                                                | Description                            |
| ---------------------------------------------------------- | -------------------------------------- |
| NotificationConfig                                         | Alert notification settings for an AlertRule. |

> If `PagerDuty_severity` is passed without specifying `PagerDuty_services` then the `PagerDuty_severity` is ignored.

**Raises**

| Error code | Issue                             |
| ---------- | --------------------------------- |
| BadRequest | All 4 input parameters are empty. |
| ValueError | Webhook ID is incorrect.          |

### get\_notification\_config()

Get notification configuration for an AlertRule.

**Parameters**

None

**Usage**

```python
ALERT_RULE_ID = '72e8835b-cde2-4dd2-a435-a35d4b51196b'
rule = fdl.AlertRule.get(id_=ALERT_RULE_ID)

rule.get_notification_config()
```

**Returns**

| Return Type         | Description                            |
| ------------------- | -------------------------------------- |
| NotificationConfig  | Alert notification settings for an AlertRule. |

**Raises**

| Error code | Issue                             |
| ---------- | --------------------------------- |
| BadRequest | All 4 input parameters are empty. |
| ValueError | Webhook ID is incorrect.          |

***

## Triggered Alerts

## AlertRecord

An AlertRecord details an AlertRule's triggered alert.

| Parameter                    | Type             | Default | Description                                                                                                                                     |
| ---------------------------- | ---------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| id                           | UUID             | -       | Unique identifier for the triggered AlertRule.                                                                                                 |
| alert\_rule\_id              | UUID             | -       | Unique identifier for the AlertRule which needs to be triggered.                                                                               |
| alert\_run\_start\_time      | int              | -       | Timestamp of AlertRule evaluation in epoch.                                                                                                    |
| alert\_time\_bucket          | int              | -       | Timestamp pointing to the start of the time bucket in epoch.                                                                                    |
| alert\_value                 | float            | -       | Value of the metric for alert\_time\_bucket.                                                                                                    |
| baseline\_time\_bucket       | Optional\[int]   | None    | Timestamp pointing to the start of the baseline time bucket in epoch, only if AlertRule is of 'time period' based comparison.                  |
| baseline\_value              | Optional\[float] | None    | Value of the metric for baseline\_time\_bucket.                                                                                                 |
| is\_alert                    | bool             | -       | Boolean to indicate if alert was supposed to be triggered.                                                                                      |
| severity                     | str              | -       | Severity of alert represented by [Severity](api-methods-30.md#severity), calculated based on value of metric and AlertRule thresholds. |
| failure\_reason              | str              | -       | String message if there was a failure sending notification.                                                                                     |
| message                      | str              | -       | String message sent as a part of email notification.                                                                                            |
| feature\_name                | Optional\[str]   | None    | Name of feature for which alert was triggered.                                                                                                  |
| alert\_record\_main\_version | int              | -       | Main version of triggered alert record in int, incremented when the value of severity changes.                                                  |
| alert\_record\_sub\_version  | int              | -       | Sub version of triggered alert record in int, incremented when another alert with same severity as before is triggered.                         |
| created\_at                  | datetime         | -       | Time at which trigger AlertRule was created.                                                                                                   |
| updated\_at                  | datetime         | -       | Latest time at which trigger AlertRule was updated.                                                                                            |

### list()

List AlertRecords triggered for an AlertRule.

**Parameters**

| Parameter       | Type                  | Default | Description                                                                                                             |
| --------------- | --------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| alert\_rule\_id | UUID                  | -       | Unique identifier for the AlertRule which needs to be triggered.                                                       |
| start\_time     | Optional\[datetime]   | None    | Start time to filter trigger alerts in yyyy-MM-dd format, inclusive.                                                    |
| end\_time       | Optional\[datetime]   | None    | End time to filter trigger alerts in yyyy-MM-dd format, inclusive.                                                      |
| ordering        | Optional\[List\[str]] | None    | List of AlertRule fields to order by. Eg. \[‘alert\_time\_bucket’] or \[‘- alert\_time\_bucket’] for descending order. |

**Usage**

```python
ALERT_NAME = "YOUR_ALERT_NAME"
MODEL_ID = '299c7b40-b87c-4dad-bb94-251dbcd3cbdf'
triggered_alerts = None

alerts_list = fdl.AlertRule.list(model_id=MODEL_ID)
for alert_rule in alerts_list:
    if ALERT_NAME == alert.name:
        triggered_alerts = fdl.AlertRecord.list(
            alert_rule_id=ALERT_RULE_ID,
            start_time=datetime(2024, 9, 1), # optional
            end_time=datetime(2024, 9, 24), # optional
            ordering = ['alert_time_bucket'], # ['-alert_time_bucket'] for descending sort, optional.
        )
```

**Returns**

| Return Type                                                | Description                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------- |
| Iterator\[[AlertRecord](api-methods-30.md#alertrecord)]    | Iterable of triggered AlertRule instances for an AlertRule. |

***

## Baselines

Baseline datasets are used for making comparisons with production data.

A baseline dataset should be sampled from your model's training set, so it can serve as a representation of what the model expects to see in production.

## Baseline

Baseline object contains the below fields.

| Parameter    | Type                                 | Default | Description                                                                                                                  |
| ------------ | ------------------------------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| id           | UUID                                 | -       | Unique identifier for the baseline.                                                                                          |
| name         | str                                  | -       | Baseline name.                                                                                                               |
| type\_       | [BaselineType](api-methods-30.md#baselinetype) | -       | Baseline type can be static (Pre-production or production) or rolling(production). |
| start\_time  | Optional\[int]                       | None    | Epoch to be used as start time for STATIC baseline.                                                                          |
| end\_time    | Optional\[int]                       | None    | Epoch to be used as end time for STATIC baseline.                                                                            |
| offset       | Optional\[int]                       | None    | Offset in seconds relative to current time to be used for ROLLING baseline.                                                  |
| window\_size | Optional\[int]                       | None    | Span of window in seconds to be used for ROLLING baseline.                                                                   |
| row\_count   | Optional\[int]                       | None    | Number of rows in baseline.                                                                                                  |
| model        | [Model](api-methods-30.md#model)     | -       | Details of the model.                                                                                                        |
| project      | [Project](api-methods-30.md#project) | -       | Details of the project to which the baseline belongs.                                                                        |
| dataset      | [Dataset](api-methods-30.md#dataset) | -       | Details of the dataset from which baseline is derived.                                                                       |
| created\_at  | datetime                             | -       | Time at which baseline was created.                                                                                          |
| updated\_at  | datetime                             | -       | Latest time at which baseline was updated.                                                                                   |

### constructor()

Initialize a new baseline instance.

**Parameters**

| Parameter         | Type                                 | Default | Description                                                                                                                                                       |
| ----------------- | ------------------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name              | str                                  | -       | Unique name of the baseline.                                                                                                                                      |
| model\_id         | UUID                                 | -       | Unique identifier for the model to add baseline to.                                                                                                               |
| environment       | [EnvType](api-methods-30.md#envtype) | -       | Type of environment. Can either be PRE\_PRODUCTION or PRODUCTION.                                                                                                 |
| type\_            | [BaselineType](api-methods-30.md#baselinetype) | -       | Baseline type can be static (pre-production or production) or rolling(production).                                      |
| dataset\_id       | Optional\[UUID]                      | None    | Unique identifier for the dataset on which the baseline is created.                                                                                               |
| start\_time       | Optional\[int]                       | None    | Epoch to be used as start time for STATIC baseline.                                                                                                               |
| end\_time         | Optional\[int]                       | None    | Epoch to be used as end time for STATIC baseline.                                                                                                                 |
| offset\_delta     | Optional\[int]                       | None    | <p>Number of times of <a href="api-methods-30.md#windowbinsize">WindowBinSize</a> to be used for ROLLING baseline.<br>offset = offset_delta * window_bin_size</p> |
| window\_bin\_size | Optional\[str]                       | None    | Span of window in seconds to be used for ROLLING baseline using [WindowBinSize](api-methods-30.md#windowbinsize)                                                  |

**Usage**

```python
BASELINE_NAME = 'YOUR_BASELINE_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

baseline = fdl.Baseline(
        name=BASELINE_NAME,
        model_id=model.id,
        environment=fdl.EnvType.PRE_PRODUCTION,
        dataset_id=dataset.id,
        type_=fdl.BaselineType.STATIC,
    )
```

### create()

Adds a baseline to Fiddler.

**Parameters**

No

**Usage**

```python
BASELINE_NAME = 'YOUR_BASELINE_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

baseline = fdl.Baseline(
        name=BASELINE_NAME,
        model_id=model.id,
        environment=fdl.EnvType.PRE_PRODUCTION,
        dataset_id=dataset.id,
        type_=fdl.BaselineType.STATIC,
    ).create()
```

**Returns**

| Return Type                            | Description        |
| -------------------------------------- | ------------------ |
| [Baseline](api-methods-30.md#baseline) | Baseline instance. |

**Raises**

| Error code | Issue                                                                  |
| ---------- | ---------------------------------------------------------------------- |
| Conflict   | Baseline with same name may exist in project .                         |
| NotFound   | Given dataset may not exist in for the input model.                    |
| ValueError | Validation failures like wrong window size, start\_time, end\_time etc |

### get()

Get baseline from Fiddler Platform based on UUID.

**Parameters**

| Parameter | Type | Default | Description                         |
| --------- | ---- | ------- | ----------------------------------- |
| id\_      | UUID | -       | Unique identifier for the baseline. |

**Usage**

```python
BASELINE_ID = 'af05646f-0cef-4638-84c9-0d195df2575d'
baseline = fdl.Baseline.get(id_=BASELINE_ID)
```

**Returns**

| Return Type                            | Description        |
| -------------------------------------- | ------------------ |
| [Baseline](api-methods-30.md#baseline) | Baseline instance. |

**Raises**

| Error code | Issue                                                             |
| ---------- | ----------------------------------------------------------------- |
| NotFound   | Baseline with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of baseline. |

***

### from\_name()

Get baseline from Fiddler Platform based on name.

**Parameters**

| Parameter | Type        | Default | Description                      |
| --------- | ----------- | ------- | -------------------------------- |
| name      | str         | -       | Name of the baseline.            |
| model\_id | UUID \| str | -       | Unique identifier for the model. |

**Usage**

```python
BASELINE_NAME = 'YOUR_BASELINE_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

baseline = fdl.Baseline.from_name(
    name=BASELINE_NAME,
    model_id=MODEL_ID
)
```

**Returns**

| Return Type                            | Description        |
| -------------------------------------- | ------------------ |
| [Baseline](api-methods-30.md#baseline) | Baseline instance. |

**Raises**

| Error code | Issue                                                             |
| ---------- | ----------------------------------------------------------------- |
| NotFound   | Baseline with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of baseline. |

***

### list()

List all baselines accessible to user.

**Parameters**

| Parameter | Type | Default | Description                                 |
| --------- | ---- | ------- | ------------------------------------------- |
| model\_id | UUID | -       | UUID of the model associated with baseline. |

**Usage**

```python
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'
baselines = fdl.Baseline.list(model_id=MODEL_ID)
```

**Returns**

| Return Type                                       | Description                       |
| ------------------------------------------------- | --------------------------------- |
| Iterable\[[Baseline](api-methods-30.md#baseline)] | Iterable of all baseline objects. |

**Raises**

| Error code | Issue                                                             |
| ---------- | ----------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of baseline. |

***

### delete()

Deletes a baseline.

**Parameters**

| Parameter | Type | Default | Description                   |
| --------- | ---- | ------- | ----------------------------- |
| id\_      | UUID | -       | Unique UUID of the baseline . |

**Usage**

```python
BASELINE_NAME = 'YOUR_BASELINE_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

baseline = fdl.Baseline.from_name(name=BASELINE_NAME, model_id=MODEL_ID)
baseline.delete()
```

**Returns**

None

**Raises**

| Error code | Issue                                                    |
| ---------- | -------------------------------------------------------- |
| NotFound   | Baseline with given identifier not found.                |
| Forbidden  | Current user may not have permission to delete baseline. |

***

## Custom Metrics

User-defined metrics to extend Fiddler's built-in metrics.

## CustomMetric

CustomMetric object contains the below parameters.

| Parameter   | Type           | Default | Description                                                  |
| ----------- | -------------- | ------- | ------------------------------------------------------------ |
| id          | UUID           | -       | Unique identifier for the custom metric.                     |
| name        | str            | -       | Custom metric name.                                          |
| model\_id   | UUID           | -       | UUID of the model in which the custom metric is being added. |
| definition  | str            | -       | Definition of the custom metric.                             |
| description | Optional\[str] | None    | Description of the custom metric.                            |
| created\_at | datetime       | -       | Time of creation of custom metric.                           |

### constructor()

Initialize a new custom metric.

**Parameters**

| Parameter   | Type           | Default | Description                                                  |
| ----------- | -------------- | ------- | ------------------------------------------------------------ |
| name        | str            | -       | Custom metric name.                                          |
| model\_id   | UUID           | -       | UUID of the model in which the custom metric is being added. |
| definition  | str            | -       | Definition of the custom metric.                             |
| description | Optional\[str] | None    | Description of the custom metric.                            |

**Usage**

```python
METRIC_NAME = 'YOUR_CUSTOM_METRIC_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

metric = fdl.CustomMetric(
    name=METRIC_NAME,
    model_id=MODEL_ID,
    definition="average(if(\"spend_amount\">1000, \"spend_amount\", 0))", #Use Fiddler Query Language (FQL) to define your custom metrics
    description='Get average spend for users spending over $1000',
)
```

### get()

Get CustomMetric from Fiddler Platform based on model UUID.

**Parameters**

| Parameter | Type | Default | Description                                           |
| --------- | ---- | ------- | ----------------------------------------------------- |
| model\_id | UUID | -       | UUID of the model associated with the custom metrics. |

**Usage**

```python
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

metrics = fdl.CustomMetric.list(model_id=MODEL_ID)
```

**Returns**

| Return Type                                               | Description                            |
| --------------------------------------------------------- | -------------------------------------- |
| Iterable\[[CustomMetric](api-methods-30.md#custommetric)] | Iterable of all custom metric objects. |

**Raises**

| Error code | Issue                                                                  |
| ---------- | ---------------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of custom metric. |

### from\_name()

Get CustomMetric from Fiddler Platform based on name and model UUID.

**Parameters**

| Parameter | Type        | Default | Description                      |
| --------- | ----------- | ------- | -------------------------------- |
| name      | str         | -       | Name of the custom metric.       |
| model\_id | UUID \| str | -       | Unique identifier for the model. |

**Usage**

```python
METRIC_NAME = 'YOUR_CUSTOM_METRIC_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

metric = fdl.CustomMetric.from_name(
    name=METRIC_NAME,
    model_id=MODEL_ID
)
```

**Returns**

| Return Type                                    | Description             |
| ---------------------------------------------- | ----------------------- |
| [CustomMetric](api-methods-30.md#custommetric) | Custom Metric instance. |

**Raises**

| Error code | Issue                                                                  |
| ---------- | ---------------------------------------------------------------------- |
| NotFound   | Custom metric with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of custom metric. |

### create()

Creates a custom metric for a model on Fiddler Platform.

**Parameters**

None

**Usage**

```python
METRIC_NAME = 'YOUR_CUSTOM_METRIC_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

metric = fdl.CustomMetric(
    name=METRIC_NAME,
    model_id=MODEL_ID,
    definition="average(if(\"spend_amount\">1000, \"spend_amount\", 0))", #Use Fiddler Query Language (FQL) to define your custom metrics
    description='Get average spend for users spending over $1000',
).create()
```

**Returns**

| Return Type                                    | Description             |
| ---------------------------------------------- | ----------------------- |
| [CustomMetric](api-methods-30.md#custommetric) | Custom Metric instance. |

**Raises**

| Error code | Issue                                               |
| ---------- | --------------------------------------------------- |
| Conflict   | Custom metric with same name may exist in project . |
| BadRequest | Invalid definition.                                 |
| NotFound   | Given model may not exist.                          |

### delete()

Delete a custom metric.

**Parameters**

| Parameter | Type | Default | Description                       |
| --------- | ---- | ------- | --------------------------------- |
| id\_      | UUID | -       | Unique UUID of the custom metric. |

**Usage**

```python
METRIC_NAME = 'YOUR_CUSTOM_METRIC_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

metric = fdl.CustomMetric.from_name(name=METRIC_NAME, model_id=MODEL_ID)
metric.delete()
```

**Returns**

No

**Raises**

| Error code | Issue                                                         |
| ---------- | ------------------------------------------------------------- |
| NotFound   | Custom metric with given identifier not found.                |
| Forbidden  | Current user may not have permission to delete custom metric. |

***

## Datasets

Datasets (or baseline datasets) are used for making comparisons with production data.

***

## Dataset

Dataset object contains the below parameters.

| Parameter    | Type                                           | Default | Description                                               |
| ------------ | ---------------------------------------------- | ------- | --------------------------------------------------------- |
| id           | UUID                                           | -       | Unique identifier for the dataset.                        |
| name         | str                                            | -       | Dataset name.                                             |
| row\_count   | int                                            | None    | Number of rows in dataset.                                |
| model_id     | [Model](api-methods-30.md#model)               | -       | Unique identifier of the associated model                 |
| project_id   | [Project](api-methods-30.md#project)           | -       | Unique identifier of the associated project               |

***

### get()

Get dataset from Fiddler Platform based on UUID.

**Parameters**

| Parameter | Type | Default | Description                        |
| --------- | ---- | ------- | ---------------------------------- |
| id\_      | UUID | -       | Unique identifier for the dataset. |

**Usage**

```python
DATASET_ID = 'ba6ec4e4-7188-44c5-ba84-c2cb22b4bb00'
dataset = fdl.Dataset.get(id_=DATASET_ID)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Dataset](api-methods-30.md#dataset) | Dataset instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Dataset with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of dataset. |

***

### from\_name()

Get dataset from Fiddler Platform based on name and model UUID.

**Usage params**

| Parameter | Type        | Default | Description                      |
| --------- | ----------- | ------- | -------------------------------- |
| name      | str         | -       | Name of the dataset.             |
| model\_id | UUID \| str | -       | Unique identifier for the model. |

**Usage**

```python
DATASET_NAME = 'YOUR_DATASET_NAME'
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

dataset = fdl.Dataset.from_name(
    name=DATASET_NAME,
    model_id=MODEL_ID
)

```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Dataset](api-methods-30.md#dataset) | Dataset instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Dataset not found in the given project name.                     |
| Forbidden  | Current user may not have permission to view details of dataset. |

***

### list()

Get a list of all datasets associated to a model.

**Parameters**

| Parameter | Type | Default | Description                                 |
| --------- | ---- | ------- | ------------------------------------------- |
| model\_id | UUID | -       | UUID of the model associated with baseline. |

**Usage**

```python
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'

datasets = fdl.Dataset.list(model_id=MODEL_ID)
```

**Returns**

| Return Type                                     | Description                      |
| ----------------------------------------------- | -------------------------------- |
| Iterable\[[Dataset](api-methods-30.md#dataset)] | Iterable of all dataset objects. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of dataset. |

***

## Jobs

A Job is used to track asynchronous processes such as batch publishing of data.

## Job

Job object contains the below fields.

| Parameter      | Type            | Default | Description                                                          |
| -------------- | --------------- | ------- | -------------------------------------------------------------------- |
| id             | UUID            | -       | Unique identifier for the job.                                       |
| name           | str             | -       | Name of the job.                                                     |
| status         | str             | -       | Current status of job.                                               |
| progress       | float           | -       | Progress of job completion.                                          |
| info           | dict            | -       | Dictionary containing resource\_type, resource\_name, project\_name. |
| error\_message | Optional\[str]  | None    | Message for job failure, if any.                                     |
| error\_reason  | Optional\[str]  | None    | Reason for job failure, if any.                                      |
| extras         | Optional\[dict] | None    | Metadata regarding the job.                                          |

#### get()

Get the job instance using job UUID.

**Parameters**

| Parameter | Type | Default | Description                                              |
| --------- | ---- | ------- | -------------------------------------------------------- |
| id\_      | UUID | -       | Unique UUID of the project to which model is associated. |
| verbose   | bool | False   | Flag to get `extras` metadata about the tasks executed.  |

**Usage**

```python
JOB_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
job = fdl.Job.get(id_=JOB_ID)
```

**Returns**

| Return Type                  | Description                             |
| ---------------------------- | --------------------------------------- |
| [Job](api-methods-30.md#job) | Single job object for the input params. |

**Raises**

| Error code | Issue                                                        |
| ---------- | ------------------------------------------------------------ |
| Forbidden  | Current user may not have permission to view details of job. |

***

### wait()

Wait for job to complete either with success or failure status.

**Parameters**

| Parameter | Type           | Default | Description                                         |
| --------- | -------------- | ------- | --------------------------------------------------- |
| interval  | Optional\[int] | 3       | Interval in seconds between polling for job status. |
| timeout   | Optional\[int] | 1800    | Timeout in seconds for iterator to stop.            |

**Usage**

```python
JOB_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
job = fdl.Job.get(id_=JOB_ID)
job.wait()
```

**Returns**

| Return Type                  | Description                             |
| ---------------------------- | --------------------------------------- |
| [Job](api-methods-30.md#job) | Single job object for the input params. |

**Raises**

| Error code   | Issue                                                        |
| ------------ | ------------------------------------------------------------ |
| Forbidden    | Current user may not have permission to view details of job. |
| TimeoutError | When the default time out of 1800 secs.                      |

### watch()

Watch job status at given interval and yield job object.

**Parameters**

| Parameter | Type           | Default | Description                                         |
| --------- | -------------- | ------- | --------------------------------------------------- |
| interval  | Optional\[int] | 3       | Interval in seconds between polling for job status. |
| timeout   | Optional\[int] | 1800    | Timeout in seconds for iterator to stop.            |

**Usage**

```python
JOB_ID = "69f846db-5aac-44fe-9fa5-14f40048e4b2"
job = fdl.Job.get(id_=JOB_ID)

for ijob in job.watch(interval=30, timeout=1200):
    print(f'Status: {ijob.status} - progress: {ijob.progress}')
```

**Returns**

| Return Type                             | Description              |
| --------------------------------------- | ------------------------ |
| Iterator\[[Job](api-methods-30.md#job)] | Iterator of job objects. |

**Raises**

| Error code   | Issue                                                        |
| ------------ | ------------------------------------------------------------ |
| Forbidden    | Current user may not have permission to view details of job. |
| TimeoutError | When the default time out of 1800 secs.                      |

***

## Models

A Model is a **representation of your machine learning model** which can be used for monitoring, explainability, and more.
You **do not need to upload your model artifact in order to onboard your model**, but doing so will significantly improve the quality of explanations generated by Fiddler.

## Model

Model object contains the below parameters.

| Parameter                  | Type                                                 | Default                | Description                                                                                      |
| -------------------------- | ---------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------ |
| id                         | UUID                                                 | -                      | Unique identifier for the model.                                                                 |
| name                       | str                                                  | -                      | Unique name of the model (only alphanumeric and underscores are allowed).                        |
| input\_type                | [ModelInputType](api-methods-30.md#modelinputtype)   | ModelInputType.TABULAR | Input data type used by the model.                                                               |
| task                       | [ModelTask](api-methods-30.md#modeltask)             | ModelTask.NOT\_SET     | Task the model is designed to address.                                                           |
| task\_params               | [ModelTaskParams](api-methods-30.md#modeltaskparams) | -                      | Task parameters given to a particular model.                                                     |
| schema                     | [ModelSchema](api-methods-30.md#modelschema)         | -                      | Model schema defines the details of each column.                                                 |
| version                    | Optional\[str]                                       | -                      | Unique version name within a model                                                               |
| spec                       | [ModelSpec](api-methods-30.md#modelspec)             | -                      | Model spec defines how model columns are used along with model task.                             |
| description                | str                                                  | -                      | Description of the model.                                                                        |
| event\_id\_col             | str                                                  | -                      | Column containing event id.                                                                      |
| event\_ts\_col             | str                                                  | -                      | Column containing event timestamp.                                                               |
| xai\_params                | [XaiParams](api-methods-30.md#xaiparams)             | -                      | Explainability parameters of the model.                                                          |
| artifact\_status           | str                                                  | -                      | Artifact Status of the model.                                                                    |
| artifact\_files            | list\[dict]                                          | -                      | Dictionary containing file details of model artifact.                                            |
| is\_binary\_ranking\_model | bool                                                 | -                      | True if model is [ModelTask.RANKING](api-methods-30.md#modeltask) and has only 2 target classes. |
| created\_at                | datetime                                             | -                      | Time at which model was created.                                                                 |
| updated\_at                | datetime                                             | -                      | Latest time at which model was updated.                                                          |
| created\_by                | [User](api-methods-30.md#user)                       | -                      | Details of the who created the model.                                                            |
| updated\_by                | [User](api-methods-30.md#user)                       | -                      | Details of the who last updated the model.                                                       |
| project                    | [Project](api-methods-30.md#project)                 | -                      | Details of the project to which the model belongs.                                               |
| organization               | [Organization](api-methods-30.md#organization)       | -                      | Details of the organization to which the model belongs.                                          |

### constructor()

Initialize a new model instance.

**Usage**

```python
model = fdl.Model(
    name='model_name',
    project_id=project.id,
    task=fdl.ModelTask.BINARY_CLASSIFICATION,
    task_params=fdl.ModelTaskParams(target_class_order=['no', 'yes']),
    schema=model_schema,
    spec=model_spec,
    event_id_col='column_name_1',
    event_ts_col='column_name_2',
)
```

**Parameters**

| Parameter      | Type                                                 | Default                | Description                                                          |
| -------------- | ---------------------------------------------------- | ---------------------- | -------------------------------------------------------------------- |
| name           | str                                                  | -                      | Unique name of the model                                             |
| project\_id    | UUID                                                 | -                      | Unique identifier for the project to which model belongs.            |
| input\_type    | [ModelInputType](api-methods-30.md#modelinputtype)   | ModelInputType.TABULAR | Input data type used by the model.                                   |
| task           | [ModelTask](api-methods-30.md#modeltask)             | ModelTask.NOT\_SET     | Task the model is designed to address.                               |
| schema         | [ModelSchema](api-methods-30.md#modelschema)         | -                      | Model schema defines the details of each column.                     |
| spec           | [ModelSpec](api-methods-30.md#modelspec)             | -                      | Model spec defines how model columns are used along with model task. |
| version        | Optional\[str]                                       | -                      | Unique version name within a model                                   |
| task\_params   | [ModelTaskParams](api-methods-30.md#modeltaskparams) | -                      | Task parameters given to a particular model.                         |
| description    | str                                                  | -                      | Description of the model.                                            |
| event\_id\_col | str                                                  | -                      | Column containing event id.                                          |
| event\_ts\_col | str                                                  | -                      | Column containing event timestamp.                                   |
| xai\_params    | [XaiParams](api-methods-30.md#xaiparams)             | -                      | Explainability parameters of the model.                              |

### from\_data()

Build model instance from the given dataframe or file(csv/parquet).

**Parameters**

| Parameter        | Type                                                 | Default                | Description                                                          |
| ---------------- | ---------------------------------------------------- | ---------------------- | -------------------------------------------------------------------- |
| source           | pd.DataFrame \| Path \| str                          | -                      | Pandas dataframe or path to csv/parquet file                         |
| name             | str                                                  | -                      | Unique name of the model                                             |
| project\_id      | UUID \| str                                          | -                      | Unique identifier for the project to which model belongs.            |
| input\_type      | [ModelInputType](api-methods-30.md#modelinputtype)   | ModelInputType.TABULAR | Input data type used by the model.                                   |
| task             | [ModelTask](api-methods-30.md#modeltask)             | ModelTask.NOT\_SET     | Task the model is designed to address.                               |
| spec             | [ModelSpec](api-methods-30.md#modelspec)             | -                      | Model spec defines how model columns are used along with model task. |
| version          | Optional\[str]                                       | -                      | Unique version name within a model                                   |
| task\_params     | [ModelTaskParams](api-methods-30.md#modeltaskparams) | -                      | Task parameters given to a particular model.                         |
| description      | Optional\[str]                                       | -                      | Description of the model.                                            |
| event\_id\_col   | Optional\[str]                                       | -                      | Column containing event id.                                          |
| event\_ts\_col   | Optional\[str]                                       | -                      | Column containing event timestamp.                                   |
| xai\_params      | [XaiParams](api-methods-30.md#xaiparams)             | -                      | Explainability parameters of the model.                              |
| max\_cardinality | Optional\[int]                                       | None                   | Max cardinality to detect categorical columns.                       |
| sample\_size     | Optional\[int]                                       | -                      | No. of samples to use for generating schema.                         |

**Usage**

```python
MODEL_NAME = 'example_model'
PROJECT_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
MODEL_SPEC = {
  'custom_features': [],
  'decisions': ['Decisions'],
  'inputs': [
    'CreditScore',
    'Geography',
  ],
  'metadata': [],
  'outputs': ['probability_churned'],
  'schema_version': 1,
  'targets': ['Churned'],
}

# Without version
model = fdl.Model.from_data(
  source=<file_path>,
  name=MODEL_NAME,
  project_id=PROJECT_ID,
  spec=fdl.ModelSpec(**MODEL_SPEC),
)

# With version
model = fdl.Model.from_data(
  source=<file_path>,
  name=MODEL_NAME,
  version='v2',
  project_id=PROJECT_ID,
  spec=fdl.ModelSpec(**MODEL_SPEC),
)
```

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Notes**

* > `from_data` will not create a model entry on Fiddler Platform.\
  > Instead this method only returns a model instance which can be edited, call `.create()` to onboard the model to\
  > Fiddler Platform.
* > `spec` is optional to `from_data` method. However, a `spec` with at least `inputs` is required for model onboarding.
* > Make sure `spec` is passed to `from_data` method if model requires custom features. This method generates centroids\
  > which are needed for custom feature drift computation
* > If `version` is not explicitly passed, Fiddler Platform will treat it as `v1` version of the model.

### create()

Onboard a new model to Fiddler Platform

**Parameters**

No

**Usage**

```python
model = fdl.Model.from_data(...)
model.create()
```

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Raises**

| Error code | Issue                                       |
| ---------- | ------------------------------------------- |
| Conflict   | Model with same name may exist in project . |

### get()

Get model from Fiddler Platform based on UUID.

**Parameters**

| Parameter | Type        | Default | Description                      |
| --------- | ----------- | ------- | -------------------------------- |
| id\_      | UUID \| str | -       | Unique identifier for the model. |

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Raises**

| Error code | Issue                                                          |
| ---------- | -------------------------------------------------------------- |
| NotFound   | Model with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of model. |

**Usage**

```python
MODEL_ID = '4531bfd9-2ca2-4a7b-bb5a-136c8da09ca2'
model = fdl.Model.get(id_=MODEL_ID)
```

### from\_name()

Get model from Fiddler Platform based on name and project UUID.

**Parameters**

| Parameter   | Type          | Default | Description                        |
| ----------- | ------------- | ------- | ---------------------------------- |
| name        | str           | -       | Name of the model.                 |
| project\_id | UUID \| str   | -       | Unique identifier for the project. |
| version     | Optional\[str] | -       | Unique version name within a model |

> `version` parameter is available from `fiddler-client==3.1` onwards

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

PROJECT = fdl.Project.from_name(name=PROJECT_NAME)

# Without version
MODEL = fdl.Model.from_name(name=MODEL_NAME, project_id=PROJECT.id)

# With version
MODEL = fdl.Model.from_name(name=MODEL_NAME, project_id=PROJECT.id, version='v2')
```

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Notes**

* When the version is not passed, then the model created without any version will be fetched. Fiddler internally\
  assigns version=v1 when not passed.
* When the version is passed, method will fetch the model corresponding to that specific version.

**Raises**

| Error code | Issue                                                          |
| ---------- | -------------------------------------------------------------- |
| NotFound   | Model not found in the given project name.                     |
| Forbidden  | Current user may not have permission to view details of model. |


### list()

Gets all models of a project.

**Parameters**

| Parameter   | Type            | Default | Description                                              |
| ----------- | --------------- | ------- | -------------------------------------------------------- |
| project\_id | UUID \| str     | -       | Unique UUID of the project to which model is associated. |
| name        | Optional\[str]   | -       | Model name. Pass this to fetch all versions of a model.  |

**Returns**

| Return Type                                                 | Description                        |
| ----------------------------------------------------------- | ---------------------------------- |
| Iterable\[[Model Compact](api-methods-30.md#model-compact)] | Iterable of model compact objects. |

**Errors**

| Error code | Issue                                                      |
| ---------- | ---------------------------------------------------------- |
| Forbidden  | Current user may not have permission to the given project. |

**Usage example**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)

models = fdl.Model.list(project_id=project.id)
```

**Notes**

> Since `Model` contains a lot of information, list operations does not return all the fields of a model.\
> Instead this method returns `ModelCompact` objects on which `.fetch()` can be called to get the complete `Model`\
> instance.\
> For most of the use-cases, `ModelCompact` objects are sufficient.

### update()

Update an existing model. Only following fields are allowed to be updated, backend will ignore if any other\
field is updated on the instance.

**Parameters**

| Parameter      | Type                                                | Default | Description                             |
| -------------- | --------------------------------------------------- | ------- | --------------------------------------- |
| version        | Optional\[str]                                      | None    | Model version name                      |
| xai\_params    | Optional\[[XaiParams](api-methods-30.md#xaiparams)] | None    | Explainability parameters of the model. |
| description    | Optional\[str]                                      | None    | Description of the model.               |
| event\_id\_col | Optional\[str]                                      | None    | Column containing event id.             |
| event\_ts\_col | Optional\[str]                                      | None    | Column containing event timestamp.      |

> `version` parameter is available from `fiddler-client==3.1` onwards

**Usage**

```python
model.description = 'YOUR_MODEL_DESCRIPTION'
model.update()
```

**Returns**

No

**Raises**

| Error code | Issue                      |
| ---------- | -------------------------- |
| BadRequest | If field is not updatable. |


### duplicate()

Duplicate the model instance with the given version name.

This call will not save the model on Fiddler Platform. After making changes to the model instance, call `.create()` to add the model version to Fiddler Platform.

> Added in version 3.1.0

**Parameters**

| Parameter | Type           | Default | Description        |
| --------- | -------------- | ------- | ------------------ |
| version   | Optional\[str] | None    | Model version name |

**Usage**

```python
PROJECT_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
MODEL_NAME = 'test_model'

model = Model.from_name(name=MODEL_NAME, project_id=PROJECT_ID, version='v3')
new_model = model.duplicate(version='v4')
new_model.schema['Age'].min = 18
new_model.schema['Age'].max = 60

new_model.create()
```

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Raises**

| Error code | Issue                      |
| ---------- | -------------------------- |
| BadRequest | If field is not updatable. |


### remove_column()

Remove column from model object(in-place)

Modifies the model object in-place by removing the column with name column_name.
Do this before uploading the model to the Fiddler Platform (which can be done with the
create() method), otherwise the change does not take effect.

> Added in version 3.7.0

**Parameters**

| Parameter     | Type   | Default | Description                                      |
| ------------- | ------ | ------- | ------------------------------------------------ |
| column_name   | str    | -       | Name of the column to be removed                 |
| missing_ok    | bool   | -       | If False, raises an error if column is not found |

**Usage**

```python
MODEL_NAME = 'example_model'
PROJECT_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
MODEL_SPEC = {
  'custom_features': [],
  'decisions': ['Decisions'],
  'inputs': [
    'CreditScore',
    'Geography',
  ],
  'metadata': [],
  'outputs': ['probability_churned'],
  'schema_version': 1,
  'targets': ['Churned'],
}

# Build model instance from the given dataframe or file(csv/parquet).
model = fdl.Model.from_data(
  source=<file_path>,
  name=MODEL_NAME,
  project_id=PROJECT_ID,
  spec=fdl.ModelSpec(**MODEL_SPEC),
)

# Remove a column from model
model.remove_column(column_name='CreditScore', missing_ok=False)

```

**Returns**

| Return Type | Description     |
| ------------| --------------- |
| None        |                 |

**Raises**

| Error code | Issue                                             |
| ---------- | ------------------------------------------------- |
| KeyError   | If column is not present and missing_ok is False. |


### delete()

Delete a model.

**Parameters**

No

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

job = model.delete()
job.wait()
```

**Returns**

| Return Type                         | Description                           |
| ----------------------------------- | ------------------------------------- |
| [Job](api-methods-30.md#job-object) | Async job details for the delete job. |

**Notes**

> Model deletion is an async process, hence a job object is returned on `delete()` call.\
> Call `job.wait()` to wait for the job to complete. If you are planning to create a model with the same\
> name, please wait for the job to complete, otherwise backend will not allow new model with same name.

### add\_surrogate()

Add surrogate existing model.

**Parameters**

| Parameter          | Type                                                              | Default | Description                  |
| ------------------ | ----------------------------------------------------------------- | ------- | ---------------------------- |
| dataset\_id        | UUID \| str                                                       | -       | Dataset identifier           |
| deployment\_params | Optional\[[DeploymentParams](api-methods-30.md#deploymentparams)] | -       | Model deployment parameters. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

DEPLOYMENT_PARAMS = {'memory': 1024, 'cpu': 1000}

model.add_surrogate(
  dataset_id=dataset.id,
  deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
)
```

**Returns**

| Return Type                  | Description                                  |
| ---------------------------- | -------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the add surrogate job. |

**Raises**

| Error code | Issue                                  |
| ---------- | -------------------------------------- |
| BadRequest | Invalid deployment parameter is passed |

### update\_surrogate()

Update surrogate existing model.

**Parameters**

| Parameter          | Type                                                              | Default | Description                  |
| ------------------ | ----------------------------------------------------------------- | ------- | ---------------------------- |
| dataset\_id        | UUID \| str                                                       | -       | Dataset identifier           |
| deployment\_params | Optional\[[DeploymentParams](api-methods-30.md#deploymentparams)] | None    | Model deployment parameters. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

DEPLOYMENT_PARAMS = {'memory': 1024, 'cpu': 1000}

model.update_surrogate(
  dataset_id=dataset.id,
  deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
)
```

**Returns**

| Return Type                  | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the update surrogate job. |

### add\_artifact()

Add artifact files to existing model.

**Parameters**

| Parameter          | Type                                                              | Default | Description                                        |
| ------------------ | ----------------------------------------------------------------- | ------- | -------------------------------------------------- |
| model\_dir         | str                                                               | -       | Path to directory containing artifacts for upload. |
| deployment\_params | Optional\[[DeploymentParams](api-methods-30.md#deploymentparams)] | None    | Model deployment parameters.                       |

**Usage**

```python
MODEL_DIR = 'PATH_TO_MODEL_DIRECTORY'
DEPLOYMENT_PARAMS = {'memory': 1024, 'cpu': 1000}

model.add_artifact(
  model_dir=MODEL_DIR,
  deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
)
```

**Returns**

| Return Type                  | Description                                 |
| ---------------------------- | ------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the add artifact job. |

### update\_artifact()

Update existing artifact files in a model.

**Parameters**

| Parameter          | Type                                                              | Default | Description                                        |
| ------------------ | ----------------------------------------------------------------- | ------- | -------------------------------------------------- |
| model\_dir         | str                                                               | -       | Path to directory containing artifacts for upload. |
| deployment\_params | Optional\[[DeploymentParams](api-methods-30.md#deploymentparams)] | None    | Model deployment parameters.                       |

**Usage**

```python
MODEL_DIR = 'PATH_TO_MODEL_DIRECTORY'
DEPLOYMENT_PARAMS = {'memory': 1024, 'cpu': 1000}

model.update_artifact(
  model_dir=MODEL_DIR,
  deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
)
```

**Returns**

| Return Type                  | Description                                 |
| ---------------------------- | ------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the add artifact job. |

### download\_artifact()

Download existing artifact files in a model.

**Parameters**

| Parameter   | Type | Default | Description                                  |
| ----------- | ---- | ------- | -------------------------------------------- |
| output\_dir | str  | -       | Path to directory to download the artifacts. |

**Usage**

```python
OUTPUT_DIR = 'PATH_TO_TARGET_DIRECTORY'
model.download_artifact(output_dir=OUTPUT_DIR)
```

**Returns**

No

### Properties

### datasets

List all datasets associated with a model.

**Parameters**

No

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

model.datasets
```

**Returns**

| Return Type                                     | Description                    |
| ----------------------------------------------- | ------------------------------ |
| Iterable\[[Dataset](api-methods-30.md#dataset)] | Iterable of dataset instances. |

**Raises**

| Error code | Issue                                                          |
| ---------- | -------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of model. |

### model\_deployment

Get the model deployment object associated with the model.

**Parameters**

No

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

model.model_deployment
```

**Returns**

| Return Type                                            | Description                |
| ------------------------------------------------------ | -------------------------- |
| [Model deployment](api-methods-30.md#model-deployment) | Model deployment instance. |

**Raises**

| Error code | Issue                                                          |
| ---------- | -------------------------------------------------------------- |
| NotFound   | Model with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of model. |

### publish()

Publish Pre-production or production events.

**Parameters**

| Parameter     | Type                                                    | Default            | Description                                                                                                                                                                                                                                                                                                               |
| ------------- | ------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| source        | Union\[list\[dict\[str, Any]], str, Path, pd.DataFrame] | -                  | <p>Source can be:<br>1. Path or str path: path for data file.<br>2. list[dict]: list of event dicts. EnvType.PRE_PRODUCTION not supported.<br>3. dataframe: events dataframe.</p>                                                                                                                                         |
| environment   | EnvType                                                 | EnvType.PRODUCTION | Either EnvType.PRE\_PRODUCTION or EnvType.PRODUCTION                                                                                                                                                                                                                                                                      |
| dataset\_name | Optional\[str]                                          | None               | Name of the dataset. Not supported for EnvType.PRODUCTION                                                                                                                                                                                                                                                                 |
| update        | Optional\[bool]                                         | False              | If True, the events data passed in the publish call will be used to update previously published event records matched by their event\_ids (note that only updating target and metadata columns is supported). For more details refer to [Updating Events](../Client\_Guide/publishing-production-data/updating-events.md) |

**Usage**

**Pre-requisite**

```python
# Before publishing, make sure you set up the necessary fields of the model(if any).
# If you set the fields to non-empty value, We expect them passed in the source.
model.event_ts_col = 'timestamp'
model.event_id_col = 'event_id'
model.update()
```

**Publish dataset (pre-production data) from file**

```python
# Publish File
FILE_PATH = 'PATH_TO_DATASET_FILE'
job = model.publish(
  source=FILE_PATH,
  environment=fdl.EnvType.PRE_PRODUCTION,
  dataset_name='training_dataset'
)
# The publish() method is asynchronous by default. Use the publish job's wait() method
# if synchronous behavior is desired.
# job.wait()
```

**Publish dataset (pre-production data) from dataframe**

```python
df = pd.DataFrame(np.random.randint(0, 100, size=(10, 4)), columns=list('ABCD'))
job = model.publish(
  source=df,
  environment=fdl.EnvType.PRE_PRODUCTION,
  dataset_name='training_dataset'
)
# The publish() method is asynchronous by default. Use the publish job's wait() method
# if synchronous behavior is desired.
# job.wait()
```

**Publish production events from list**

List is only supported for production data but not for pre-production.

Events are published as a stream. This mode is recommended If you have a high volume of continuous real-time traffic of events, as it allows for more efficient processing on our backend.

It returns a list of `event_id` for each of the published events.

```python
# Publish list of dictionary objects
events = [
  {'A': 56, 'B': 68, 'C': 67, 'D': 27, 'event_id': 'A1', 'timestamp':'2024-05-01 00:00:00'},
  {'A': 43, 'B': 59, 'C': 64, 'D': 18, 'event_id': 'A2', 'timestamp':'2024-05-01 00:00:00'},
  ...
]
event_ids = model.publish(
  source=events,
  environment=fdl.EnvType.PRODUCTION
)
```

**Notes**

> In this example where `model.event_id_col`=`event_id`, we expect `event_id` as the required key of the dictionary. Otherwise if you keep `model.event_id_col=None`, our backend will generate unique event ids and return these back to you. Same for `model.event_ts_col`, we assign current time as event timestamp in case of `None`.

**Publish production events from file**

Batch events is faster if you want to publish a large-scale set of historical data.

```python
# Publish File
FILE_PATH = 'PATH_TO_EVENTS_FILE'
job = model.publish(
  source=FILE_PATH,
  environment=fdl.EnvType.PRODUCTION,
)
# The publish() method is asynchronous by default. Use the publish job's wait() method
# if synchronous behavior is desired.
# job.wait()
```

**Publish production events from dataframe**

```python
df = pd.DataFrame(
    {
        'A': np.random.randint(0, 100, size=(2)),
        'B': np.random.randint(0, 100, size=(2)),
        'C': np.random.randint(0, 100, size=(2)),
        'D': np.random.randint(0, 100, size=(2)),
        'timestamp': [time.time()]*2,  # optional model.event_ts_col
        'event_id': ['A1', 'A2'],      # optional model.event_id_col
    }
)
event_ids = model.publish(
  source=df,
  environment=fdl.EnvType.PRODUCTION,
)
```

**Update events**

if you need to update the target or metadata columns for a previously published production event, set `update`=True. For more details please refer to [Updating Events](../Client\_Guide/publishing-production-data/updating-events.md). Note only production events can be updated.

**Update production events from list**

```python
# suppose 'A' is the target, 'B' is the metadata. The Model.event_id_col is required.
events_update = [
    {
        'A': [0],                   
        'B': [0], 
        'event_id': ['A1'], 
    },
    {
        'A': [1], 
        'B': [1], 
        'event_id': ['A2'], 
    },
]
event_ids = model.publish(
    source=events_update,
    environment=fdl.EnvType.PRODUCTION,
    update=True,
)
```

**Update production events from dataframe**

```python
df_update = pd.DataFrame(
    {
        'A': [0, 1],  # suppose 'A' is the target
        'B': [0, 1],  # suppose 'B' is the metadata
        'event_id': ['A1', 'A2'],  # required model.event_id_col
    }
)
event_ids = model.publish(
    source=df_update,
    environment=fdl.EnvType.PRODUCTION,
    update=True,
)
```

**Returns**

In case of streaming publish

| Return Type      | Source      | Description              |
| ---------------- | ----------- | ------------------------ |
| list\[UUID\|str] | list\[dict] | List of event identifier |

In case of batch publish

| Return Type                  | Source                          | Description                             |
| ---------------------------- | ------------------------------- | --------------------------------------- |
| [Job](api-methods-30.md#job) | Union\[str, Path, pd.DataFrame] | Job object for file/dataframe published |

## Model Compact

Model object contains the below parameters.

| Parameter | Type           | Default | Description                        |
| --------- | -------------- | ------- | ---------------------------------- |
| id        | UUID           | -       | Unique identifier for the model.   |
| name      | str            | -       | Unique name of the model           |
| version   | Optional\[str] | -       | Unique version name within a model |

#### fetch()

Fetch the model instance from Fiddler Platform.

**Parameters**

No

**Returns**

| Return Type                      | Description     |
| -------------------------------- | --------------- |
| [Model](api-methods-30.md#model) | Model instance. |

**Raises**

| Error code | Issue                                                          |
| ---------- | -------------------------------------------------------------- |
| NotFound   | Model not found for the given identifier                       |
| Forbidden  | Current user may not have permission to view details of model. |

***

## Model deployment

Get model deployment object of a particular model.

### Model deployment:

Model deployment object contains the below parameters.

| Parameter        | Type                                               | Default                         | Description                                                                                                                                                                         |
| ---------------- | -------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id               | UUID                                               | -                               | Unique identifier for the model.                                                                                                                                                    |
| model            | [Model](api-methods-30.md#model)                   | -                               | Details of the model.                                                                                                                                                               |
| project          | [Project](api-methods-30.md#project)               | -                               | Details of the project to which the model belongs.                                                                                                                                  |
| organization     | [Organization](api-methods-30.md#organization)     | -                               | Details of the organization to which the model belongs.                                                                                                                             |
| artifact\_type   | [ArtifactType](api-methods-30.md#artifacttype)     | -                               | Task the model is designed to address.                                                                                                                                              |
| deployment\_type | [DeploymentType](api-methods-30.md#deploymenttype) | -                               | Type of deployment of the model.                                                                                                                                                    |
| image\_uri       | Optional\[str]                                     | md-base/python/python-311:1.0.0 | A Docker image reference. See available images [here](../product-guide/explainability/flexible-model-deployment/). |
| active           | bool                                               | True                            | Status of the deployment.                                                                                                                                                           |
| replicas         | Optional\[str]                                     | 1                               | <p>The number of replicas running the model.<br>Minimum value: 1<br>Maximum value: 10<br>Default value: 1</p>                                                                       |
| cpu              | Optional\[str]                                     | 100                             | <p>The amount of CPU (milli cpus) reserved per replica.<br>Minimum value: 10<br>Maximum value: 4000 (4vCPUs)<br>Default value: 100</p>                                              |
| memory           | Optional\[str]                                     | 256                             | <p>The amount of memory (mebibytes) reserved per replica.<br>Minimum value: 150<br>Maximum value: 16384 (16GiB)<br>Default value: 256</p>                                           |
| created\_at      | datetime                                           | -                               | Time at which model deployment was created.                                                                                                                                         |
| updated\_at      | datetime                                           | -                               | Latest time at which model deployment was updated.                                                                                                                                  |
| created\_by      | [User](api-methods-30.md#user)                     | -                               | Details of the user who created the model deployment.                                                                                                                               |
| updated\_by      | [User](api-methods-30.md#user)                     | -                               | Details of the user who last updated the model deployment.                                                                                                                          |

***

### Update model deployment

Update an existing model deployment.

**Parameters**

| Parameter | Type            | Default | Description                                                                                                                               |
| --------- | --------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| active    | Optional\[bool] | True    | Status of the deployment.                                                                                                                 |
| replicas  | Optional\[str]  | 1       | <p>The number of replicas running the model.<br>Minimum value: 1<br>Maximum value: 10<br>Default value: 1</p>                             |
| cpu       | Optional\[str]  | 100     | <p>The amount of CPU (milli cpus) reserved per replica.<br>Minimum value: 10<br>Maximum value: 4000 (4vCPUs)<br>Default value: 100</p>    |
| memory    | Optional\[str]  | 256     | <p>The amount of memory (mebibytes) reserved per replica.<br>Minimum value: 150<br>Maximum value: 16384 (16GiB)<br>Default value: 256</p> |

**Usage**

```python
# Update CPU allocation and activate the model pod
model_id = 'a920ddb6-edb7-473b-a5f7-035f91e1d53a'
model = fdl.Model.get(model_id)
model_deployment = model.deployment
model_deployment.cpu = 300
model_deployment.active = True
model_deployment.update()
```

**Returns**

No

**Raises**

| Error code | Issue                      |
| ---------- | -------------------------- |
| BadRequest | If field is not updatable. |

***

## Organizations

Organization in which all the projects, models are present.

***

### Organization:

Organization object contains the below parameters.

| Parameter   | Type     | Default | Description                                    |
| ----------- | -------- | ------- | ---------------------------------------------- |
| id          | UUID     | -       | Unique identifier for the organization.        |
| name        | str      | -       | Unique name of the organization.               |
| created\_at | datetime | -       | Time at which organization was created.        |
| updated\_at | datetime | -       | Latest time at which organization was updated. |

***

## Projects

Projects are **used to organize your models and datasets**. Each project can represent a machine learning task (e.g. predicting house prices, assessing creditworthiness, or detecting fraud).

A project **can contain one or more models** (e.g. lin\_reg\_house\_predict, random\_forest\_house\_predict).

***

### Project

Project object contains the below parameters.

| Parameter    | Type                                           | Default | Description                                               |
| ------------ | ---------------------------------------------- | ------- | --------------------------------------------------------- |
| id           | UUID                                           | None    | Unique identifier for the project.                        |
| name         | str                                            | None    | Unique name of the project.                               |
| created\_at  | datetime                                       | None    | Time at which project was created.                        |
| updated\_at  | datetime                                       | None    | Latest time at which project was updated.                 |
| created\_by  | [User](api-methods-30.md#user)                 | None    | Details of the who created the project.                   |
| updated\_by  | [User](api-methods-30.md#user)                 | None    | Details of the who last updated the project.              |
| organization | [Organization](api-methods-30.md#organization) | None    | Details of the organization to which the project belongs. |

### create()

Creates a project using the specified name.

**Parameters**

| Parameter | Type | Default | Description                 |
| --------- | ---- | ------- | --------------------------- |
| name      | str  | None    | Unique name of the project. |

**Usage**

```python
PROJECT_NAME = 'bank_churn'
project = fdl.Project(name=PROJECT_NAME)
project.create()
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Project](api-methods-30.md#project) | Project instance. |

**Raises**

| Error code | Issue                             |
| ---------- | --------------------------------- |
| Conflict   | Project with same name may exist. |

### get()

Get project from Fiddler Platform based on UUID.

**Parameters**

| Parameter | Type | Default | Description                        |
| --------- | ---- | ------- | ---------------------------------- |
| id\_      | UUID | None    | Unique identifier for the project. |

**Usage**

```python
PROJECT_ID = '1531bfd9-2ca2-4a7b-bb5a-136c8da09ca1'
project = fdl.Project.get(id_=PROJECT_ID)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Project](api-methods-30.md#project) | Project instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Project with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of project. |

### from\_name()

Get project from Fiddler Platform based on name.

**Parameters**

| Parameter     | Type | Default | Description          |
| ------------- | ---- | ------- | -------------------- |
| project\_name | str  | None    | Name of the project. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
project = fdl.Project.from_name(name=PROJECT_NAME)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Project](api-methods-30.md#project) | Project instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Project not found in the given project name.                     |
| Forbidden  | Current user may not have permission to view details of project. |

### get\_or\_create()

> Added in version 3.7.0

Get the project instance if exists, otherwise create a new project.

**Parameters**

| Parameter | Type | Default | Description                 |
| --------- | ---- | ------- | --------------------------- |
| name      | str  | None    | Unique name of the project. |



**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
project = fdl.Project.get_or_create(name=PROJECT_NAME)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Project](api-methods-30.md#project) | Project instance. |

**Raises**

| Error code | Issue                                                          |
| ---------- |----------------------------------------------------------------|
| Forbidden  | Current user may not have permission to view/create a project. |


### list()

Gets all projects in an organization.

**Parameters**

No

**Returns**

| Return Type                                      | Description                  |
| ------------------------------------------------ | ---------------------------- |
| Iterable\[[Project](api-methods-30.md#project) ] | Iterable of project objects. |

**Errors**

| Error code | Issue                                                      |
| ---------- | ---------------------------------------------------------- |
| Forbidden  | Current user may not have permission to the given project. |

**Usage example**

```python
projects = fdl.Project.list()
```

### delete()

Delete a project.

**Parameters**

| Parameter | Type | Default | Description                  |
| --------- | ---- | ------- | ---------------------------- |
| id\_      | UUID | None    | Unique UUID of the project . |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
project = fdl.Project.from_name(name=PROJECT_NAME)

project.delete()
```

**Returns**

None

### Properties

### List models()

List all models associated with a project.

**Parameters**

| Parameter | Type | Default | Description                  |
| --------- | ---- | ------- | ---------------------------- |
| id\_      | UUID | None    | Unique UUID of the project . |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
project = fdl.Project.from_name(name=PROJECT_NAME)

project.models
```

**Returns**

| Return Type                                 | Description                |
| ------------------------------------------- | -------------------------- |
| Iterable\[[Model](api-methods-30.md#model)] | Iterable of model objects. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Project with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of project. |

## Segments

Fiddler offers the ability to segment your data based on a custom condition.

### Segment

Segment object contains the below parameters.

| Parameter   | Type           | Default | Description                                 |
| ----------- | -------------- | ------- | ------------------------------------------- |
| id          | UUID           | -       | Unique identifier for the segment.          |
| name        | str            | -       | Segment name.                               |
| model\_id   | UUID           | -       | UUID of the model to which segment belongs. |
| definition  | str            | -       | Definition of the segment.                  |
| description | Optional\[str] | None    | Description of the segment.                 |
| created\_at | datetime       | -       | Time of creation of segment.                |

***

### constructor()

Initialize a new segment.

**Usage params**

| Parameter   | Type           | Default | Description                                 |
| ----------- | -------------- | ------- | ------------------------------------------- |
| name        | str            | -       | Segment name.                               |
| model\_id   | UUID           | -       | UUID of the model to which segment belongs. |
| definition  | str            | -       | Definition of the segment.                  |
| description | Optional\[str] | None    | Description of the segment.                 |

**Usage**

```python
SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

segment = fdl.Segment(
        name=SEGMENT_NAME,
        model_id=model.id,
        definition="Age < 60", #Use Fiddler Query Language (FQL) to define your custom segments
        description='Users with Age under 60',
    )
```

***

### get()

Get segment from Fiddler Platform based on UUID.

**Parameters**

| Parameter | Type | Default | Description                        |
| --------- | ---- | ------- | ---------------------------------- |
| id\_      | UUID | -       | Unique identifier for the segment. |

**Usage**

```python
SEGMENT_ID = 'ba6ec4e4-7188-44c5-ba84-c2cb22b4bb00'
segment = fdl.Segment.get(id_= SEGMENT_ID)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Segment](api-methods-30.md#segment) | Segment instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Segment with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of segment. |

***

### from\_name()

Get segment from Fiddler Platform based on name and model UUID.

**Parameters**

| Parameter | Type        | Default | Description                      |
| --------- | ----------- | ------- | -------------------------------- |
| name      | str         | -       | Name of the segment.             |
| model\_id | UUID \| str | -       | Unique identifier for the model. |

**Usage**

```python
SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

segment = fdl.Segment.from_name(
    name=NAME,
    model_id=model.id
)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Segment](api-methods-30.md#segment) | Segment instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Segment with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of segment. |

### list()

List all segments in the given model.

**Parameters**

| Parameter | Type | Default | Description                                    |
| --------- | ---- | ------- | ---------------------------------------------- |
| model\_id | UUID | -       | UUID of the model associated with the segment. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

segment = fdl.Segment.list(model_id=model.id)
```

**Returns**

| Return Type                                     | Description                      |
| ----------------------------------------------- | -------------------------------- |
| Iterable\[[Segment](api-methods-30.md#segment)] | Iterable of all segment objects. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of segment. |

### create()

Adds a segment to a model.

**Parameters**

No

**Usage**

```python
SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

segment = fdl.Segment(
        name=SEGMENT_NAME,
        model_id=model.id,
        definition="Age < 60", #Use Fiddler Query Language (FQL) to define your custom segments
        description='Users with Age under 60',
    ).create()
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Segment](api-methods-30.md#segment) | Segment instance. |

**Raises**

| Error code | Issue                                           |
| ---------- | ----------------------------------------------- |
| Conflict   | Segment with same name may exist for the model. |
| BadRequest | Invalid definition.                             |
| NotFound   | Given model may not exist .                     |

### delete()

Delete a segment.

**Parameters**

No

**Usage**

```python
SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)

segment = fdl.Segment.from_name(name=SEGMENT_NAME,model_id=model.id)


segment.delete()
```

**Returns**

No

**Raises**

| Error code | Issue                                                   |
| ---------- | ------------------------------------------------------- |
| NotFound   | Segment with given identifier not found.                |
| Forbidden  | Current user may not have permission to delete segment. |

## Webhooks

Webhooks integration for alerts to be posted on Slack or other apps.

### Webhook()

Webhook object contains the below parameters.

| Parameter   | Type                                                 | Default | Description                                                                |
| ----------- | ---------------------------------------------------- | ------- | -------------------------------------------------------------------------- |
| id          | UUID                                                 | -       | Unique identifier for the webhook.                                         |
| name        | str                                                  | -       | Unique name of the webhook.                                                |
| url         | str                                                  | -       | Webhook integration URL.                                                   |
| provider    | [WebhookProvider](api-methods-30.md#webhookprovider) | -       | App in which the webhook needs to be integrated. Either 'SLACK' or 'OTHER' |
| created\_at | datetime                                             | -       | Time at which webhook was created.                                         |
| updated\_at | datetime                                             | -       | Latest time at which webhook was updated.                                  |

***

### constructor()

Initialize a new webhook.

**Parameters**

| Parameter | Type                                                 | Default | Description                                      |
| --------- | ---------------------------------------------------- | ------- | ------------------------------------------------ |
| name      | str                                                  | -       | Unique name of the webhook.                      |
| url       | str                                                  | -       | Webhook integration URL.                         |
| provider  | [WebhookProvider](api-methods-30.md#webhookprovider) | -       | App in which the webhook needs to be integrated. |

**Usage**

```python
WEBHOOK_NAME = 'test_webhook_config_name'
WEBHOOK_URL = 'https://www.slack.com'
WEBHOOK_PROVIDER = 'SLACK'
webhook = fdl.Webhook(
        name=WEBHOOK_NAME, url=WEBHOOK_URL, provider=WEBHOOK_PROVIDER
    )
```

### get()

Gets all details of a particular webhook from UUID.

**Parameters**

| Parameter | Type | Default | Description                        |
| --------- | ---- | ------- | ---------------------------------- |
| id\_      | UUID | -       | Unique identifier for the webhook. |

**Usage**

```python
WEBHOOK_ID = 'a5b654eb-15c8-43c8-9d50-9ba6eea9a0ff'
webhook = fdl.Webhook.get(id_=WEBHOOK_ID)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Webhook](api-methods-30.md#webhook) | Webhook instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Webhook with given identifier not found.                         |
| Forbidden  | Current user may not have permission to view details of webhook. |

### from\_name()

Get Webhook from Fiddler Platform based on name.

**Parameters**

| Parameter | Type | Default | Description          |
| --------- | ---- | ------- | -------------------- |
| name      | str  | -       | Name of the webhook. |

**Usage**

```python
WEBHOOK_NAME = 'YOUR_WEBHOOK_NAME'

webhook = fdl.Webhook.from_name(
    name=WEBHOOK_NAME
)
```

**Returns**

| Return Type                          | Description       |
| ------------------------------------ | ----------------- |
| [Webhook](api-methods-30.md#webhook) | Webhook instance. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| NotFound   | Webhook with given name not found.                               |
| Forbidden  | Current user may not have permission to view details of webhook. |

### list()

Gets all webhooks accessible to a user.

**Parameters**

No

**Usage**

```python
WEBHOOKS = fdl.Webhook.list()
```

**Returns**

| Return Type                                     | Description                  |
| ----------------------------------------------- | ---------------------------- |
| Iterable\[[Webhook](api-methods-30.md#webhook)] | Iterable of webhook objects. |

**Raises**

| Error code | Issue                                                            |
| ---------- | ---------------------------------------------------------------- |
| Forbidden  | Current user may not have permission to view details of webhook. |

### create()

Create a new webhook.

**Parameters**

No

**Usage**

```python
WEBHOOK_NAME = 'YOUR_WEBHOOK_NAME'
WEBHOOK_URL = 'https://www.slack.com'
WEBHOOK_PROVIDER = 'SLACK'
webhook = fdl.Webhook(
        name=WEBHOOK_NAME, url=WEBHOOK_URL, provider=WEBHOOK_PROVIDER
    )
webhook.create()
```

**Returns**

| Return Type                          | Description     |
| ------------------------------------ | --------------- |
| [Webhook](api-methods-30.md#webhook) | Webhook object. |

### update()

Update an existing webhook.

**Parameters**

| Parameter | Type                                                 | Default | Description                                      |
| --------- | ---------------------------------------------------- | ------- | ------------------------------------------------ |
| name      | str                                                  | -       | Unique name of the webhook.                      |
| url       | str                                                  | -       | Webhook integration URL.                         |
| provider  | [WebhookProvider](api-methods-30.md#webhookprovider) | -       | App in which the webhook needs to be integrated. |

**Usage**

```python
WEBHOOK_NAME = "YOUR_WEBHOOK_NAME"
webhook_list = fdl.Webhook.list()
webhook_instance = None

for webhook in webhook_list:
    if WEBHOOK_NAME == webhook.name:
    webhook_instance = webhook

webhook_instance.name = 'NEW_WEBHOOK_NAME'
webhook_instance.update()
```

**Returns**

None

**Raises**

| Error code | Issue                      |
| ---------- | -------------------------- |
| BadRequest | If field is not updatable. |

### delete()

Delete a webhook.

**Parameters**

| Parameter | Type | Default | Description                 |
| --------- | ---- | ------- | --------------------------- |
| id\_      | UUID | -       | Unique UUID of the webhook. |

**Usage**

```python
WEBHOOK_NAME = "YOUR_WEBHOOK_NAME"
webhook_instance = None

for webhook in webhook_list:
    if WEBHOOK_NAME == webhook.name:
    webhook_instance = webhook

webhook_instance.delete()
```

**Returns**

None

***

## Explainability

Explainability methods for models.

### precompute\_feature\_importance

Pre-compute feature importance for a model on a dataset. This is used in various places in the UI.\
A single feature importance can be precomputed (computed and cached) for a model.

**Parameters**

| Parameter       | Type             | Default | Description                                                                                   |
| --------------- | ---------------- | ------- | --------------------------------------------------------------------------------------------- |
| dataset\_id     | UUID             | -       | The unique identifier of the dataset.                                                         |
| num\_samples    | Optional\[int]   | None    | The number of samples used.                                                                   |
| num\_iterations | Optional\[int]   | None    | The maximum number of ablated model inferences per feature.                                   |
| num\_refs       | Optional\[int]   | None    | The number of reference points used in the explanation.                                       |
| ci\_level       | Optional\[float] | None    | The confidence level (between 0 and 1).                                                       |
| update          | Optional\[bool]  | False   | Flag to indicate whether the precomputed feature importance should be recomputed and updated. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

job = model.precompute_feature_importance(dataset_id=dataset.id, update=False)
```

**Returns**

| Return Type                  | Description                                 |
| ---------------------------- | ------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the pre-compute job . |

### get\_precomputed\_feature\_importance

Get pre-computed global feature **importance** for a model over a dataset or a slice.

**Parameters**

No

**Usage**

```python
feature_importance = model.get_precomputed_feature_importance()
```

**Returns**

| Return Type | Description                                         |
| ----------- | --------------------------------------------------- |
| Tuple       | A named tuple with the feature importance results . |

### get\_feature\_importance()

Get global feature **importance** for a model over a dataset or a slice.

**Usage params**

| Parameter       | Type                                                                                                                                   | Default | Description                                                                                                       |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------- |
| data\_source    | [DatasetDataSource](api-methods-30.md#datasetdatasource) | -       | Dataset data Source for the input dataset to compute feature importance on |
| num\_iterations | Optional\[int]                                                                                                                         | None    | The maximum number of ablated model inferences per feature.                                                       |
| num\_refs       | Optional\[int]                                                                                                                         | None    | The number of reference points used in the explanation.                                                           |
| ci\_level       | Optional\[float]                                                                                                                       | None    | The confidence level (between 0 and 1).                                                                           |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

model = fdl.Model.get(id_=model.id)

# Dataset data source
feature_importance = model.get_feature_importance(
        data_source=fdl.DatasetDataSource(
            env_type='PRE-PRODUCTION',
            env_id=dataset.id,
        ),
    )
```

**Returns**

| Return Type | Description                                         |
| ----------- | --------------------------------------------------- |
| Tuple       | A named tuple with the feature importance results . |

**Raises**

| Error code | Issue                           |
| ---------- | ------------------------------- |
| BadRequest | If dataset id is not specified. |

***

### precompute\_feature\_impact()

Pre-compute feature impact for a model on a dataset. This is used in various places in the UI.\
A single feature impact can be precomputed (computed and cached) for a model.

**Usage params**

| Parameter       | Type             | Default | Description                                                                                                                                                              |
| --------------- | ---------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| dataset\_id     | UUID             | -       | The unique identifier of the dataset.                                                                                                                                    |
| num\_samples    | Optional\[int]   | None    | The number of samples used.                                                                                                                                              |
| num\_iterations | Optional\[int]   | None    | The maximum number of ablated model inferences per feature.                                                                                                              |
| num\_refs       | Optional\[int]   | None    | The number of reference points used in the explanation.                                                                                                                  |
| ci\_level       | Optional\[float] | None    | The confidence level (between 0 and 1).                                                                                                                                  |
| min\_support    | Optional\[int]   | 15      | Only used for NLP (TEXT inputs) models. Specify a minimum support (number of times a specific word was present in the sample data) to retrieve top words. Default to 15. |
| update          | Optional\[bool]  | False   | Flag to indicate whether the precomputed feature impact should be recomputed and updated.                                                                                |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

job = model.precompute_feature_impact(dataset_id=dataset.id, update=False)
```

**Returns**

| Return Type                  | Description                                 |
| ---------------------------- | ------------------------------------------- |
| [Job](api-methods-30.md#job) | Async job details for the pre-compute job . |

### upload\_feature\_impact()

Upload a custom feature impact for a model of input type `TABULAR`. All input features need to be passed for the method to run successfully. Partial upload of feature impacts are not supported.

**Usage params**

| Parameter            | Type            | Default | Description                                                                                                                                             |
| -------------------- | --------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| feature\_impact\_map | dict            | -       | <p>Feature impacts dictionary with feature name as key and impact as value.<br>Impact value is of type float and can be positive, negative or zero.</p> |
| update               | Optional\[bool] | False   | Flag to indicate whether the feature impact is being uploaded or updated.                                                                               |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'
FEATURE_IMPACT_MAP = {'feature_1': 0.1, 'feature_2': 0.4, 'feature_3': -0.05}

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

feature_impacts = model.upload_feature_impact(feature_impact_map=FEATURE_IMPACT_MAP, update=False)
```

**Returns**

| Return Type | Description                                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| Dict        | Dictionary with feature\_names, feature\_impact\_scores, system\_generated, model\_task, model\_input\_type, created\_at. |

### get\_precomputed\_feature\_impact()

Get pre-computed global feature **impact** for a model over a dataset or a slice.

**Parameters**

No

**Usage**

```python
feature_impact = model.get_precomputed_feature_impact()
```

**Returns**

| Return Type | Description                                     |
| ----------- | ----------------------------------------------- |
| Tuple       | A named tuple with the feature impact results . |

### get\_feature\_impact()

Get global feature **impact** for a model over a dataset or a slice.

**Parameters**

| Parameter       | Type                                                                                                                                   | Default | Description                                                                                                                                                             |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| data\_source    | [DatasetDataSource](api-methods-30.md#datasetdatasource) | -       | Dataset data Source for the input dataset to compute feature importance   |
| num\_iterations | Optional\[int]                                                                                                                         | None    | The maximum number of ablated model inferences per feature.                                                                                                             |
| num\_refs       | Optional\[int]                                                                                                                         | None    | The number of reference points used in the explanation.                                                                                                                 |
| ci\_level       | Optional\[float]                                                                                                                       | None    | The confidence level (between 0 and 1).                                                                                                                                 |
| min\_support    | Optional\[int]                                                                                                                         | 15      | Only used for NLP (TEXT inputs) models. Specify a minimum support (number of times a specific word was present in the sample data)to retrieve top words. Default to 15. |
| output\_columns | Optional\[list\[str]]                                                                                                                  | None    | Only used for NLP (TEXT inputs) models. Output column names to compute feature impact on.                                                                               |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

model = fdl.Model.get(id_=model.id)

# Dataset data source
feature_impact = model.get_feature_impact(
        data_source=fdl.DatasetDataSource(
            env_type='PRE-PRODUCTION',
            env_id=dataset.id,
        ),
    )
```

**Returns**

| Return Type | Description                                     |
| ----------- | ----------------------------------------------- |
| Tuple       | A named tuple with the feature impact results . |

**Raises**

| Error code | Issue                                                 |
| ---------- | ----------------------------------------------------- |
| BadRequest | If dataset id is not specified or query is not valid. |

### precompute\_predictions()

Pre-compute predictions for a model on a dataset.

**Parameters**

| Parameter   | Type            | Default | Description                                                                                               |
| ----------- | --------------- | ------- | --------------------------------------------------------------------------------------------------------- |
| dataset\_id | UUID            | -       | Unique identifier of the dataset used for prediction.                                                     |
| chunk\_size | Optional\[int]  | None    | Chunk size for fetching predictions.                                                                      |
| update      | Optional\[bool] | False   | Flag to indicate whether the pre-computed predictions should be re-computed and updated for this dataset. |

**Usage**

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_DATASET_NAME'

project = fdl.Project.from_name(name=PROJECT_NAME)
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

model.precompute_predictions(dataset_id=dataset.id, update=False)
```

**Returns**

| Return Type                  | Description                                |
| ---------------------------- | ------------------------------------------ |
| [Job](api-methods-30.md#job) | Async job details for the prediction job . |

### explain()

Get explanation for a single observation.

**Parameters**

| Parameter           | Type                                                                                                               | Default                     | Description                                                                                                                                                                                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| input\_data\_source | Union\[[RowDataSource](api-methods-30.md#rowdatasource), [EventIdDataSource](api-methods-30.md#eventiddatasource)] | -                           | DataSource for the input data to compute explanation on (RowDataSource, EventIdDataSource).                                                                                                                                                                                  |
| ref\_data\_source   | Optional\[[DatasetDataSource](api-methods-30.md#datasetdatasource)]                                                | None                        | <p>Dataset data Source for the reference data to compute explanation.<br>Only used for non-text models and the following methods:<br>'SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET'.</p>                                                                                  |
| method              | Optional\[Union\[[ExplainMethod](api-methods-30.md#explainmethod), str]]                                           | ExplainMethod.FIDDLER\_SHAP | <p>Explanation method name. Could be your custom explanation method or one of the following method:<br>'SHAP', 'FIDDLER_SHAP', 'IG', 'PERMUTE', 'MEAN_RESET', 'ZERO_RESET'.</p>                                                                                              |
| num\_permutations   | Optional\[int]                                                                                                     | None                        | <p>For Fiddler SHAP, that corresponds to the number of coalitions to sample to estimate the Shapley values of each single-reference game.<br>For the permutation algorithms, this corresponds to the number of permutations from the dataset to use for the computation.</p> |
| ci\_level           | Optional\[float]                                                                                                   | None                        | The confidence level (between 0 and 1) to use for the confidence intervals in Fiddler SHAP. Not used for other methods.                                                                                                                                                      |
| top\_n\_class       | Optional\[int]                                                                                                     | None                        | For multiclass classification models only, specifying if only the n top classes are computed or all classes (when parameter is None).                                                                                                                                        |

**Usage**

```python
# RowDataSource and
explain_result = model.explain(
        input_data_source=fdl.RowDataSource(
            row={
                'CreditScore': 619,
                'Geography': 'France',
                'Gender': 'Female',
                'Age': 42,
                'Tenure': 2,
                'Balance': 0.0,
                'NumOfProducts': 1,
                'HasCrCard': 'Yes',
                'IsActiveMember': 'Yes',
                'EstimatedSalary': 101348.88,
            },
        ),
        ref_data_source=fdl.DatasetDataSource(
            env_type='PRODUCTION',
        ),
    )

# EventIdDataSource
explain_result = model.explain(
        input_data_source=fdl.EventIdDataSource(
            event_id='5531bfd9-2ca2-4a7b-bb5a-136c8da09ca0',
            env_type=fdl.EnvType.PRE_PRODUCTION
        ),
        ref_data_source=fdl.DatasetDataSource(
            env_type='PRODUCTION',
        ),
    )
```

**Return params**

| Return Type | Description                                 |
| ----------- | ------------------------------------------- |
| Tuple       | A named tuple with the explanation results. |

**Raises**

| Error code   | Issue                                      |
| ------------ | ------------------------------------------ |
| NotSupported | If specified source type is not supported. |



### download\_data()

Download data using environment and segments, to csv or parquet file. 10M rows is the max size that can be downloaded.

**Parameters**

| Parameter   | Type                  | Default | Description                                                                                             |
| ----------- | --------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| output\_dir | Union\[Path, str]     | -       | Path to download the file.                                                                              |
| env\_type   | [EnvType](api-methods-30.md#envtype)              | -       | Type of environment to query (PRODUCTION or PRE_PRODUCTION)   |
| env\_id     | UUID                  | None    | If PRE_PRODUCTION env selected, provide the uuid of the dataset to query. |
| start\_time | Optional\[datetime] | None | Start time to retrieve data, only for PRODUCTION env. If no time zone is indicated, UTC is assumed.|
| end\_time   | Optional\[datetime] | None | End time to retrieve data, only for PRODUCTION env. If no time zone is indicated, UTC is assumed.|
| segment\_id | Optional\[UUID] | None | Optional segment UUID to query data using a saved segment associated with the model |
| segment\_definition | Optional\[str] | None | Optional segment FQL definition to query data using an applied segment. This segment will not be saved to the model. |
| columns | Optional\[List\[str]] | None |  Allows caller to explicitly specify list of columns to retrieve. Default to None which fetch all columns from the model. |
| max\_rows   | Optional\[int]        | None    | Number of maximum rows to fetch.                                                                        |
| chunk_size | Optional\[int] | 1000 |  Number of rows per chunk to download data. You can increase that number for faster download if you query less than 1000 columns and don't have vector columns.|
| fetch\_vectors | Optional\[bool] | None | Whether the vectors columns are fetched or not. Default to False. |
| output_format | [DownloadFormat](api-methods-30.md#downloadformat) | PARQUET | Indicating if the result should be a CSV file or a PARQUET file. |

**Usage**

```python
DATASET_ID = 'YOUR_DATASET_UUID'

model.download_data(
    output_dir='test_download',
    env_type=fdl.EnvType.PRODUCTION,
    env_id=None,  # Not needed for Environment PRODUCTION
    start_time=datetime(2024, 10, 4, 0, 0, 0),
    end_time=datetime(2024, 10, 5,  0, 0, 0),
    segment_definition="Geography=='Germany'",
    segment_id=None,
    columns=['Geography', 'EstimatedSalary'],
    output_format=fdl.DownloadFormat.PARQUET,
    max_rows=1000000,
    chunk_size=10000,
    fetch_vectors=False,
)
```

**Returns**

Parquet or CSV file with slice data contents downloaded to the Path mentioned in output\_dir.

**Raises**

| Error code | Issue                    |
| ---------- | ------------------------ |
| BadRequest | If given segment is not implemented correctly |

### predict()

Run model on an input dataframe.

**Parameters**

| Parameter   | Type           | Default | Description                          |
| ----------- | -------------- | ------- | ------------------------------------ |
| df          | pd.DataFrame   | None    | Feature dataframe.                   |
| chunk\_size | Optional\[int] | None    | Chunk size for fetching predictions. |

**Usage**

```python
data = {
        'row_id': 1109,
        'fixed acidity': 10.8,
        'volatile acidity': 0.47,
        'citric acid': 0.43,
        'residual sugar': 2.1,
        'chlorides': 0.171,
        'free sulfur dioxide': 27.0,
        'total sulfur dioxide': 66.0,
        'density': 0.9982,
        'pH': 3.17,
        'sulphates': 0.76,
        'alcohol': 10.8,
    }
df = pd.DataFrame(data, index=data.keys())
predictions = model.predict(df=df)
```

**Returns**

| Return Type | Description                            |
| ----------- | -------------------------------------- |
| Dataframe   | A pandas DataFrame of the predictions. |


***

## Constants

### ModelInputType

Input data type used by the model.

| Enum Value             | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| ModelInputType.TABULAR | For tabular models.                                    |
| ModelInputType.TEXT    | For text models.                                       |
| ModelInputType.MIXED   | For models which can be a mixture of text and tabular. |

### ModelTask

The model’s algorithm type.

| Enum Value                           | Description                                       |
| ------------------------------------ | ------------------------------------------------- |
| ModelTask.REGRESSION                 | For regression models.                            |
| ModelTask.BINARY\_CLASSIFICATION     | For binary classification models.                 |
| ModelTask.MULTICLASS\_CLASSIFICATION | For multiclass classification models.             |
| ModelTask.RANKING                    | For ranking classification models.                |
| ModelTask.LLM                        | For LLM models.                                   |
| ModelTask.NOT\_SET                   | For other model tasks or no model task specified. |

### DataType

The available data types when defining a model [Column](api-methods-30.md#column).

| Enum Value         | Description                 |
| ------------------ |-----------------------------|
| DataType.FLOAT     | For floats.                 |
| DataType.INTEGER   | For integers.               |
| DataType.BOOLEAN   | For booleans.               |
| DataType.STRING    | For strings.                |
| DataType.CATEGORY  | For categorical types.      |
| DataType.TIMESTAMP | For 32-bit Unix timestamps. |
| DataType.VECTOR    | For vector types            |

### CustomFeatureType

This is an enumeration defining the types of custom features that can be created.

| Enum                                     | Value                                                     |
| ---------------------------------------- | --------------------------------------------------------- |
| CustomFeatureType.FROM\_COLUMNS          | Represents custom features derived directly from columns. |
| CustomFeatureType.FROM\_VECTOR           | Represents custom features derived from a vector column.  |
| CustomFeatureType.FROM\_TEXT\_EMBEDDING  | Represents custom features derived from text embeddings.  |
| CustomFeatureType.FROM\_IMAGE\_EMBEDDING | Represents custom features derived from image embeddings. |
| CustomFeatureType.ENRICHMENT             | Represents custom features derived from an enrichment.    |

### ArtifactType

Indicator of type of a model artifact.

| Enum Value                   | Description         |
| ---------------------------- | ------------------- |
| ArtifactType.SURROGATE       | For surrogates.     |
| ArtifactType.PYTHON\_PACKAGE | For python package. |

### DeploymentType

Indicator of how the model was deployed.

| Enum Value                     | Description            |
| ------------------------------ | ---------------------- |
| DeploymentType.BASE\_CONTAINER | For base containers.   |
| DeploymentType.MANUAL          | For manual deployment. |

### EnvType

Environment type of a dataset.

| Enum Value              | Description                |
| ----------------------- | -------------------------- |
| EnvType.PRODUCTION      | For production events.     |
| EnvType.PRE\_PRODUCTION | For pre production events. |

### BaselineType

Type of a baseline.

| Enum Value           | Description                      |
| -------------------- | -------------------------------- |
| BaselineType.STATIC  | For static production baseline.  |
| BaselineType.ROLLING | For rolling production baseline. |

### DownloadFormat

File format to download

| Enum Value              | Description                       |
| ----------------------- | --------------------------------- |
| DownloadFormat.PARQUET  | Download data into a Parquet file |
| DownloadFormat.CSV      | Download data into a CSV file     |

### WindowBinSize

Window for rolling baselines.

| Enum Value          | Description                       |
| ------------------- | --------------------------------- |
| WindowBinSize.HOUR  | For rolling window to be 1 hour.  |
| WindowBinSize.DAY   | For rolling window to be 1 day.   |
| WindowBinSize.WEEK  | For rolling window to be 1 week.  |
| WindowBinSize.MONTH | For rolling window to be 1 month. |

### WebhookProvider

Specifies the integration provider or OTHER for generic callback response.

| Enum Value            | Description        |
| --------------------- | ------------------ |
| WebhookProvider.SLACK | For slack.         |
| WebhookProvider.OTHER | For any other app. |

### AlertCondition

Specifies the comparison operator to use for an alert threshold value.

| Enum Value             | Description                |
| ---------------------- | -------------------------- |
| AlertCondition.GREATER | The greater than operator. |
| AlertCondition.LESSER  | the less than operator.    |

### BinSize

Specifies the comparison operator to use for an alert threshold value.

| Enum Value    | Description     |
| ------------- | --------------- |
| BinSize.HOUR  | The 1 hour bin. |
| BinSize.DAY   | the 1 day bin.  |
| BinSize.WEEK  | The 7 day bin.  |
| BinSize.MONTH | The 30 day bin. |

### CompareTo

Specifies the type of evaluation to use for an alert.

| Enum Value            | Description                                                         |
| --------------------- | ------------------------------------------------------------------- |
| CompareTo.RAW_VALUE   | For an absolute comparison of a specified value to the alert metric |
| CompareTo.TIME_PERIOD | For a relative comparison of the alert metric to the same metric from a previous time period. |

### Priority

Priority level label for alerts.

| Enum Value       | Description                |
| ---------------- | -------------------------- |
| Priority.LOW     | The low priority label.    |
| Priority.MEDIUM  | The medium priority label. |
| Priority.HIGH    | The high priority label.   |

### Severity

Severity level for alerts.

| Enum Value        | Description                                                                               |
| ----------------- | ----------------------------------------------------------------------------------------- |
| Severity.DEFAULT  | For AlertRule when none of the thresholds have passed.                                   |
| Severity.WARNING  | For AlertRule when alert crossed the warning\_threshold but not the critical\_threshold. |
| Severity.CRITICAL | For AlertRule when alert crossed the critical\_raw\_threshold.                           |

### Alert Metric ID

AlertRule metric_id parameter constants.

| Metric Type     | Metric Id Constant         | Metric Name                |
|-----------------|----------------------------|----------------------------|
| Drift           | jsd                        | Jensen-Shannon Distance    |
|                 | psi                        | Population Stability Index |
| Service Metrics | traffic                    | Traffic                    |
| Data Integrity  | null_violation_count       | Missing Value Violation    |
|                 | type_violation_count       | Type Violation             |
|                 | range_violation_count      | Range Violation            |
|                 | any_violation_count        | Any Violation              |
|                 | null_violation_percentage  | % Missing Value Violation  |
|                 | type_violation_percentage  | % Type Violation           |
|                 | range_violation_percentage | % Range Violation          |
|                 | any_violation_percentage   | % Any Violation            |
| Statistics      | sum                        | Sum                        |
|                 | average                    | Average                    |
|                 | frequency                  | Frequency                  |
| Performance     | accuracy                   | Accuracy                   |
|                 | log_loss                   | Log Loss                   |
|                 | map                        | MAP                        |
|                 | ndcg_mean                  | NDhorCG                    |
|                 | query_count                | Query Count                |
|                 | precision                  | Precision                  |
|                 | recall                     | Recall / TPR               |
|                 | f1_score                   | F1                         |
|                 | geometric_mean             | Geometric Mean             |
|                 | data_count                 | Total Count                |
|                 | expected_calibration_error | Expected Calibration Error |
|                 | auc                        | AUC                        |
|                 | auroc                      | AUROC                      |
|                 | calibrated_threshold       | Calibrated Threshold       |
|                 | fpr                        | False Positive Rate        |
| Custom Metrics  | UUID of custom metric      | Custom Metric Name         |

***

## Schemas

### Column

A model column representation.

| Parameter            | Type                                          | Default | Description                                                           |
| -------------------- | --------------------------------------------- | ------- | --------------------------------------------------------------------- |
| name                 | str                                           | None    | Column name provided by the customer.                                 |
| data\_type           | list\[[Datatype](api-methods-30.md#datatype)] | None    | List of columns.                                                      |
| min                  | Union\[int, float]                            | None    | Min value of integer/float column.                                    |
| max                  | Union\[int, float]                            | None    | Max value of integer/float column.                                    |
| categories           | list                                          | None    | List of unique values of a categorical column.                        |
| bins                 | list\[Union\[int, float]]                     | None    | Bins of integer/float column.                                         |
| replace\_with\_nulls | list                                          | None    | Replace the list of given values to NULL if found in the events data. |
| n\_dimensions        | int                                           | None    | Number of dimensions of a vector column.                              |

## fdl.Enrichment (Private Preview)

| Input Parameter | Type            | Default | Description                                                                                                 |
| --------------- | --------------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| name            | str             |         | The name of the custom feature to generate                                                                  |
| enrichment      | str             |         | The enrichment operation to be applied                                                                      |
| columns         | List\[str]      |         | The column names on which the enrichment depends                                                            |
| config          | Optional\[List] | {}      | (optional): Configuration specific to an enrichment operation which controls the behavior of the enrichment |

```python
fiddler_custom_features = [
        fdl.TextEmbedding(
            name='question_cf',
            source_column='question',
            column='question_embedding',
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

_Note_

Enrichments are **disabled** by default. To enable them, contact your administrator. Failing to do so will result in an error during the `add_model` call.

***

### Embedding (Private Preview)

**Supported Models:**

| model\_name                            | size  | Type                    | pooling\_method | Notes           |
| -------------------------------------- | ----- | ----------------------- | --------------- | --------------- |
| BAAI/bge-small-en-v1.5                 | small | Sentence Transformer    |                 |                 |
| sentence-transformers/all-MiniLM-L6-v2 | med   | Sentence Transformer    |                 |                 |
| thenlper/gte-base                      | med   | Sentence Transformer    |                 | _**(default)**_ |
| gpt2                                   | med   | Encoder NLP Transformer | last\_token     |                 |
| distilgpt2                             | small | Encoder NLP Transformer | last\_token     |                 |
| EleuteherAI/gpt-neo-125m               | med   | Encoder NLP Transformer | last\_token     |                 |
| google/bert\_uncased\_L-4\_H-256\_A-4  | small | Decoder NLP Transformer | first\_token    | Smallest Bert   |
| bert-base-cased                        | med   | Decoder NLP Transformer | first\_token    |                 |
| distilroberta-base                     | med   | Decoder NLP Transformer | first\_token    |                 |
| xlm-roberta-large                      | large | Decoder NLP Transformer | first\_token    | Multilingual    |
| roberta-large                          | large | Decoder NLP Transformer | first\_token    |                 |

```python
fiddler_custom_features = [
      fdl.Enrichment(
          name='Question Embedding', # name of the enrichment, will be the vector col
          enrichment='embedding',
          columns=['question'], # only one allowed per embedding enrichment, must be a text column in dataframe
          config={ # optional
            'model_name': ... # default: 'thenlper/gte-base'
            'pooling_method': ... # choose from '{first/last/mean}_token'. Only required if NOT using a sentence transformer
          }
      ),
      fdl.TextEmbedding(
        name='question_cf', # name of the text embedding custom feature
        source_column='question', # source - raw text
        column='Question Embedding', # the name of the vector - output of the embedding enrichment
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

If embeddings have already been generated for any field and sent to Fiddler, they can be imported for visualization in UMAP by modifying the `column` field of TextEmbedding to be the column with the embeddings. The Embedding enrichment can also be removed for the corresponding input field, as there is no need for Fiddler to generate the embeddings in the case that embeddings are prepopulated and imported into Fiddler.


The above example will lead to generation of new column:

| Column                 | Type   | Description                                           |
| ---------------------- | ------ | ----------------------------------------------------- |
| FDL Question Embedding | vector | Embeddings corresponding to string column `question`. |




_Note_

In the context of Hugging Face models, particularly transformer-based models used for generating embeddings, the pooling\_method determines how the model processes the output of its layers to produce a single vector representation for input sequences (like sentences or documents). This is crucial when using these models for tasks like sentence or document embedding, where you need a fixed-size vector representation regardless of the input length.

***

### Centroid Distance (Private Preview)

```
fiddler_custom_features = [
      fdl.Enrichment(
        name='question_embedding',
        enrichment='embedding',
        columns=['question'],
      ),
      fdl.TextEmbedding(
          name='question_cf',
          source_column='question',
          column='question_embedding',
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```



The above example will lead to generation of new column:

| Column                                      | Type  | Description                                                                                      |
| ------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------ |
| FDL Centroid Distance (question\_embedding) | float | <p>Distance from the nearest K-Means centroid present in<br><code>question_embedding</code>.</p> |

_Note_

Does not calculate membership for preproduction data, so you cannot calculate drift. Centroid Distance is automatically added if the `TextEmbedding` enrichment is created for any given model.

***

### Personally Identifiable Information (Private Preview)

**List of PII entities**

| Entity Type         | Description                                                                                                                                                                                                                                                    | Detection Method                                    | Example                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| CREDIT\_CARD        | A credit card number is between 12 to 19 digits. [https://en.wikipedia.org/wiki/Payment\_card\_number](https://en.wikipedia.org/wiki/Payment\_card\_number)                                                                                                    | Pattern match and checksum                          | <p><code>4111111111111111</code><br><code>378282246310005</code> (American Express)</p>                           |
| CRYPTO              | A Crypto wallet number. Currently only Bitcoin address is supported                                                                                                                                                                                            | Pattern match, context and checksum                 | `1BoatSLRHtKNngkdXEeobR76b53LETtpyT`                                                                              |
| DATE\_TIME          | Absolute or relative dates or periods or times smaller than a day.                                                                                                                                                                                             | Pattern match and context                           | ../2024                                                                                                           |
| EMAIL\_ADDRESS      | An email address identifies an email box to which email messages are delivered                                                                                                                                                                                 | Pattern match, context and RFC-822 validation       | `trust@fiddler.ai`                                                                                                |
| IBAN\_CODE          | The International Bank Account Number (IBAN) is an internationally agreed system of identifying bank accounts across national borders to facilitate the communication and processing of cross border transactions with a reduced risk of transcription errors. | Pattern match, context and checksum                 | `DE89 3704 0044 0532 0130 00`                                                                                     |
| IP\_ADDRESS         | An Internet Protocol (IP) address (either IPv4 or IPv6).                                                                                                                                                                                                       | Pattern match, context and checksum                 | <p><code>1.2.3.4</code><br><code>127.0.0.12/16</code><br><code>1234:BEEF:3333:4444:5555:6666:7777:8888</code></p> |
| LOCATION            | Name of politically or geographically defined location (cities, provinces, countries, international regions, bodies of water, mountains                                                                                                                        | Custom logic and context                            | <p>PALO ALTO<br>Japan</p>                                                                                         |
| PERSON              | A full person name, which can include first names, middle names or initials, and last names.                                                                                                                                                                   | Custom logic and context                            | Joanna Doe                                                                                                        |
| PHONE\_NUMBER       | A telephone number                                                                                                                                                                                                                                             | Custom logic, pattern match and context             | `5556667890`                                                                                                      |
| URL                 | A URL (Uniform Resource Locator), unique identifier used to locate a resource on the Internet                                                                                                                                                                  | Pattern match, context and top level url validation | [www.fiddler.ai](http://www.fiddler.ai)                                                                           |
| US SSN              | A US Social Security Number (SSN) with 9 digits.                                                                                                                                                                                                               | Pattern match and context                           | `1234-00-5678`                                                                                                    |
| US\_DRIVER\_LICENSE | A US driver license according to [https://ntsi.com/drivers-license-format/](https://ntsi.com/drivers-license-format/)                                                                                                                                          | Pattern match and context                           |                                                                                                                   |
| US\_ITIN            | US Individual Taxpayer Identification Number (ITIN). Nine digits that start with a "9" and contain a "7" or "8" as the 4 digit.                                                                                                                                | Pattern match and context                           | 912-34-1234                                                                                                       |
| US\_PASSPORT        | A US passport number begins with a letter, followed by eight numbers                                                                                                                                                                                           | Pattern match and context                           | L12345678                                                                                                         |

```python
fiddler_custom_features = [
      fdl.Enrichment(
        name='Rag PII',
        enrichment='pii',
        columns=['question'], # one or more columns
        allow_list=['fiddler'], # Optional: list of strings that are white listed
        score_threshold=0.85, # Optional: float value for minimum possible confidence
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

The above example will lead to generation of new columns:

| Column                          | Type | Description                                                                              |
| ------------------------------- | ---- | ---------------------------------------------------------------------------------------- |
| FDL Rag PII (question)          | bool | Whether any PII was detected.                                                            |
| FDL Rag PII (question) Matches  | str  | What matches in raw text were flagged as potential PII (ex. ‘Douglas MacArthur,Korean’)? |
| FDL Rag PII (question) Entities | str  | What entites these matches were tagged as (ex. 'PERSON')?                                |

_Note_

PII enrichment is integrated with [Presidio](https://microsoft.github.io/presidio/analyzer/languages/)

***

### Evaluate (Private Preview)

Here is a summary of the three evaluation metrics for natural language generation:

| Metric | Description                                                                                      | Strengths                                    | Limitations                                            |
| ------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------ |
| bleu   | Measures precision of word n-grams between generated and reference texts                         | Simple, fast, widely used                    | Ignores recall, meaning, and word order                |
| rouge  | Measures recall of word n-grams and longest common sequences                                     | Captures more information than BLEU          | Still relies on word matching, not semantic similarity |
| meteor | Incorporates recall, precision, and additional semantic matching based on stems and paraphrasing | More robust and flexible than BLEU and ROUGE | Requires linguistic resources and alignment algorithms |

```python
fiddler_custom_features = [
      fdl.Enrichment(
        name='QA Evaluate',
        enrichment='evaluate',
        columns=['correct_answer', 'generated_answer'],
        config={
            'reference_col': 'correct_answer', # required
            'prediction_col': 'generated_answer', # required
            'metrics': ..., # optional, default - ['bleu', 'rouge' , 'meteor']
        }
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```



The above example generates 6 new columns:

| Column                      | Type  |
| --------------------------- | ----- |
| FDL QA Evaluate (bleu)      | float |
| FDL QA Evaluate (rouge1)    | float |
| FDL QA Evaluate (rouge2)    | float |
| FDL QA Evaluate (rougel)    | float |
| FDL QA Evaluate (rougelsum) | float |
| FDL QA Evaluate (meteor)    | float  |

***

### Textstat (Private Preview)

\*\*Supported Statistics \*\*

| Statistic                       | Description                                                                                      | Usage                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| char\_count                     | Total number of characters in text, including everything.                                        | Assessing text length, useful for platforms with character limits.   |
| letter\_count                   | Total number of letters only, excluding numbers, punctuation, spaces.                            | Gauging text complexity, used in readability formulas.               |
| miniword\_count                 | Count of small words (usually 1-3 letters).                                                      | Specific readability analyses, especially for simplistic texts.      |
| words\_per\_sentence            | Average number of words in each sentence.                                                        | Understanding sentence complexity and structure.                     |
| polysyllabcount                 | Number of words with more than three syllables.                                                  | Analyzing text complexity, used in some readability scores.          |
| lexicon\_count                  | Total number of words in the text.                                                               | General text analysis, assessing overall word count.                 |
| syllable\_count                 | Total number of syllables in the text.                                                           | Used in readability formulas, measures text complexity.              |
| sentence\_count                 | Total number of sentences in the text.                                                           | Analyzing text structure, used in readability scores.                |
| flesch\_reading\_ease           | Readability score indicating how easy a text is to read (higher scores = easier).                | Assessing readability for a general audience.                        |
| smog\_index                     | Measures years of education needed to understand a text.                                         | Evaluating text complexity, especially for higher education texts.   |
| flesch\_kincaid\_grade          | Grade level associated with the complexity of the text.                                          | Educational settings, determining appropriate grade level for texts. |
| coleman\_liau\_index            | Grade level needed to understand the text based on sentence length and letter count.             | Assessing readability for educational purposes.                      |
| automated\_readability\_index   | Estimates the grade level needed to comprehend the text.                                         | Evaluating text difficulty for educational materials.                |
| dale\_chall\_readability\_score | Assesses text difficulty based on a list of familiar words for average American readers.         | Determining text suitability for average readers.                    |
| difficult\_words                | Number of words not on a list of commonly understood words.                                      | Analyzing text difficulty, especially for non-native speakers.       |
| linsear\_write\_formula         | Readability formula estimating grade level of text based on sentence length and easy word count. | Simplifying texts, especially for lower reading levels.              |
| gunning\_fog                    | Estimates the years of formal education needed to understand the text.                           | Assessing text complexity, often for business or professional texts. |
| long\_word\_count               | Number of words longer than a certain length (often 6 or 7 letters).                             | Evaluating complexity and sophistication of language used.           |
| monosyllabcount                 | Count of words with only one syllable.                                                           | Readability assessments, particularly for simpler texts.             |

```python
fiddler_custom_features = [
      fdl.Enrichment(
          name='Text Statistics',
          enrichment='textstat',
          columns=['question'],
          config={
          'statistics' : [
              'char_count',
              'dale_chall_readability_score',
            ]
          },
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

The above example leads to the creation of two additional columns:

| Column                                                         | Type  | Description                                      |
| -------------------------------------------------------------- | ----- | ------------------------------------------------ |
| FDL Text Statistics (question) char\_count                     | int   | Character count of string in `question`column.   |
| FDL Text Statistics (question) dale\_chall\_readability\_score | float | Readability score of string in `question`column. |

***

### Sentiment (Private Preview)

```python
fiddler_custom_features = [
      fdl.Enrichment(
          name='Question Sentiment',
          enrichment='sentiment',
          columns=['question'],
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

The above example leads to creation of two columns:

| Column                                      | Type   | Description                                  |
| ------------------------------------------- | ------ | -------------------------------------------- |
| FDL Question Sentiment (question) compound  | float  | Raw score of sentiment.                      |
| FDL Question Sentiment (question) sentiment | string | One of `positive`, `negative` and \`neutral. |

***

### Profanity (Private Preview)

```python
fiddler_custom_features = [
      fdl.Enrichment(
            name='Profanity',
            enrichment='profanity',
            columns=['prompt', 'response'],
            config={'output_column_name': 'contains_profanity'},
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'response'],
    custom_features=fiddler_custom_features,
)
```



The above example leads to creation of two columns:

| Column                                       | Type | Description                                                                  |
| -------------------------------------------- | ---- | ---------------------------------------------------------------------------- |
| FDL Profanity (prompt) contains\_profanity   | bool | To indicate if input contains profanity in the value of the prompt column.   |
| FDL Profanity (response) contains\_profanity | bool | To indicate if input contains profanity in the value of the response column. |

***

### Answer Relevance (Private Preview)

```python
answer_relevance_config = {
  'prompt' : 'prompt_col',
  'response' : 'response_col',
}

fiddler_custom_features = [
      fdl.Enrichment(
          name = 'Answer Relevance',
          enrichment = 'answer_relevance',
          columns = ['prompt_col', 'response_col'],
          config = answer_relevance_config,
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt_col', 'response_col'],
    custom_features=fiddler_custom_features,
)
```

The above example will lead to the generation of a new column

| Column               | Type | Description                                                             |
| -------------------- | ---- | ----------------------------------------------------------------------- |
| FDL Answer Relevance | bool | Binary metric, which is True if `response` is relevant to the `prompt`. |

***

### Faithfulness (Private Preview)

```python
faithfulness_config = {
  'context' : ['doc_0', 'doc_1', 'doc_2'],
  'response' : 'response_col',
}

fiddler_custom_features = [
      fdl.Enrichment(
          name = 'Faithfulness',
          enrichment = 'faithfulness',
          columns = ['doc_0', 'doc_1', 'doc_2', 'response_col'],
          config = faithfulness_config,
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['doc_0', 'doc_1', 'doc_2', 'response_col'],
    custom_features=fiddler_custom_features,
)
```

The above example will lead to generation of new column:

| Column           | Type | Description                                                                                               |
| ---------------- | ---- | --------------------------------------------------------------------------------------------------------- |
| FDL Faithfulness | bool | Binary metric, which is True if the facts used in`response` is correctly used from the `context` columns. |

***

### Coherence (Private Preview)

```python
coherence_config = {
  'response' : 'response_col',
}

fiddler_custom_features = [
      fdl.Enrichment(
          name = 'Coherence',
          enrichment = 'coherence',
          columns = ['response_col'],
          config = coherence_config,
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['doc_0', 'doc_1', 'doc_2', 'response_col'],
    custom_features=fiddler_custom_features,
)
```

\


The above example will lead to generation of new column:

| Column        | Type | Description                                                                         |
| ------------- | ---- | ----------------------------------------------------------------------------------- |
| FDL Coherence | bool | Binary metric, which is True if`response` makes coherent arguments which flow well. |

***

### Conciseness (Private Preview)

```c
conciseness_config = {
  'response' : 'response_col',
}

fiddler_custom_features = [
      fdl.Enrichment(
          name = 'Conciseness',
          enrichment = 'conciseness',
          columns = ['response'],
          config = coherence_config,
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'doc_0', 'doc_1', 'doc_2', 'response'],
    custom_features=fiddler_custom_features,
)
```

The above example will lead to generation of new column:

| Column          | Type | Description                                                                   |
| --------------- | ---- | ----------------------------------------------------------------------------- |
| FDL Conciseness |      | Binary metric, which is True if`response` is concise, and not overly verbose. |

***

### Toxicity (Private Preview)

| Dataset    | PR-AUC | Precision | Recall |
| ---------- | ------ | --------- | ------ |
| Toxic-Chat | 0.4    | 0.64      | 0.24   |

#### Usage

The code snippet shows how to enable toxicity scoring on the `prompt` and `response` columns for each event published to Fiddler.

```python
fiddler_custom_features = [
      fdl.Enrichment(
            name='Toxicity',
            enrichment='toxicity',
            columns=['prompt', 'response'],
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'doc_0', 'doc_1', 'doc_2', 'response'],
    custom_features=fiddler_custom_features,
)
```

The above example leads to creation of two columns each for prompt and response that contain the prediction probability and the model decision.

For example for the prompt column following two columns will be generated

| Column                                   | Type  | Description                               |
| ---------------------------------------- | ----- | ----------------------------------------- |
| FDL Toxicity (prompt) toxicity\_prob     | float | Model prediction probability between 0-1. |
| FDL Toxicity (prompt) contains\_toxicity | bool  | Model prediction either 0 or 1.           |

***

### Regex Match (Private Preview)

```python
fiddler_custom_features = [
        fdl.Enrichment(
          name='Regex - only digits',
          enrichment='regex_match',
          columns=['prompt', 'response'],
          config = {
                'regex' : '^\d+$',
            }
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'doc_0', 'doc_1', 'doc_2', 'response'],
    custom_features=fiddler_custom_features,
)
```

The above example will lead to generation of new column

| Column                  | Type     | Description                                                                           |
| ----------------------- | -------- | ------------------------------------------------------------------------------------- |
| FDL Regex - only digits | category | Match or No Match, depending on the regex specified in config matching in the string. |

***

### Topic (Private Preview)

```python
fiddler_custom_features = [
      fdl.Enrichment(
          name='Topics',
          enrichment='topic_model',
          columns=['response'],
          config={'topics':['politics', 'economy', 'astronomy']},
      ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'doc_0', 'doc_1', 'doc_2', 'response'],
    custom_features=fiddler_custom_features,
)
```

\


The above example leads to creation of two columns -

| Column                                     | Type         | Description                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FDL Topics (response) topic\_model\_scores | list\[float] | Indicating probability of the given column in each of the topics specified in the Enrichment config. Each float value indicate probability of the given input classified in the corresponding topic, in the same order as topics. Each value will be between 0 and 1. The sum of values does not equal to 1, as each classification is performed independently of other topics. |
| FDL Topics (response) max\_score\_topic    | string       | Topic with the maximum score from the list of topic names specified in the Enrichment config.                                                                                                                                                                                                                                                                                   |

***

### Banned Keyword Detector (Private Preview)

```python
fiddler_custom_features = [
      fdl.Enrichment(
            name='Banned KW',
            enrichment='banned_keywords',
            columns=['prompt', 'response'],
            config={'output_column_name': 'contains_banned_kw', 'banned_keywords':['nike', 'adidas', 'puma'],},
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt', 'doc_0', 'doc_1', 'doc_2', 'response'],
    custom_features=fiddler_custom_features,
)
```

\


The above example leads to creation of two columns -

| Column                                        | Type | Description                                                                                             |
| --------------------------------------------- | ---- | ------------------------------------------------------------------------------------------------------- |
| FDL Banned KW (prompt) contains\_banned\_kw   | bool | To indicate if input contains one of the specified banned keywords in the value of the prompt column.   |
| FDL Banned KW (response) contains\_banned\_kw | bool | To indicate if input contains one of the specified banned keywords in the value of the response column. |

***

### Language Detector (Private Preview)

Language detector leverages [fasttext models](https://fasttext.cc/docs/en/language-identification.html) for language detection.

```python
fiddler_custom_features = [
      fdl.Enrichment(
            name='Language',
            enrichment='language_detection',
            columns=['prompt'],
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt'],
    custom_features=fiddler_custom_features,
)
```



The above example leads to creation of two columns -

| Column                                      | Type   | Description                                                    |
| ------------------------------------------- | ------ | -------------------------------------------------------------- |
| FDL Language (prompt) language              | string | Language prediction for input text                             |
| FDL Language (prompt) language\_probability | float  | To indicate the confidence probability of language prediction |

***

### Fast Safety (Private Preview)

The Fast safety enrichment evaluates the safety of the text along ten different dimensions: `illegal, hateful, harassing, racist, sexist, violent, sexual, harmful, unethical, jailbreaking`. These dimensions are all returned by default, but can be selectively chosen as needed. Fast safety is generated through the [Fast Trust Models](doc:llm-based-metrics).

```python
fiddler_custom_features = [
      fdl.Enrichment(
            name='Prompt Safety',
            enrichment='ftl_prompt_safety',
            columns=['prompt'],
            config={'classifiers':['jailbreaking', 'illegal']}
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['prompt'],
    custom_features=fiddler_custom_features,
)
```

\


The above example leads to creation of a column for each dimension. -

| Column                                       | Type  | Description                                                                 |
| -------------------------------------------- | ----- | --------------------------------------------------------------------------- |
| FDL Prompt Safety (prompt) `dimension`       | bool  | Binary metric, which is True if the input is deemed unsafe, False otherwise |
| FDL Prompt Safety (prompt) `dimension` score | float | To indicate the confidence probability of safety prediction                |

***

### Fast Faithfulness (Private Preview)

The Fast faithfulness enrichment is designed to evaluate the accuracy and reliability of facts presented in AI-generated text responses. Fast safety is generated through the [Fast Trust Models](doc:llm-based-metrics).

```python
fiddler_custom_features = [
        fdl.Enrichment(
            name='Faithfulness',
            enrichment='ftl_response_faithfulness',
            columns=['context', 'response'],
            config={'context_field':'context',
                    'response_field': 'response'}
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['context', 'response'],
    custom_features=fiddler_custom_features,
)
```



The above example leads to creation of two columns -

| Column                          | Type  | Description                                                                                               |
| ------------------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| FDL Faithfulness faithful       | bool  | Binary metric, which is True if the facts used in`response` is correctly used from the `context` columns. |
| FDL Faithfulness faithful score | float | To indicate the confidence probability of faithfulness prediction                                        |

***

### SQL Validation (Private Preview)
{% hint style="info" %}
Query validation is syntax based and does not check against any existing schema or databases for validity.
{% endhint %}

The SQL Validation enrichment is designed to evaluate different query dialects for syntax correctness.

```python
# The following dialects are supported
# 'athena', 'bigquery', 'clickhouse', 'databricks', 'doris', 'drill', 'duckdb', 'hive', 'materialize', 'mysql', 'oracle', 'postgres', 'presto', 'prql', 'redshift', 'risingwave', 'snowflake', 'spark', 'spark2', 'sqlite', 'starrocks', 'tableau', 'teradata', 'trino', 'tsql'
fiddler_custom_features = [
        fdl.Enrichment(
            name='SQLValidation',
            enrichment='sql_validation',
            columns=['query_string'],
            config={
                'dialect':'mysql'
            }
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['query_string'],
    custom_features=fiddler_custom_features,
)
```

The above example leads to creation of two columns -

| Column                          | Type  | Description                                                                                               |
| ------------------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| SQL Validator valid       | bool  | True if the query string is syntactically valid for the specified dialect, False if not. |
| SQL Validator errors | str | If syntax errors are found they will be present as a JSON serialized string containing a list of dictionaries describing the errors.  |

***

### JSON Validation (Private Preview)

The JSON Validation enrichment is designed to evaluate strings for correct JSON syntax and optionally against a user-defined schema for validation.

This enrichment uses the [python-jsonschema](https://python-jsonschema.readthedocs.io) library for json schema validation.  The defined `validation_schema` must be a valid python-jsonschema schema.

```python
fiddler_custom_features = [
        fdl.Enrichment(
            name='JSONValidation',
            enrichment='json_validation',
            columns=['json_string'],
            config={
                'strict':'true'
                'validation_schema': {
                    '$schema': 'https://json-schema.org/draft/2020-12/schema',
                    'type': 'object',
                    'properties': {
                        'prop_1': {'type': 'number'}
                        ...
                    },
                    'required': ['prop_1', ...],
                    'additionalProperties': False
                }
            }
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['json_string'],
    custom_features=fiddler_custom_features,
)
```
The above example leads to creation of two columns -

| Column                          | Type  | Description                                                                                               |
| ------------------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| JSON Validator valid       | bool  | String is valid JSON. |
| JSON Validator errors | str | If the string failed to parse to JSON any parsing errors will be returned as a serialized json list of dictionaries,   |

***

### ModelTaskParams

Task parameters given to a particular model.

| Parameter                         | Type         | Default | Description                                                                         |
| --------------------------------- | ------------ | ------- | ----------------------------------------------------------------------------------- |
| binary\_classification\_threshold | float        | None    | Threshold for labels.                                                               |
| target\_class\_order              | list         | None    | Order of target classes.                                                            |
| group\_by                         | str          | None    | Query/session id column for ranking models.                                         |
| top\_k                            | int          | None    | Top k results to consider when computing ranking metrics.                           |
| class\_weights                    | list\[float] | None    | Weight of each class.                                                               |
| weighted\_ref\_histograms         | bool         | None    | Whether baseline histograms must be weighted or not when calculating drift metrics. |

### ModelSchema

Model schema defines the list of columns associated with a model version.

| Parameter       | Type                                      | Default | Description      |
| --------------- | ----------------------------------------- | ------- | ---------------- |
| schema\_version | int                                       | 1       | Schema version.  |
| columns         | list\[[Column](api-methods-30.md#column)] | None    | List of columns. |

### ModelSpec

Model spec defines how model columns are used along with model task.

| Parameter        | Type                                                    | Default | Description                 |
| ---------------- | ------------------------------------------------------- | ------- | --------------------------- |
| schema\_version  | int                                                     | 1       | Schema version.             |
| inputs           | list\[str]                                              | None    | Feature columns.            |
| outputs          | list\[str]                                              | None    | Prediction columns.         |
| targets          | list\[str]                                              | None    | Label columns.              |
| decisions        | list\[str]                                              | None    | Decisions columns.          |
| metadata         | list\[str]                                              | None    | Metadata columns            |
| custom\_features | list\[[CustomFeature](api-methods-30.md#customfeature)] | None    | Custom feature definitions. |

### CustomFeature

The base class for derived features such as Multivariate, VectorFeature, etc.

| Parameter   | Type                                                     | Default | Description                                                                                 |
| ----------- | -------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------- |
| name        | str                                                      | None    | The name of the custom feature.                                                             |
| type        | [CustomFeatureType](api-methods-30.md#customfeaturetype) | None    | The type of custom feature. Must be one of the `CustomFeatureType` enum values.             |
| n\_clusters | Optional\[int]                                           | 5       | The number of clusters.                                                                     |
| centroids   | Optional\[List]                                          | None    | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters`. |

**Multivariate**

Represents custom features derived from multiple columns.

| Parameter           | Type                                                     | Default                         | Description                                                                                                                                |
| ------------------- | -------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| type                | [CustomFeatureType](api-methods-30.md#customfeaturetype) | CustomFeatureType.FROM\_COLUMNS | Indicates this feature is derived from multiple columns.                                                                                   |
| columns             | List\[str]                                               | None                            | List of original columns from which this feature is derived.                                                                               |
| monitor\_components | bool                                                     | False                           | Whether to monitor each column in `columns` as individual feature. If set to `True`, components are monitored and drift will be available. |

**VectorFeature**

Represents custom features derived from a single vector column.

| Parameter      | Type                                                     | Default                        | Description                                                                 |
| -------------- | -------------------------------------------------------- | ------------------------------ | --------------------------------------------------------------------------- |
| type           | [CustomFeatureType](api-methods-30.md#customfeaturetype) | CustomFeatureType.FROM\_VECTOR | Indicates this feature is derived from a single vector column.              |
| source\_column | Optional\[str]                                           | None                           | Specifies the original column if this feature is derived from an embedding. |
| column         | str                                                      | None                           | The vector column name.                                                     |

**TextEmbedding**

Represents custom features derived from text embeddings.

| Parameter | Type                                                     | Default                                 | Description                                                                                                      |
| --------- | -------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| type      | [CustomFeatureType](api-methods-30.md#customfeaturetype) | CustomFeatureType.FROM\_TEXT\_EMBEDDING | Indicates this feature is derived from a text embedding.                                                         |
| n\_tags   | Optional\[int]                                           | 5                                       | How many tags(tokens) the text embedding uses in each cluster as the `tfidf` summarization in drift computation. |

**ImageEmbedding**

Represents custom features derived from image embeddings.

| Parameter | Type                                                     | Default                                  | Description                                                |
| --------- | -------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------- |
| type      | [CustomFeatureType](api-methods-30.md#customfeaturetype) | CustomFeatureType.FROM\_IMAGE\_EMBEDDING | Indicates this feature is derived from an image embedding. |

**Enrichment**

Represents custom features derived from enrichment.

| Parameter  | Type                                                     | Default                      | Description                                                       |
| ---------- | -------------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------- |
| type       | [CustomFeatureType](api-methods-30.md#customfeaturetype) | CustomFeatureType.ENRICHMENT | Indicates this feature is derived from enrichment.                |
| columns    | List\[str]                                               | None                         | List of original columns from which this feature is derived.      |
| enrichment | str                                                      | None                         | A string identifier for the type of enrichment to be applied.     |
| config     | Dict\[str, Any]                                          | None                         | A dictionary containing configuration options for the enrichment. |

### XaiParams

Represents the explainability parameters.

| Parameter                | Type           | Default | Description                                                                     |
| ------------------------ | -------------- | ------- | ------------------------------------------------------------------------------- |
| custom\_explain\_methods | List\[str]     | None    | User-defined explain\_custom methods of the model object defined in package.py. |
| default\_explain\_method | Optional\[str] | NOne    | Default explanation method.                                                     |

### DeploymentParams

Deployment parameters of a particular model.

| Parameter        | Type                                               | Default                                                        | Description                                                                                                                                                                         |
| ---------------- | -------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| artifact\_type   | str                                                | [ArtifactType.PYTHON\_PACKAGE](api-methods-30.md#artifacttype) | Type of artifact upload.                                                                                                                                                            |
| deployment\_type | [DeploymentType](api-methods-30.md#deploymenttype) | None                                                           | Type of deployment.                                                                                                                                                                 |
| image\_uri       | Optional\[str]                                     | md-base/python/python-311:1.0.0                                | A Docker image reference. See available images [here](../product-guide/explainability/flexible-model-deployment/). |
| replicas         | Optional\[str]                                     | 1                                                              | The number of replicas running the model. Minimum value: 1 Maximum value: 10 Default value: 1                                                                                       |
| cpu              | Optional\[str]                                     | 100                                                            | The amount of CPU (milli cpus) reserved per replica. Minimum value: 10 Maximum value: 4000 (4vCPUs) Default value: 100                                                              |
| memory           | Optional\[str]                                     | 256                                                            | The amount of memory (mebibytes) reserved per replica. Minimum value: 150 Maximum value: 16384 (16GiB) Default value: 256                                                           |

### RowDataSource

Explainability input source for row data.

| Parameter | Type | Default | Description                        |
| --------- | ---- | ------- | ---------------------------------- |
| row       | Dict | None    | Dictionary containing row details. |

### EventIdDataSource

Explainability input source for event data.

| Parameter | Type                                 | Default | Description                |
| --------- | ------------------------------------ | ------- | -------------------------- |
| event\_id | str                                  | None    | Unique ID for event.       |
| env\_id   | Optional\[Union\[str, UUID]]         | None    | Unique ID for environment. |
| env\_type | [EnvType](api-methods-30.md#envtype) | None    | Environment type.          |

### DatasetDataSource

Reference data source for explainability.

| Parameter    | Type                                 | Default | Description                                  |
| ------------ | ------------------------------------ | ------- | -------------------------------------------- |
| env\_type    | [EnvType](api-methods-30.md#envtype) | None    | Environment type.                            |
| num\_samples | Optional\[int]                       | None    | Number of samples to select for computation. |
| env\_id      | Optional\[Union\[str, UUID]]          | None    | Unique ID for environment.                   |

***

## Helper functions

### set\_logging

Set app logger at given log level.

**Parameters**

| Parameter | Type | Default      | Description                              |
| --------- | ---- | ------------ | ---------------------------------------- |
| level     | int  | logging.INFO | Logging level from python logging module |

**Usage**

```python
set_logging(logging.INFO)
```

**Returns**

None

### group\_by

Group the events by a column. Use this method to form the grouped data for ranking models.

**Parameters**

| Parameter      | Type           | Default | Description                           |
| -------------- | -------------- | ------- | ------------------------------------- |
| df             | pd.DataFrame   | -       | Unique identifier for the AlertRule. |
| group\_by\_col | str            | -       | The column to group the data by.      |
| output\_path   | Optional\[Path | str]    | -                                     |

**Usage**

```python
COLUMN_NAME = 'col_2'

grouped_df = group_by(df=df, group_by_col=COLUMN_NAME)
```

**Returns**

| Return Type  | Description                  |
| ------------ | ---------------------------- |
| pd.Dataframe | Dataframe in grouped format. |
