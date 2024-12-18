# Python Client History

## 3.x Client Version

***

### 3.7
#### **3.7.0**

Release highlights:

* **Robustness via retrying**: this release introduces a persistent HTTP request retrying strategy to enhance fault tolerance in view of transient network problems and retryable HTTP request errors. You can take control of the maximum duration for which an HTTP request is retried by setting the environment variable `FIDDLER_CLIENT_RETRY_MAX_DURATION_SECONDS`.

* **AWS SageMaker authentication support**: to enable that, install version 2.236.0+ of the [AWS Python SageMaker SDK](https://pypi.org/project/sagemaker/). Then, before calling `init()`, set the  environment variable `AWS_PARTNER_APP_AUTH` to `true` and set `AWS_PARTNER_APP_ARN`/`AWS_PARTNER_APP_URL` to meaningful values.

* **Logging improvements**: messages are now emitted to `stderr` instead of `stdout`. Only if the calling context does not configure a root logger this library will actively declare a handler for its own log messages (this automation can be disabled by setting `auto_attach_log_handler=False` during `init()`).

Compatibility changes:

* Pydantic 2.x is now supported (and compatibility with pydantic 1.x has been retained).
* Support for Python 3.8 has been dropped.


API surface additions:

* Introduced `Project.get_or_create()` to reduce code required for instantiating a project.
* Introduced `model.remove_column()`  to allow for removing a column from a model object.

Fixes:

* A transient error during a job status update does not prematurely terminate waiting for a job anymore.
* GET requests do not contain the `Content-Type` header anymore.




### 3.6
#### **3.6.0**

* **Removed**
  * The `get_slice` and `download_slice` methods are removed. Please use `download_data` to retrieve some data.
  * The `get_mutual_info` method is removed.
  * The `SqlSliceQueryDataSource` option is removed from explain, feature impact and importance. Please use the `DatasetDataSource` instead or the UI.

### 3.5
#### **3.5.0**

* **New Features**
  * New `download_data` method, to download a slice of data given an environment, time range and segment. Resulted file can be downloaded either as a CSV or a Parquet file.

### 3.4
#### **3.4.0**

* **Removed**
  * The `get_fairness` method is removed. Please use charts and custom metrics to track / compute fairness metrics on your model.


### 3.3

#### **3.3.2**

* **Modifications**
  * Fixed the error while setting notification config for alert rule.

***

#### **3.3.1**

* **Modifications**
  * Added validation while adding notifications to alert rules.
  * Upgraded dependencies to resolve known vulnerabilities - deepdiff, mypy, pytest, pytest-mock, python-decouple, types-requests and types-simplejson.

***

#### **3.3.0**

* **New Features**
  * Introduced `upload_feature_impact()` method to upload or update feature impact manually.

***

### 3.2

#### **3.2.0**

* **New Features**
  * Introduced evaluation delay in Alerts Rule.
    * Optional `evaluation_delay` parameter added to `AlertRule.__init__` method.
    * It is used to introduce a delay in the evaluation of the alert.

* **Modifications**
  * Fix windows file permission error bug with publish method.

***

### 3.1

#### **3.1.2**

* **Modifications**
  * Adds support to get schema of Column object by `fdl.Column`

#### **3.1.1**

* **Modifications**
  * Updated `pydantic` and `typing-extensions` dependencies to support Python 3.12.

#### **3.1.0**

* **New Features**
  * Introduced the native support for model versions.
    * Optional `version` parameter added to `Model`, `Model.from_data`, `Model.from_name` methods.
    * New `duplicate()` method to seamlessly create new version from existing model.
    * Optional `name` parameter added to `Model.list` to offer the ability to list all the versions of a model.

***

### 3.0

#### **3.0.5**

* **New Features**
  * Allowed usage of `group_by()` to form the grouped data for ranking models.

#### **3.0.4**

* **Modifications**
  * Return Job in ModelDeployment update.

#### **3.0.3**

* **New Features**
  * Added `Webhook.from_name()`
* **Modifications**
  * Import path fix for packtools.

#### **3.0.2**

* **Modifications**
  * Fix pydantic issue with typing-extensions versions > 4.5.0

#### **3.0.1**

* **New Features**
  * General
    * Moving all functions of client to an Object oriented approach
    * Methods return resource object or a deserialized object wherever possible.
    * Support to search model, project, dataset, baselines by their names using `from_name()` method.
    * List methods will return iterator which handles pagination internally.
  * Data
    * Concept of environments was introduced.
    * Ability to download slice data to a parquet file.
    * Publish dataframe as stream instead of batch.
    * New methods for baselines.
    * Multiple datasets can be added to a single model. Ability to choose which dataset to use for computing feature impact / importance, surrogate generation etc.
    * Model can be added without dataset.
    * Ability to generate schema for a model.
    * Model delete is async and returns job details.
    * Added cached properties for `model`: `datasets`, `model_deployment`.
  * Alerts
    * New methods for alerts: `enable_notification`, `disable_notification`, `set_notification_config` and `get_notification_config`.
  * Explainability
    * New methods in explainability: `precompute_feature_impact`, `precompute_feature_importance`, `get_precomputed_feature_importance`, `get_precomputed_feature_impact`, `precompute_predictions`.
    * Decoupled model artifact / surrogate upload and feature impact / importance pre-computation.
* **Modifications**
  * All IDs will be UUIDs instead of strings
  * Dataset delete is not allowed anymore
