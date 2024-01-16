---
title: "S3 Integration"
slug: "integration-with-s3"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 17:40:36 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Pulling a dataset from S3

You may want to **pull a dataset directly from S3**. This may be used either to upload a baseline dataset, or to publish production traffic to Fiddler.

You can use the following code snippet to do so. Just fill out each of the string variables (`S3_BUCKET`, `S3_FILENAME`, etc.) with the correct information.

```python
import boto3
import pandas as pd

S3_BUCKET = 'my_bucket'
S3_FILENAME = 'my_baseline.csv'

AWS_ACCESS_KEY_ID = 'my_access_key'
AWS_SECRET_ACCESS_KEY = 'my_secret_access_key'
AWS_REGION = 'my_region'

session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

s3 = session.client('s3')

s3_data = s3.get_object(
    Bucket=S3_BUCKET,
    Key=S3_FILENAME
)['Body']

df = pd.read_csv(s3_data)
```

## Uploading the data to Fiddler

If your goal is to **use this data as a baseline dataset** within Fiddler, you can then proceed to upload your dataset (see [Uploading a Baseline Dataset](doc:uploading-a-baseline-dataset)).

If your goal is to **use this data as a batch of production traffic**, you can then proceed to publish the batch to Fiddler (see [Publishing Batches of Events](doc:publishing-batches-of-events) ). 

## What if I don’t want to hardcode my AWS credentials?

If you don’t want to hardcode your credentials, you can **use an AWS profile** instead. For more information on how to create an AWS profile, click [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).

You can use the following code snippet to point your `boto3` session to the profile of your choosing.

```python
import boto3
import pandas as pd

S3_BUCKET = 'my_bucket'
S3_FILENAME = 'my_baseline.csv'

AWS_PROFILE = 'my_profile'

session = boto3.session.Session(
    profile_name=AWS_PROFILE
)

s3 = session.client('s3')

s3_data = s3.get_object(
    Bucket=S3_BUCKET,
    Key=S3_FILENAME
)['Body']

df = pd.read_csv(s3_data)
```

## What if I don't want to load the data into memory?

If you would rather **save the data to a disk** instead of loading it in as a pandas DataFrame, you can use the following code snippet instead.

```python
import boto3
import pandas as pd
import fiddler as fdl

S3_BUCKET = 'my_bucket'
S3_FILENAME = 'my_baseline.csv'

AWS_ACCESS_KEY_ID = 'my_access_key'
AWS_SECRET_ACCESS_KEY = 'my_secret_access_key'
AWS_REGION = 'my_region'

OUTPUT_FILENAME = 's3_data.csv'

session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

s3 = session.client('s3')

s3.download_file(
    Bucket=S3_BUCKET,
    Key=S3_FILENAME,
    Filename=OUTPUT_FILENAME
)
```
