---
title: "client.add_monitoring_config"
slug: "clientadd_monitoring_config"
excerpt: "Adds a custom configuration for monitoring."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 20:41:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "config_info",
    "0-1": "dict",
    "0-2": "None",
    "0-3": "Monitoring config info for an entire org or a project or a model.",
    "1-0": "project_id",
    "1-1": "Optional [str]",
    "1-2": "None",
    "1-3": "The unique identifier for the project.",
    "2-0": "model_id",
    "2-1": "Optional [str]",
    "2-2": "None",
    "2-3": "The unique identifier for the model."
  },
  "cols": 4,
  "rows": 3
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "*add_monitoring_config* can be applied at the model, project, or organization level.\n\n- If *project_id* and *model_id* are specified, the configuration will be applied at the **model** level.\n- If *project_id* is specified but model_id is not, the configuration will be applied at the **project** level.\n- If neither *project_id* nor *model_id* are specified, the configuration will be applied at the **organization** level."
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\nmonitoring_config = {\n    'min_bin_value': 3600,\n    'time_ranges': ['Day', 'Week', 'Month', 'Quarter', 'Year'],\n    'default_time_range': 7200\n}\n\nclient.add_monitoring_config(\n    config_info=monitoring_config,\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]