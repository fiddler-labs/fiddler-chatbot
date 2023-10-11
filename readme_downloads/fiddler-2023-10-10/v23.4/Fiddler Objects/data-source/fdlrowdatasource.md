---
title: "fdl.RowDataSource"
slug: "fdlrowdatasource"
excerpt: "Provides the single row to use for point explanation."
hidden: false
createdAt: "2023-08-30T14:41:13.642Z"
updatedAt: "2023-10-05T18:49:41.097Z"
---
| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| row             | dict | None    | Single row to explain as a dictionary. |



```python Usage
row = df.to_dict(orient='records')[0]

data_source = fdl.RowDataSource(
    row=row,
)
```