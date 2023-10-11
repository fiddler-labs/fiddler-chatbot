---
title: "Kafka Integration"
slug: "kafka-integration"
hidden: false
createdAt: "2023-05-23T16:48:07.206Z"
updatedAt: "2023-05-23T19:31:26.107Z"
---
Fiddler Kafka connector is a service that connects to a [Kafka topic](https://kafka.apache.org/documentation/#intro_concepts_and_terms) containing production events for a model, and publishes the events to Fiddler.

## Pre-requisites

We assume that the user has an account with Fiddler, has already created a project, uploaded a dataset and onboarded a model. We will need the [url_id, org_id,](doc:client-setup) project_id and model_id to configure the Kafka connector.

## Installation

The Kafka connector runs on Kubernetes within the customer’s environment. It is packaged as a Helm chart. To install:

```shell
helm repo add fiddler https://helm.fiddler.ai/stable/

helm repo update

kubectl -n kafka create secret generic fiddler-credentials --from-literal=auth=<API-KEY>

helm install fiddler-kafka fiddler/fiddler-kafka \
    --devel \
    --namespace kafka \
    --set fiddler.url=https://<FIDDLER-URL> \
    --set fiddler.org=<ORG> \
    --set fiddler.project_id=<PROJECT-ID> \
    --set fiddler.model_id=<MODEL-ID> \
    --set fiddler.ts_field=timestamp \
    --set fiddler.ts_format=INFER \
    --set kafka.host=kafka \
    --set kafka.port=9092 \
    --set kafka.topic=<KAFKA-TOPIC> \
    --set kafka.security_protocol=SSL \
    --set kafka.ssl_cafile=cafile \
    --set kafka.ssl_certfile=certfile \
    --set kafka.ssl_keyfile=keyfile \
    --set-string kafka.ssl_check_hostname=False

```

This creates a deployment that reads events from the Kafka topic and publishes it to the configured model. The deployment can be scaled as needed. However, if the Kafka topic is not partitioned, scaling will not result in any gains.

## Limitations

1. The connector assumes that there is a single dedicated topic containing production events for a given model. Multiple deployments can be created, one for each model, and scaled independently.
2. The connector assumes that events are published as JSON serialized dictionaries of key-value pairs. Support for other formats can be added on request. As an example, a Kafka message should look like the following:

```json
{
    “feature_1”: 20.7,
    “feature_2”: 45000,
    “feature_3”: true,
    “output_column”: 0.79,
    “target_column”: 1,
    “ts”: 1637344470000,
}

```