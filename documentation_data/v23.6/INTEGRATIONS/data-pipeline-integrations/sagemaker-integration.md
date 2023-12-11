---
title: "SageMaker Integration"
slug: "sagemaker-integration"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Fri May 13 2022 14:21:38 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
The following Python script can be used to define a AWS Lambda function that can move your SageMaker inference logs from an S3 bucket to a Fiddler environment.

## Setup

In addition to pasting this code into your Lambda function, you will need to ensure the following steps are completed before the integration will work.

1. Make sure your model is actively being served by SageMaker and that you have  [enabled data capture](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-capture.html) for your SageMaker hosted models so that your model inferences are stored in a S3 bucket as JSONL files.
2. Make sure you have a Fiddler trial environment and your SageMaker model is onboarded with Fiddler.  Check out our Getting Started guide for guidance on how to onboard your models.
3. Make sure to specify the environment variables in the “Configuration” section of your Lambda function so that the Lambda knows how to connect with your Fiddler environment and so it knows what inputs and outputs to expect in the JSONL files captured by your SageMaker model.

![](https://files.readme.io/3b4cb21-lambda_setup.jpg "lambda_setup.jpg")

4. Make sure you have set up a trigger on your Lambda function so that the function is called upon “Object creation” events in your model’s S3 bucket.
5. Make sure you paste the following code into your new Lambda function.
6. Make sure that your Lambda function references the Fiddler ARN for the Layer that encapsulates the Fiddler Python client. (`arn:aws:lambda:us-west-2:079310353266:layer:fiddler-client-0814:1`)

## Script

```python
import fiddler as fdl
import json
import boto3
import os
import pandas as pd
import sys
import uuid
from urllib.parse import unquote_plus
import csv
import json
import base64
from io import StringIO
from botocore.vendored import requests

s3_client = boto3.client('s3')
url = os.getenv('FIDDLER_URL')
org = os.getenv('FIDDLER_ORG')
token = os.getenv('FIDDLER_TOKEN')
project = os.getenv('FIDDLER_PROJECT')
model = os.getenv('FIDDLER_MODEL')
timestamp_field = os.getenv('FIDDLER_TIMESTAMP_FIELD', None)  # optional arg
id_field = os.getenv('FIDDLER_ID_FIELD', None)  # optional arg
timestamp_format = os.getenv('FIDDLER_TIMESTAMP_FORMAT', None)  # optional arg
credentials = os.getenv('FIDDLER_AWS_CREDENTIALS', '{}')  # optional arg, json string
string_in_features = os.getenv('FEATURE_INPUTS')
out_feature = os.getenv('MODEL_OUTPUT')

def lambda_handler(event, context):
    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        s3_client.download_file(bucket, key, download_path)
        parse_sagemaker_log(download_path)

    
    return {
        'statusCode': 200,
        'body': json.dumps('Successful Lambda Publishing Run')
    }
                  

def parse_sagemaker_log(log_file):
    with open(log_file) as f:

        result = {}
        resultList = []
        in_features= string_in_features.replace("'", "").split(',')
        
        for line in f:
            pline = json.loads(line)
            input = pline['captureData']['endpointInput']['data']
            inputstr = StringIO(input)
            output = pline['captureData']['endpointOutput']['data']
            outputstr = StringIO(output)
            outarray = list(csv.reader(outputstr, delimiter=','))
            
            new_outarray = [float(x) for x in outarray[0]]
        
            csvReader = csv.reader(inputstr, delimiter=',')
            j = 0
            for row in csvReader:
                input_dict = {in_features[i]: row[i] for i in range(len(row))}
                
                pred_dict = {out_feature:new_outarray[j]}
                result.update(input_dict)
                result.update(pred_dict)
                result['__event_type'] = 'execution_event'
                resultList.append(result)
                j= j+1

        df = pd.DataFrame(resultList)
        print("Data frame : ", df)
        publish_event(df, log_file)

def assert_envs():
    """
    Asserting presence of required environmental variables:
        - FIDDLER_URL
        - FIDDLER_ORG
        - FIDDLER_TOKEN
        - FIDDLER_PROJECT
        - FIDDLER_MODEL
    """
    try:
        assert url is not None, '`FIDDLER_URL` env variable must be set.'
        assert org is not None, '`FIDDLER_ORG` env variable must be set.'
        assert token is not None, '`FIDDLER_TOKEN` env variable must be set.'
        assert project is not None, '`FIDDLER_PROJECT` env variable must be set.'
        assert model is not None, '`FIDDLER_MODEL` env variable must be set.'

        return None
    except Exception as e:
        log(f'ERROR: Env Variable assertion failed: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'ERROR: Env Variable assertion failed: {str(e)}'),
        }

def get_timestamp_format(env_timestamp_format):
    """
    Parses environment variable to convert `string` to `enum` value
    """
    if env_timestamp_format == 'EPOCH_MILLISECONDS':
        return fdl.FiddlerTimestamp.EPOCH_MILLISECONDS
    elif env_timestamp_format == 'EPOCH_SECONDS':
        return fdl.FiddlerTimestamp.EPOCH_SECONDS
    elif env_timestamp_format == 'ISO_8601':
        return fdl.FiddlerTimestamp.ISO_8601
    else:
        return fdl.FiddlerTimestamp.INFER

def log(out):
    print(out)

def publish_event(df, log_file):
    client = fdl.FiddlerApi(url=url, org_id=org, auth_token=token)

    log(f'Publishing events for file JSON for S3 file ' + str(log_file))
    res = client.publish_events_batch(
                    project_id=project,
                    model_id=model,
                    batch_source=df,
                    data_source=fdl.BatchPublishType.DATAFRAME,
                    timestamp_field=timestamp_field,
                    timestamp_format=get_timestamp_format(timestamp_format)
                    )
    
    log(res)
```