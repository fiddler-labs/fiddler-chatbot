---
title: "client.add_monitoring_config"
slug: "clientadd_monitoring_config"
excerpt: "Adds a custom configuration for monitoring."
hidden: false
createdAt: "Mon May 23 2022 20:41:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type           | Default | Description                                                       |
| :--------------- | :------------- | :------ | :---------------------------------------------------------------- |
| config_info      | dict           | None    | Monitoring config info for an entire org or a project or a model. |
| project_id       | Optional [str] | None    | The unique identifier for the project.                            |
| model_id         | Optional [str] | None    | The unique identifier for the model.                              |

> 📘 Info
> 
> _add_monitoring_config_ can be applied at the model, project, or organization level.
> 
> - If _project_id_ and _model_id_ are specified, the configuration will be applied at the **model** level.
> - If _project_id_ is specified but model_id is not, the configuration will be applied at the **project** level.
> - If neither _project_id_ nor _model_id_ are specified, the configuration will be applied at the **organization** level.

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

monitoring_config = {
    'min_bin_value': 3600,
    'time_ranges': ['Day', 'Week', 'Month', 'Quarter', 'Year'],
    'default_time_range': 7200
}

client.add_monitoring_config(
    config_info=monitoring_config,
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```
