---
title: "Useful Queries for Root Cause Analysis"
slug: "useful-queries-for-root-cause-analysis"
excerpt: "This page has an examples of queries which one can use in the **Analyze** tab to perform Root Cause Analysis of an issue or look at various aspect of the data."
hidden: false
createdAt: "Wed Sep 07 2022 14:46:59 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:49:35 GMT+0000 (Coordinated Universal Time)"
---
## 1. Count of events from the previous day

In order to look at how many events were published from the previous/last publishing date, we can do it in two ways - 

### i. Jump from **Monitor** tab

This can be done in the following steps - 

1. In the monitor tab, click on the 'jump to last event' button to get to the most recent event 
2. Select the appropriate time bin, in this case, we can select **1D bin** to get day-wise aggregated data
3. Once we have the data in the chart, we can select the most recent bin
4. Select 'Export bin and feature to analyze' to jump to analyze tab

![](https://files.readme.io/54545c9-1a.png)

5. In the analyze tab, query will be auto-populated based on the **Monitor** tab selection
6. Modify the query to count the number of events from the selection 

   ```sql
   SELECT
     count(*)
   FROM
     production."bank_churn"
   WHERE
     fiddler_timestamp BETWEEN '2022-07-20 00:00:00'
     AND '2022-07-20 23:59:59'
   ```

### ii. Using `date` function in Analyze tab

To know how many events were published on the last publishing day, we can use `date` function of SQL  
Use the following query to query number of events

```sql
select
  *
from
  "production.churn_classifier_test"
where
  date(fiddler_timestamp) = (
    select
      date(max(fiddler_timestamp))
    from
      "production.churn_classifier_test"
  )
```

![](https://files.readme.io/2676acb-2.png)

## 2. Number of events on last day by output label

If we want to check how many events were published on the last day by the output class, we can use the following query 

```sql SQL
select
  churn,
  count(*)
from
  "production.churn_classifier_test"
where
  date(fiddler_timestamp) = (
    select
      date(max(fiddler_timestamp))
    from
      "production.churn_classifier_test"
  )
group by 
  churn
```

![](https://files.readme.io/29e443f-3.png)

## 3. Check events with missing values

If you want to check events where one of the columns is has null values, you can use the `isnull` function. 

```sql
SELECT
  *
FROM
  production."churn_classifier_test"
WHERE
  isnull("estimatedsalary")
LIMIT
  1000
```

![](https://files.readme.io/43c2eac-4.png)

## 4. Frequency by Categorical column

We query w.r.t to a categorical field. For example, we can count the number of events by geography which is a categorical column using the following query 

```sql
SELECT
  geography,
  count(*)
FROM
  "production.churn_classifier_test"
GROUP BY
  geography

```

![](https://files.readme.io/cbc5c25-5.png)

## 5. Frequency by Metadata

We can even query w.r.t to a metadata field. For example, if we consider gender to be a metadata column (specified in ModelInfo object), then we can obtain a frequency of events by the metadata field using the following query 

```sql
SELECT
  gender,
  count(*)
FROM
  "production.churn_classifier_test"
GROUP BY
  gender

```

![](https://files.readme.io/4e5a79d-6.png)

## Filter Events by Cluster_ID

You can query events with certain cluster_ids if you have custom features defined such as [embedding vectors](doc:vector-monitoring-platform).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0d3cfe6-Screenshot_2023-10-19_at_3.26.43_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert
