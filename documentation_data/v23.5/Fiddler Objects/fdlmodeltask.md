---
title: "fdl.ModelTask"
slug: "fdlmodeltask"
excerpt: "Represents supported model tasks"
hidden: false
createdAt: "2022-05-25T14:56:32.969Z"
updatedAt: "2023-10-24T04:14:06.861Z"
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