---
title: "Release 22.12 Notes"
slug: "release-notes-2022-2-10"
type: ""
createdAt: {}
hidden: false
---
This page enumerates the new features and updates in this release of the Fiddler platform.

## Release of Fiddler platform version 22.12:

- Scale & performance improvements

- Alert on Metadata Columns

- New API for updating existing model artifacts or surrogate models

## What's New and Improved:

- **Scale and performance improvements for monitoring metrics**
  - Significant service refactoring for faster computing of monitoring metrics

- **Support for setting monitoring alerts on metadata columns**
  - Ability to configure Data Drift and Data Integrity alerts on metadata columns

- **Support for updating existing model artifacts or surrogate models to user-uploaded models**
  - The [`update_model_artifact`](ref:clientupdate_model_artifact) method allows you to modify existing surrogate or user-uploaded models with new user uploaded-models. This will be replacing the previously used `update_model` method
  - Read the [API Reference Documentation](https://docs.fiddler.ai/reference/clientupdate_model_artifact) to learn more

### Client Version

Client version 1.6 is required for the updates and features mentioned in this release.