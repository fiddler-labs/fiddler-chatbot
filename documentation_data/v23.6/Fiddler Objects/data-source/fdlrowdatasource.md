---
title: "fdl.RowDataSource"
slug: "fdlrowdatasource"
excerpt: "Provides the single row to use for point explanation."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed Aug 30 2023 14:41:13 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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