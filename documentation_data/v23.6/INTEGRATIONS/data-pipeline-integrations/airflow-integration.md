---
title: "Airflow Integration"
slug: "airflow-integration"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:18:03 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
Apache Airflow is an open source platform ETL platform to manage company’s complex  
workflows. Companies are increasingly integrating their ML models pipeline into Airflow DAGs to manage and monitor all the components of their ML model system.

By integrating Fiddler into an existing Airflow DAG, you will be able to train, manage, and onboard your models while  actively monitoring performance, data quality, and troubleshooting degradations across your models.

Fiddler can be easily integrated into your existing airflow DAG for ML model pipeline. A notebook which is used for publishing events can be orchestrated to run as a part of your airflow DAG using a ‘Papermill Operator’.

## Steps for the walkthrough

1. Setup airflow on your local or docker, these steps can be followed. [Link](https://airflow.apache.org/docs/apache-airflow/stable/start/index.html)

2. Add your jupyter notebook containing the code for publishing to your airflow home directory. In this example we will use the 2 different notebooks - 

   a. [Notebook to onboard ML model to Fiddler platform](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/airflow/notebooks/Fiddler_Churn_Model_Registration.ipynb)

   b. [Notebook to push production events to Fiddler platform](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/airflow/notebooks/Fiddler_Churn_Event_Publishing.ipynb)

3. Add an orchestration code to your airflow directory, airflow will pick up the orchestration code and construct a DAG as defined. The orchestration code contains the ‘papermill operator’ to orchestrate the jupyter notebooks which will be used to onboard models and publish events to Fiddler. Please refer to our [orchestration codes](https://github.com/fiddler-labs/fiddler-samples/tree/master/content_root/tutorial/integration-examples/airflow/DAGs).

4. The run interval can be set up in orchestration code as ‘schedule_interval’ in the DAG class. This interval can be based on the frequency of training and inference of your ML model.

5. Once the DAGs are set up it can be monitored on the UI. Below we can see dummy DAGs have been set up with placeholder nodes for ‘data preparation ETL’ and ‘model training/inference’. We have two DAGs - 

   a. To set up Fiddler model registration after preparing baseline data (training pipeline)

   b. To publish events to Fiddler after data preparation and ML model inference (inference pipeline)

## Label Update

An important business use case is integrating Fiddler’s ‘Label Update’ as a part of your ML workflow using Airflow. Label update can be used to update the ground truth feature in your data. This can be done using the ‘​​publish_event’ api, passing the event, event_id parameters, and making the update_event parameter as ‘True’.  
The code to update label can be found in the [notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/airflow/notebooks/Fiddler_Churn_Label_Update.ipynb)  
This notebook can be integrated to run as a part of your airflow DAG using the [sample code](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/integration-examples/airflow/DAGs/fiddler_event_update.py)

## Papermill Operator

```
operator_var = PapermillOperator(
        task_id="task_name",
        input_nb="input_jupyter_notebook",
        output_nb="output_jupyter_notebook",
        parameters={"variable_1": "{{ value }}"},
    )
```

## Airflow DAG

Below is an example of Model Registration Airflow DAG run history

![](https://files.readme.io/3fb8a21-model_registration_1.png "model_registration_1.png")

Model Registration Airflow DAG flow

![](https://files.readme.io/2891852-model_registration_2.png "model_registration_2.png")