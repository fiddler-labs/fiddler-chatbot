---
title: "fdl.ModelTask"
slug: "fdlmodeltask"
excerpt: "Represents supported model tasks"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed May 25 2022 14:56:32 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Enum Value                              | Description                                       |
| :-------------------------------------- | :------------------------------------------------ |
| fdl.ModelTask.REGRESSION                | For regression models.                            |
| fdl.ModelTask.BINARY_CLASSIFICATION     | For binary classification models                  |
| fdl.ModelTask.MULTICLASS_CLASSIFICATION | For multiclass classification models              |
| fdl.ModelTask.RANKING                   | For ranking classification models                 |
| fdl.ModelTask.LLM                       | For LLM models.                                   |
| fdl.ModelTask.NOT_SET                   | For other model tasks or no model task specified. |

```python Usage
model_task = fdl.ModelTask.BINARY_CLASSIFICATION
```