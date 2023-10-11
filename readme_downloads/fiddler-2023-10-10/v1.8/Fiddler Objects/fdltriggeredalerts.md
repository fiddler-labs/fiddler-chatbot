---
title: "fdl.TriggeredAlerts"
slug: "fdltriggeredalerts"
excerpt: "An object containing details of a triggered alert"
hidden: false
createdAt: "2023-05-11T19:23:53.071Z"
updatedAt: "2023-05-15T17:16:04.322Z"
---
| Field                | Description                                                                                                                                                                                                                   |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                   | Integer identifier pointing to the database table row                                                                                                                                                                         |
| triggered_alert_id   | A unique identifier (UUID)                                                                                                                                                                                                    |
| alert_rule_uuid      | A unique identifier of the corresponding alert rule                                                                                                                                                                           |
| alert_run_start_time | Time in epoch milliseconds of when this alert was triggered                                                                                                                                                                   |
| alert_time_bucket    | Time in epoch milliseconds pointing to the start of the Time Bin that violated the threshold of the corresponding alert rule                                                                                                  |
| alert_value          | A float value of the metric from the Time Bin that violated the threshold of the corresponding alert rule                                                                                                                     |
| baseline_time_bucket | Applicable only when[fdl.CompareTo](ref:fdlcompareto) is 'TimePeriod'. Time in epoch milliseconds pointing to the start of the Time Bin before the compare period that violated the threshold of the corresponding alert rule |
| baseline_value       | Applicable only when [fdl.CompareTo](ref:fdlcompareto) is 'TimePeriod'. A float value of the metric from the Time Bin before compare period that violated the threshold of the corresponding alert rule                       |
| is_alert             | True, if alert notification is successfully sent, False otherwise                                                                                                                                                             |
| severity             | 'critical' if alert_value violated the critical threshold, 'warning' if alert_value violated the warning threshold, in that order                                                                                             |
| failure_reason       | String explanation of any failures while sending the alert message                                                                                                                                                            |
| message              | Alert message text                                                                                                                                                                                                            |