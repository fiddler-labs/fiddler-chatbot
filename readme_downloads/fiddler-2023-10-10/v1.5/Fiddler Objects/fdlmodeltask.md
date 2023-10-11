---
title: "fdl.ModelTask"
slug: "fdlmodeltask"
excerpt: "Represents supported model tasks"
hidden: false
createdAt: "2022-05-25T14:56:32.969Z"
updatedAt: "2022-05-25T14:56:32.969Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Enum Value",
    "h-1": "Description",
    "0-0": "fdl.ModelTask.REGRESSION",
    "0-1": "For tabular models.",
    "1-0": "fdl.ModelTask.BINARY_CLASSIFICATION",
    "1-1": "For binary classification models",
    "2-0": "fdl.ModelTask.MULTICLASS_CLASSIFICATION",
    "3-0": "fdl.ModelTask.RANKING",
    "2-1": "For multiclass classification models",
    "3-1": "For ranking classification models"
  },
  "cols": 2,
  "rows": 4
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "model_task = fdl.ModelTask.BINARY_CLASSIFICATION",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]