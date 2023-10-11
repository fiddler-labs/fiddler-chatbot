---
title: "Release 22.11 Notes"
slug: "release-notes-2211"
createdAt: "2022-12-15T18:36:20.125Z"
hidden: false
---
This page enumerates the new features and updates in this release of the Fiddler platform.

## Release of Fiddler platform version 22.11:

- Alert authoring and maintenance via the Fiddler Client
- New Add Model APIs via the Fiddler Client

## What's New and Improved:

- **Support for alert authoring and management via the Fiddler Client**
  - Add and delete alert rules
  - Retrieve alert rules and triggered alerts
  - Setup alert notifications via Slack, email, and PagerDuty
  - Learn more through the [API Reference Docs](https://docs.fiddler.ai/v1.5/reference/clientadd_alert_rule) and [User Guide](https://docs.fiddler.ai/v1.5/docs/alerts-client) 
- **Support for new add model APIs via the Fiddler Client **
  - Deprecated `register_model`, now using `add_model` in combination with `add_model_surrogate` instead
  - Deprecated `trigger_pre_computation`
  - Deprecated `upload_model_package`, now using `add_model_artifact`

### Client Version

Client version 1.5 is required for the updates and features mentioned in this release.