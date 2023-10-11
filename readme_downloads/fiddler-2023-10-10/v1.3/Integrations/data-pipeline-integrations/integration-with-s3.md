---
title: "S3 Integration"
slug: "integration-with-s3"
hidden: false
createdAt: "2022-04-19T17:40:36.681Z"
updatedAt: "2022-06-08T15:46:46.046Z"
---
[block:api-header]
{
  "title": "Pulling a dataset from S3"
}
[/block]
You may want to **pull a dataset directly from S3**. This may be used either to upload a baseline dataset, or to publish production traffic to Fiddler.

You can use the following code snippet to do so. Just fill out each of the string variables (`S3_BUCKET`, `S3_FILENAME`, etc.) with the correct information.
[block:code]
{
  "codes": [
    {
      "code": "import boto3\nimport pandas as pd\n\nS3_BUCKET = 'my_bucket'\nS3_FILENAME = 'my_baseline.csv'\n\nAWS_ACCESS_KEY_ID = 'my_access_key'\nAWS_SECRET_ACCESS_KEY = 'my_secret_access_key'\nAWS_SESSION_TOKEN = 'my_session_token'\nAWS_REGION = 'my_region'\n\nsession = boto3.session.Session(\n    aws_access_key_id=AWS_ACCESS_KEY_ID,\n    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,\n    aws_session_token=AWS_SESSION_TOKEN,\n    region_name=AWS_REGION\n)\n\ns3 = session.client('s3')\n\ns3_data = s3.get_object(\n    Bucket=S3_BUCKET,\n    Key=S3_FILENAME\n)['Body']\n\ndf = pd.read_csv(s3_data)",
      "language": "python"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Uploading the data to Fiddler"
}
[/block]
If your goal is to **use this data as a baseline dataset** within Fiddler, you can then proceed to upload your dataset (see [Uploading a Baseline Dataset](doc:uploading-a-baseline-dataset)).

If your goal is to **use this data as a batch of production traffic**, you can then proceed to publish the batch to Fiddler (see [Publishing Batches of Events](doc:publishing-batches-of-events) ). 

[block:api-header]
{
  "title": "What if I don’t want to hardcode my AWS credentials?"
}
[/block]
If you don’t want to hardcode your credentials, you can **use an AWS profile** instead. For more information on how to create an AWS profile, click [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).

You can use the following code snippet to point your `boto3` session to the profile of your choosing.
[block:code]
{
  "codes": [
    {
      "code": "import boto3\nimport pandas as pd\n\nS3_BUCKET = 'my_bucket'\nS3_FILENAME = 'my_baseline.csv'\n\nAWS_PROFILE = 'my_profile'\n\nsession = boto3.session.Session(\n    profile_name=AWS_PROFILE\n)\n\ns3 = session.client('s3')\n\ns3_data = s3.get_object(\n    Bucket=S3_BUCKET,\n    Key=S3_FILENAME\n)['Body']\n\ndf = pd.read_csv(s3_data)",
      "language": "python"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "What if I don't want to load the data into memory?"
}
[/block]
If you would rather **save the data to a disk** instead of loading it in as a pandas DataFrame, you can use the following code snippet instead.
[block:code]
{
  "codes": [
    {
      "code": "import boto3\nimport pandas as pd\nimport fiddler as fdl\n\nS3_BUCKET = 'my_bucket'\nS3_FILENAME = 'my_baseline.csv'\n\nAWS_ACCESS_KEY_ID = 'my_access_key'\nAWS_SECRET_ACCESS_KEY = 'my_secret_access_key'\nAWS_SESSION_TOKEN = 'my_session_token'\nAWS_REGION = 'my_region'\n\nOUTPUT_FILENAME = 's3_data.csv'\n\nsession = boto3.session.Session(\n    aws_access_key_id=AWS_ACCESS_KEY_ID,\n    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,\n    aws_session_token=AWS_SESSION_TOKEN,\n    region_name=AWS_REGION\n)\n\ns3 = session.client('s3')\n\ns3.download_file(\n    Bucket=S3_BUCKET,\n    Key=S3_FILENAME,\n    Filename=OUTPUT_FILENAME\n)",
      "language": "python"
    }
  ]
}
[/block]