---
title: "fdl.DeploymentType"
slug: "fdldeploymenttype"
excerpt: "Represents supported Deployment type"
hidden: true
createdAt: "2023-08-07T15:02:09.548Z"
updatedAt: "2023-08-07T15:20:07.425Z"
---
| Enum Value                        | Description                                                                                                                                                                  |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fdl.DeploymentType.BASE_CONTAINER | Default mode for deploying a model artifact or surrogate.                                                                                                                    |
| fdl.DeploymentType.MANUAL         | Deploy a model in MANUAL mode (used in On-prem seeting only, if permissions are not given). Please check this [section](doc:manual-flexible-model-deployment) for more info. |

```python Usage
deployment_type = fdl.DeploymentType.MANUAL
```