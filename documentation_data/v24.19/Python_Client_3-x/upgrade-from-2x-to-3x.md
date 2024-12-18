---
title: Upgrade from 2.x to 3.x
slug: upgrade-from-2x-to-3x
excerpt: ''
createdAt: Tue Apr 23 2024 19:33:10 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri May 03 2024 14:26:20 GMT+0000 (Coordinated Universal Time)
---

# Upgrade from 2.x To 3.x

With Platform Version `24.4` bringing changes in the model onboarding flow, the Python client has been upgraded to reflect these changes using an object-oriented design. This article is a guide on how your existing 2.x API method calls change when upgrading to Fiddler Python client 3.x. Please note that the below 3.x methods are more fully documented in [API documentation](api-methods-30.md). You can also take a look at this [notebook](https://drive.google.com/file/d/1g1ldfxaDnY7zokewFTnqnYbQcTgF72fT/view?usp=sharing) which walks you through usage changes with the new client

### Notable Changes

* **Dataset management**: In client 3.x and platform 24.4+, the dataset is a model asset rather than a project asset. Multiple datasets can be associated with a model for different purposes like feature impact computation or surrogate model generation.
* **Explicit triggering**: In client 3.x, actions such as feature importance and impact computation must be triggered explicitly unlike in client 2.x where they were part of the add artifact/surrogate model methods.
* **Onboarding prerequisites**: A dataset is no longer a perquisite for onboarding a model into Fiddler and the DatasetInfo object has been deprecated.
*   **Naming conventions**: In client 2.x API method parameters for unique identifiers used semantic names such as project\_id='my\_project' and model\_id='my\_model'. With client 3.x we will expose automatically generated unique identifiers for objects like projects and models. This unique identifier is what is to be used for any "id" or "\_id" parameter. Your semantic names will be associated with an object's "name" parameter and will allow retrieval by your semantic name in addition to get by "id".

    **Flow Changes**

    **Import**

    * **2.x**: `import fiddler as fdl`
    * **3.x**: `import fiddler as fdl`

    **Initialization**

    *   **2.x**:

        ```python
        client = fdl.FiddlerApi(
            url=URL,
            org_id=ORG_ID,
            auth_token=AUTH_TOKEN
        )
        ```
    *   **3.x**:

        ```python
        fdl.init(
            url=URL,
            token=AUTH_TOKEN
        )
        ```

        `org_id` is no longer required and will be inferred from the token.

    **Projects**

    **Get Projects**

    * **2.x**: `projects = client.get_projects()`
    * **3.x**: `projects = fdl.Project.list()`

    **Add Project**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'

        project = client.create_project(project_id=PROJECT_ID)
        ```
    *   **3.x**:

        ```python
        PROJECT_NAME = 'YOUR_PROJECT_NAME'

        project = fdl.Project(name=PROJECT_NAME)
        project.create()
        ```

    **Delete Project**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'

        client.delete_project(project_id=PROJECT_ID)
        ```
    *   **3.x**:

        ```python
        PROJECT_NAME = 'YOUR_PROJECT_NAME'

        project = fdl.Project.from_name(name=PROJECT_NAME)
        project.delete()
        ```

    **Models**

    **Get Model**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'

        model = client.get_model(
            project_id=PROJECT_ID,
            model_id=MODEL_ID
        )
        ```
    *   **3.x**:

        ```python
        PROJECT_NAME = 'YOUR_PROJECT_NAME'
        MODEL_NAME = 'YOUR_MODEL_NAME'

        project = fdl.Project.from_name(name=PROJECT_NAME)
        model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)
        ```

    **List Models**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'

        models = client.list_models(project_id=PROJECT_ID))
        ```
    *   **3.x**:

        ```python
        PROJECT_ID = '6dbf8656-1b6b-4f80-ba2b-b75739526dc2'

        models = fdl.Model.list(project_id=PROJECT_ID)
        ```

    **Add Model**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        DATASET_ID = 'YOUR_DATASET_NAME'

        client.add_model(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID,
            model_id=MODEL_ID,
            model_info=model_info
        )
        ```
    *   **3.x**:

        ```python
        DATASET_FILE_PATH = <path_to_file>
        MODEL_NAME = 'YOUR_MODEL_NAME'
        PROJECT_ID = '6dbf8656-1b6b-4f80-ba2b-b75739526dc2'

        MODEL_SPEC = fdl.ModelSpec(
            inputs=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance'],
            outputs=['probability_churned'],
            targets=['Churned'],
            decisions=[],
            metadata=[],
            custom_features=[],
        )

        model = fdl.Model.from_data(
            source=DATASET_FILE_PATH,
            name=MODEL_NAME,
            project_id=PROJECT_ID,
            spec=MODEL_SPEC,
        )
        model.create()
        ```

    \\

    **Add Model Artifact**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        MODEL_DIR = <path_to_dir_containing_artifact>
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        job_id = client.add_model_artifact(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            model_dir=MODEL_DIR,
            deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}
        MODEL_DIR = <path_to_dir_containing_artifact>

        model = fdl.Model.get(id_=MODEL_ID)
        job = model.add_artifact(
                model_dir=MODEL_DIR,
                deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
              )
        job.wait()
        ```

    > 📘 Computation of Feature Importance
    >
    > Pre-compute of feature importance and feature impact needs to be done manually in 3.x. Below blocks showcase how it can be done with client 3.x

    *   **3.x**: **New steps**

        ```python
        DATASET_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'

        importance_job = model.precompute_feature_importance(
                  dataset_id=DATASET_ID
              )
        importance_job.wait()

        impact_job = model.precompute_feature_impact(
                  dataset_id=DATASET_ID
              )
        impact_job.wait()
        ```

    **Update Model**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'

        models = client.update_model(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        model = fdl.Model.get(id_=MODEL_ID)
        model.xai_params.default_explain_method = 'SHAP'
        model.update()
        ```

    **Update Model Artifact**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        MODEL_DIR = <path_to_dir_containing_artifact>
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        job_id = client.update_model_artifact(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            model_dir=MODEL_DIR,
            deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}
        MODEL_DIR = <path_to_dir_containing_artifact>

        model = fdl.Model.get(id_=MODEL_ID)
        job = model.update_artifact(
                model_dir=MODEL_DIR,
                deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS)
              )
        job.wait()
        ```

    \\

    > 📘 Computation of Feature Importance
    >
    > Pre-compute of feature importance and feature impact needs to be done manually in 3.x. Below blocks showcase how it can be done with client 3.x

    *   **3.x**: **New steps**

        ```python
        DATASET_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'

        importance_job = model.precompute_feature_importance(
                  dataset_id=DATASET_ID
              )
        importance_job.wait()

        impact_job = model.precompute_feature_impact(
                  dataset_id=DATASET_ID
              )
        impact_job.wait()
        ```

    **Download Artifacts**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        OUTPUT_DIR = <path_to_dir_to_download_artifact>

        client.download_artifacts(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            output_dir=OUTPUT_DIR
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        OUTPUT_DIR = <path_to_dir_to_download_artifact>

        model = fdl.Model.get(id_=MODEL_ID)
        model.download_artifact(
            output_dir=OUTPUT_DIR
        )
        ```

    **Get Model Deployment**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'

        model_deployment = client.get_model_deployment(
                              project_id=PROJECT_ID,
                              model_id=MODEL_ID
                          )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        # Using Model
        model = fdl.Model.get(id_=MODEL_ID)
        model_deployment = model.deployment

        # Using ModelDeployment
        model_deployment = fdl.ModelDeployment.of(model_id=MODEL_ID)
        ```

    **Add Model Surrogate**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        job_id = client.add_model_surrogate(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        DATASET_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        model = fdl.Model.get(id_=MODEL_ID)
        job = model.add_surrogate(
                dataset_id=DATASET_ID,
                deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        job.wait()
        ```

    **Update Model Surrogate**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        job_id = client.update_model_surrogate(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        DATASET_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'
        DEPLOYMENT_PARAMS = {'deployment_type': 'MANUAL', 'cpu': 1000}

        model = fdl.Model.get(id_=MODEL_ID)
        job = model.update_surrogate(
                dataset_id=DATASET_ID,
                deployment_params=fdl.DeploymentParams(**DEPLOYMENT_PARAMS))
        job.wait()
        ```

    **Update Model Deployment**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'

        model_deployment = client.update_model_deployment(
                              project_id=PROJECT_ID,
                              model_id=MODEL_ID,
                              cpu=1000
                          )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        model_deployment = fdl.ModelDeployment.of(
                            model_id=MODEL_ID
                           )
        model_deployment.cpu = 1000
        model_deployment.update()
        ```

    **Delete Model**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'

        client.delete_model(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
        )
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        model = fdl.Model.get(id_=MODEL_ID)
        job = model.delete()
        job.wait()
        ```

    **Datasets**

    **Get Dataset**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        DATASET_ID = 'YOUR_MODEL_NAME'

        dataset = client.get_dataset(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID
        )
        ```
    *   **3.x**:

        ```python
        # From id
        DATASET_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'
        dataset = fdl.Dataset.get(id_=DATASET_ID)

        # From name
        DATASET_NAME = 'test_dataset'
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        dataset = fdl.Dataset.from_name(
              name=DATASET_NAME,
              model_id=MODEL_ID
        )
        ```

    **List Datasets**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        datasets = client.list_datasets(project_id=PROJECT_ID)
        ```
    *   **3.x**:

        ```python
        # In 3.x, datasets are stored at a model level rather than project level.
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        datasets = fdl.Dataset.list(model_id=MODEL_ID)
        ```

    **Upload Dataset**

    *   **2.x**:

        ```python
        baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
        dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df)

        PROJECT_ID = 'YOUR_PROJECT_NAME'
        DATASET_ID = 'YOUR_MODEL_NAME'

        client.upload_dataset(
            project_id=PROJECT_ID,
            dataset_id=DATASET_ID,
            dataset={
                'baseline': baseline_df
            },
            info=dataset_info
        )
        ```
    *   **3.x**:

        ```python
        # Fiddler no longer requires a dataset to be added before model creation.
        # However, you can optionally add upload dataset to a model using the
        # publish method as shown below.
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        DATASET_NAME = 'YOUR_DATASET_NAME'
        DATASET_FILE_PATH = <path_to_dataset>

        job = model.publish(
            source=DATASET_FILE_PATH,
            environment=fdl.EnvType.PRE_PRODUCTION,
            dataset_name=DATASET_NAME,
        )
        # The publish() method is asynchronous by default as in previous versions. 
        # Use the publish job's wait() method if synchronous behavior is desired.
        # job.wait()        
        ```

    **Baselines**

    **Get Baseline**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        DATASET_ID = 'YOUR_MODEL_NAME'
        BASELINE_ID = 'YOUR_BASELINE_NAME'

        baseline = client.get_baseline(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            baseline_id=BASELINE_ID
        )
        ```
    *   **3.x**:

        ```python
        # From UUID
        BASELINE_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'
        baseline = fdl.Baseline.get(id_=BASELINE_ID)

        # From name
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
        BASELINE_NAME = 'YOUR_BASELINE_NAME'

        baseline = fdl.Baseline.from_name(
              name=BASELINE_NAME,
              model_id=MODEL_ID
        )
        ```

    **Add Baseline**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        BASELINE_ID = 'YOUR_BASELINE_NAME'
        DATASET_ID = 'YOUR_DATASET_NAME'

        # Static baseline
        baseline = client.add_baseline(
              project_id=PROJECT_ID,
              model_id=MODEL_ID,
              baseline_id=BASELINE_ID,
              type=fdl.BaselineType.STATIC,
              dataset_id=DATASET_ID
        )

        # Rolling baseline
        baseline = client.add_baseline(
              project_id=PROJECT_ID,
              model_id=MODEL_ID,
              baseline_id=BASELINE_NAME,
              type=fdl.BaselineType.ROLLING_PRODUCTION,
              offset=fdl.WindowSize.ONE_MONTH, # How far back to set our window
              window_size=fdl.WindowSize.ONE_WEEK, # Size of the sliding window
        )
        ```
    *   **3.x**:

        ```python
        BASELINE_NAME = 'YOUR_BASELINE_NAME'
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        # Static baseline
        baseline = fdl.Baseline(
            name=BASELINE_NAME,
            model_id=MODEL_ID,
            environment=fdl.EnvType.PRE_PRODUCTION,
            type_=fdl.BaselineType.STATIC,
            dataset_id=DATASET_ID,
        )
        baseline.create()

        # Rolling baseline
        baseline = fdl.Baseline(
            name=BASELINE_NAME,
            model_id=MODEL_ID,
            environment=fdl.EnvType.PRODUCTION,
            type_=fdl.BaselineType.ROLLING,
            window_bin_size=fdl.WindowBinSize.HOUR,
            offset_delta=fdl.WindowBinSize.HOUR,
        )
        baseline.create()
        ```

    **List Baselines**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'

        baselines = client.list_baselines(project_id=PROJECT_ID)
        ```
    *   **3.x**:

        ```python
        MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

        baselines = fdl.Baseline.list(model_id=MODEL_ID)
        ```

    **Delete Baselines**

    *   **2.x**:

        ```python
        PROJECT_ID = 'YOUR_PROJECT_NAME'
        MODEL_ID = 'YOUR_MODEL_NAME'
        BASELINE_ID = 'YOUR_BASELINE_NAME'

        client.delete_baseline(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            baseline_id=BASELINE_ID
        )
        ```
    *   **3.x**:

        ```python
        BASELINE_ID = '5e1e67d2-5170-45ce-a851-68bdde1ac1ad'

        baseline = fdl.Baseline.get(id_=BASELINE_ID)
        baseline.delete()
        ```

    **Event Publishing**

    > 📘 Source
    >
    > In 3.x, an event data source for batch publishing can be one of CSV filepath, parquet filepath, or Pandas dataframe and a Python list\[dict] for streaming publishing.

    **Publish batch production events**

    *   **Pre-requisite**:

        ```python
          PROJECT_ID = 'YOUR_PROJECT_NAME'
          MODEL_ID = 'YOUR_MODEL_NAME'
          production_df = pd.read_csv(PATH_TO_EVENTS_CSV)
        ```
    *   **2.x**:

        ```python
        job = client.publish_events_batch(
            project_id=PROJECT_ID,
            model_id=MODEL_ID,
            id_field='event_id',
            batch_source=production_df,
            timestamp_field='timestamp',
            update_event=False,
        )
        ```
    *   **3.x**:

        ```python
        # Instantiate project and model object in 3.x
        project = fdl.Project.from_name(name=PROJECT_ID)
        model = fdl.Model.from_name(project_id=project.id, name=MODEL_ID)

        # One-time only on migration from v1/v2: Before publishing events, update your model
        # with the event unique identifier and event timestamp as these are now Model properties
        # instead of publish() method parameters.
        model.event_ts_col = 'timestamp'
        model.event_id_col = 'event_id'
        model.update()

        job = model.publish(source=production_df, update=False)
        # The publish() method is asynchronous by default as in previous versions. 
        # Use the publish job's wait() method if synchronous behavior is desired.
        # job.wait() 
        ```

        For examples of updating labels in 3.x, refer to [publish](api-methods-30.md#publish) API documentation.

    **Publish Production Events Streaming**

    * **Pre-requisite**:

    ```python
      PROJECT_ID = 'YOUR_PROJECT_NAME'
      MODEL_ID = 'YOUR_MODEL_NAME'
      event_dict = [{
        'A': [0], 
        'B': [0], 
      }]
      event_id = 7342881 
      event_time = '2024-05-01 00:00:00' 
    ```

    * **2.x**:

    ```python
    client.publish_event(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        event=event_dict,
        event_timestamp=event_time,
        event_id=event_id,
        update_event= False
    )
    ```

    * **3.x**:

    ```python
    # setup project and model object in 3.x
    project = fdl.Project.from_name(name=PROJECT_ID)
    model = fdl.Model.from_name(project_id=project.id, name=MODEL_ID)

    # One-time only on migration from v1/v2: Before publishing events, update your model
    # with the event unique identifier and event timestamp as these are now Model properties
    # instead of publish() method parameters.
    model.event_ts_col = 'timestamp'
    model.event_id_col = 'event_id'
    model.update()

    # Add the event_id and timestamp fields to every event to be updated. Alternatively, alter 
    # your data pipeline to include these fields on the event dictionary sent to Fiddler 
    # to avoid the following step.
    event_dict['event_id'] = event_id
    event_dict['timestamp'] = event_time

    # The source accepts a list of 1 or more dictionaries
    model.publish(source=[event_dict])
    ```

    **Custom Metrics**

    **Get Custom Metric**

    * **2.x**:

    ```python
    CUSTOM_METRIC_ID = 'YOUR_METRIC_NAME'

    client.get_custom_metric(metric_id=METRIC_ID)
    ```

    * **3.x**:

    ```python
    # From UUID
    CUSTOM_METRIC_ID = '7057867c-6dd8-4915-89f2-a5f253dd4a3a'
    custom_metric = fdl.CustomMetric.get(id_=CUSTOM_METRIC_ID)

    # From name
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    CUSTOM_METRIC_NAME = 'YOUR_METRIC_NAME'

    custom_metric = fdl.CustomMetric.from_name(
            name=CUSTOM_METRIC_NAME,
            model_id=MODEL_ID,
        )
    ```

    **List Custom Metrics**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    client.get_custom_metrics(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    custom_metrics = fdl.CustomMetric.list(model_id=MODEL_ID)
    ```

    **Add Custom Metric**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'
    CUSTOM_METRIC_NAME = 'YOUR_METRIC_NAME'
    DEFINITION = 'average("Age")'
    DESCRIPTION = 'Testing custom metrics'

    client.get_custom_metrics(
        name=CUSTOM_METRIC_NAME,
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        definition=DEFINITION,
        description=DESCRIPTION,
    )
    ```

    * **3.x**:

    ```python
    CUSTOM_METRIC_NAME = 'YOUR_METRIC_NAME'
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    DEFINITION = 'average("Age")'
    DESCRIPTION = 'Testing custom metrics'

    custom_metric = fdl.CustomMetric(
        name=CUSTOM_METRIC_NAME,
        model_id=MODEL_ID,
        definition=DEFINITION,
        description=DESCRIPTION,
    )
    custom_metric.create()
    ```

    **Delete Custom Metric**

    * **2.x**:

    ```python
    CUSTOM_METRIC_ID = 'YOUR_METRIC_NAME'

    client.delete_custom_metric(metric_id=METRIC_ID)
    ```

    * **3.x**:

    ```python
    CUSTOM_METRIC_ID = '7057867c-6dd8-4915-89f2-a5f253dd4a3a'

    custom_metric = fdl.CustomMetric.get(id_=CUSTOM_METRIC_ID)
    custom_metric.delete()
    ```

    **Segments**

    **Get Segment**

    * **2.x**:

    ```python
    SEGMENT_ID = 'YOUR_SEGMENT_NAME'

    client.get_segment(segment_id=SEGMENT_ID)
    ```

    * **3.x**:

    ```python
    # From UUID
    SEGMENT_ID = '2c22a28b-08b8-4dd6-9238-7d7f1b5b4cb7'
    segment = fdl.Segment.get(id_=SEGMENT_ID)

    # From name
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    SEGMENT_NAME = 'YOUR_SEGMENT_NAME'

    segment = fdl.Segment.from_name(
        name=SEGMENT_NAME,
        model_id=MODEL_ID,
    )
    ```

    **List Segments**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    client.get_segments(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = '2c22a28b-08b8-4dd6-9238-7d7f1b5b4cb7'

    segment = fdl.Segment.list(model_id=MODEL_ID)
    ```

    **Add Segment**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'
    SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
    DEFINITION = 'Age < 60'
    DESCRIPTION = 'Testing segment'

    client.add_segment(
        name=SEGMENT_NAME,
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        definition=DEFINITION,
        description=DESCRIPTION,
    )
    ```

    * **3.x**:

    ```python
    SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    DEFINITION = 'Age < 60'
    DESCRIPTION = 'Testing segment'

    segment = fdl.Segment(
        name=SEGMENT_NAME,
        model_id=MODEL_ID,
        definition=DEFINITION,
        description=DESCRIPTION
    )
    segment.create()
    ```

    **Delete Segment**

    * **2.x**:

    ```python
    SEGMENT_ID = 'YOUR_SEGMENT_NAME'
    client.delete_segment(
      segment_id=SEGMENT_ID
    )
    ```

    * **3.x**:

    ```python
    SEGMENT_ID = '2c22a28b-08b8-4dd6-9238-7d7f1b5b4cb7'

    segment = fdl.Segment.get(id_=SEGMENT_ID)
    segment.delete()
    ```

    **Alerts**

    **List Alert Rules**

    * **2.x**:

    ```python
    MODEL_ID = 'YOUR_MODEL_NAME'

    rules = client.get_alert_rules(model_id=MODEL_ID)
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    rules = fdl.AlertRule.list(model_id=MODEL_ID)
    ```

    \\

    **Add Alert Rule**

    * **2.x**:

    ```python
    notifications_config = client.build_notifications_config(
        emails = "name@google.com",
    )
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    rule = client.add_alert_rule(
        name = "Bank Churn Range Violation Alert1",
        project_id = PROJECT_ID,
        model_id = MODEL_ID,
        alert_type = fdl.AlertType.DATA_INTEGRITY,
        metric = fdl.Metric.RANGE_VIOLATION,
        bin_size = fdl.BinSize.ONE_DAY,
        compare_to = fdl.CompareTo.RAW_VALUE,
        compare_period = None,
        priority = fdl.Priority.HIGH,
        warning_threshold = 2,
        critical_threshold = 3,
        condition = fdl.AlertCondition.GREATER,
        column = "numofproducts",
        notifications_config = notifications_config
    )
    ```

    * **3.x**:

    ```python
    ALERT_NAME = 'YOUR_ALERT_NAME'
    METRIC_NAME = 'null_violation_count'
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    rule = fdl.AlertRule(
      name=ALERT_NAME,
      model_id=MODEL_ID,
      metric_id=METRIC_NAME,
      priority=fdl.Priority.MEDIUM,
      compare_to=fdl.CompareTo.RAW_VALUE,
      condition=fdl.AlertCondition.GREATER,
      bin_size=fdl.BinSize.HOUR,
      critical_threshold=1,
      warning_threshold=0.32,
    )
    rule.create()
    ```

    **Delete Alert Rule**

    * **2.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    client.delete_alert_rule(alert_rule_uuid=ALERT_RULE_ID)
    ```

    * **3.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    rule = fdl.AlertRule.get(id_=ALERT_RULE_ID)
    rule.delete()
    ```

    \\

    **Get Triggered Alerts**

    * **2.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    rules = client.get_triggered_alerts(alert_rule_uuid=ALERT_RULE_ID)
    ```

    * **3.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    rules = fdl.AlertRecord.list(
        alert_rule_id=ALERT_RULE_ID,
        start_time=datetime(),
        end_time=datetime()
    )
    ```

    **Enable Notifications**

    * **2.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    notifications = client.update_alert_rule(
        alert_config_uuid=ALERT_RULE_ID,
        enable_notification=True
    )
    ```

    * **3.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    rule = fdl.AlertRule.get(id_=ALERT_RULE_ID)
    rule.enable_notifications()
    ```

    **Disable Notifications**

    * **2.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    notifications = client.update_alert_rule(
        alert_config_uuid=ALERT_RULE_ID,
        enable_notification=False
    )
    ```

    * **3.x**:

    ```python
    ALERT_RULE_ID = '31109d19-b8aa-4db0-a4d5-aa0706987b1b'

    rule = fdl.AlertRule.get(id_=ALERT_RULE_ID)
    rule.disable_notifications()
    ```

    **Webhooks**

    **Get Webhook**

    * **2.x**:

    ```python
    WEBHOOK_UUID = '00cb3169-7983-497c-8f3c-d25df26543b0'

    webhook = client.get_webhook(uuid=WEBHOOK_UUID)
    ```

    * **3.x**:

    ```python
    WEBHOOK_ID = '00cb3169-7983-497c-8f3c-d25df26543b0'

    webhook = fdl.Webhook.get(id_=WEBHOOK_ID)
    ```

    **List Webhooks**

    * **2.x**:

    ```python
    webhooks = client.get_webhooks()
    ```

    * **3.x**:

    ```python
    webhooks = fdl.Webhook.list()
    ```

    **Add Webhook**

    * **2.x**:

    ```python
    WEBHOOK_NAME = 'YOUR_WEBHOOK_NAME'
    WEBHOOK_URL = 'https://hooks.slack.com/services/T9EAVLUQ5/xxxxxxxxxx'
    WEBHOOK_PROVIDER = 'SLACK'

    webhook = client.add_webhook(
        name=WEBHOOK_NAME,
        url=WEBHOOK_URL,
        provider=WEBHOOK_PROVIDER
    )
    ```

    * **3.x**:

    ```python
    WEBHOOK_NAME = 'YOUR_WEBHOOK_NAME'
    WEBHOOK_URL = 'https://hooks.slack.com/services/xxxxxxxxxx'
    WEBHOOK_PROVIDER = 'SLACK'

    webhook = fdl.Webhook(
        name=WEBHOOK_NAME,
        url=WEBHOOK_URL,
        provider=WEBHOOK_PROVIDER
    )
    webhook.create()
    ```

    **Update Webhook**

    * **2.x**:

    ```python
    WEBHOOK_UUID = '00cb3169-7983-497c-8f3c-d25df26543b0'
    WEBHOOK_NAME = 'YOUR_WEBHOOK_NAME'
    WEBHOOK_URL = 'https://hooks.slack.com/services/xxxxxxxxxx'
    WEBHOOK_PROVIDER = 'SLACK'

    webhook = client.update_webhook(
      uuid=WEBHOOK_UUID,
      name=WEBHOOK_NAME,
      url=WEBHOOK_URL,
      provider=WEBHOOK_PROVIDER
    )
    ```

    * **3.x**:

    ```python
    WEBHOOK_ID = '00cb3169-7983-497c-8f3c-d25df26543b0'

    webhook = fdl.Webhook.get(id_=WEBHOOK_ID)
    webhook.name = 'YOUR_WEBHOOK_NAME_CHANGE'
    webhook.update()
    ```

    **Delete Webhook**

    * **2.x**:

    ```python
    WEBHOOK_UUID = '00cb3169-7983-497c-8f3c-d25df26543b0'

    webhook = client.delete_webhook(uuid=WEBHOOK_UUID)
    ```

    * **3.x**:

    ```python
    WEBHOOK_ID = '00cb3169-7983-497c-8f3c-d25df26543b0'

    webhook = fdl.Webhook.get(id_=WEBHOOK_ID)
    webhook.delete()
    ```

    **XAI**

    **Get Explanation**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    # RowDataSource
    explain = client.get_explanation(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      input_data_source=fdl.RowDataSource(row={})
    )
    # EventIdDataSource
    explain = client.get_explanation(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      input_data_source=fdl.EventIdDataSource()
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    # RowDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    explain = model.explain(
        input_data_source=fdl.RowDataSource(row={})
    )

    # EventIdDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    explain = model.explain(
        input_data_source=fdl.EventIdDataSource()
    )
    ```

    **Get Fairness**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    # DatasetDataSource
    fairness = client.get_fairness(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        data_source=fdl.DatasetDataSource(),
        protected_features=[],
        positive_outcome='',
    )
    # SqlSliceQueryDataSource
    fairness = client.get_fairness(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        data_source=fdl.SqlSliceQueryDataSource(),
        protected_features=[],
        positive_outcome='',
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    # DatasetDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    fairness = model.get_fairness(
        data_source=fdl.DatasetDataSource(),
        protected_features=[],
        positive_outcome='',
    )

    # SqlSliceQueryDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    fairness = model.get_fairness(
        data_source=fdl.SqlSliceQueryDataSource(),
        protected_features=[],
        positive_outcome='',
    )
    ```

    **Get Feature Impact**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    # DatasetDataSource
    impact =client.get_feature_impact(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      data_source=fdl.DatasetDataSource()
    )

    # SqlSliceQueryDataSource
    impact = client.get_feature_impact(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      data_source=fdl.SqlSliceQueryDataSource()
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    # DatasetDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    impact = model.get_feature_impact(
      data_source=fdl.DatasetDataSource()
    )

    # SqlSliceQueryDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    impact = model.get_feature_impact(
        data_source=fdl.SqlSliceQueryDataSource()
    )
    ```

    **Get Feature Importance**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'

    # DatasetDataSource
    importance = client.get_feature_importance(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      data_source=fdl.DatasetDataSource()
    )

    # SqlSliceQueryDataSource
    importance = client.get_feature_importance(
      project_id=PROJECT_ID,
      model_id=MODEL_ID,
      data_source=fdl.SqlSliceQueryDataSource()
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'

    # DatasetDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    importance = model.get_feature_importance(
            data_source=fdl.DatasetDataSource()
    )

    # SqlSliceQueryDataSource
    model = fdl.Model.get(id_=MODEL_ID)
    importance = model.get_feature_importance(
            data_source=fdl.SqlSliceQueryDataSource()
    )
    ```

    **Get Mutual Information**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    DATASET_ID = 'YOUR_DATASET_NAME'
    QUERY=f'select * from production.{MODEL_NAME} limit 10'

    mutual_info = client.get_mutual_information(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        query=QUERY,
        COLUMN_NAME=''
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    QUERY=f'select * from production.{MODEL_NAME} limit 10'

    model = fdl.Model.get(id_=MODEL_ID)
    mutual_info = model.get_mutual_info(
        query=QUERY,
        COLUMN_NAME=''
    )
    ```

    **Get Predictions**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    MODEL_ID = 'YOUR_MODEL_NAME'
    DF = <any dataframe>

    predict = client.get_predictions(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        input_df=DF
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    DF = <any dataframe>

    model = fdl.Model.get(id_=MODEL_ID)
    predict = model.predict(df=DF)
    ```

    **Get Slice**

    * **2.x**:

    ```python
    PROJECT_ID = 'YOUR_PROJECT_NAME'
    QUERY=f'select * from production.{MODEL_NAME} limit 10'

    slice = client.get_slice(
        project_id=PROJECT_ID,
        sql_query=QUERY
    )
    ```

    * **3.x**:

    ```python
    MODEL_ID = 'e38ab1ad-1a50-40b8-8bee-ab33cd8b9b93'
    QUERY=f'select * from production.{MODEL_NAME} limit 10'

    model = fdl.Model.get(id_=MODEL_ID)
    slice = model.get_slice(query=QUERY)
    ```

    **Jobs**

    **Get Job**

    * **2.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = client.get_job(uuid=JOB_ID)
    ```

    * **3.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = fdl.Job.get(id_=JOB_ID)
    ```

    **Wait for Job**

    * **2.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = client.wait_for_job(uuid=JOB_ID
    ```

    * **3.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = fdl.Job.get(id_=JOB_ID)
    job.wait()
    ```

    **Watch Job**

    * **2.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = client.watch_job(uuid=JOB_ID)
    ```

    * **3.x**:

    ```python
    JOB_ID = '904e33e0-c4a2-45ca-b8dc-43c9f3ac5519'

    job = fdl.Job.get(id_=JOB_ID)
    job.watch()
    ```



{% include "../.gitbook/includes/main-doc-dev-footer.md" %}
