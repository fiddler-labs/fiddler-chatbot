---
title: "fdl.FiddlerClient"
slug: "fdlfiddlerclient"
hidden: true
createdAt: "2023-08-01T11:16:37.768Z"
updatedAt: "2023-08-01T11:23:53.555Z"
---
The Client object is used to communicate with Fiddler.  In order to use the client, you'll need to provide authentication details as shown below.

For more information, see [Authorizing the Client](doc:authorizing-the-client).

[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "url",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The URL used to connect to Fiddler",
    "1-0": "organization_name",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The organization name for a Fiddler instance. Can be found on the General tab of the Settings page.",
    "2-0": "org_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The organization ID for a Fiddler instance. Can be found on the General tab of the Settings page.",
    "3-0": "auth_token",
    "3-1": "str",
    "3-2": "None",
    "3-3": "The authorization token used to authenticate with Fiddler. Can be found on the Credentials tab of the Settings page.",
    "4-0": "proxies",
    "4-1": "Optional [dict]",
    "4-2": "None",
    "4-3": "A dictionary containing proxy URLs.",
    "5-0": "verbose",
    "5-1": "Optional [bool]",
    "5-2": "False",
    "5-3": "If True, client calls will be logged verbosely.",
    "6-0": "timeout",
    "6-1": "Optional [int]",
    "6-2": "1200",
    "6-3": "The \"timeout\" parameter allows you to select the maximum time (in seconds) for the request to complete. By default, the value is 1200 sec.",
    "7-0": "verify",
    "7-1": "Optional  \n[bool]",
    "7-2": "True",
    "7-3": "If False, client will allow self-signed SSL certificates from the Fiddler server environment.  If True, the SSL certificates need to be signed by a certificate authority (CA)."
  },
  "cols": 4,
  "rows": 8,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

> 📘 Info
> 
> To maximize compatibility, **please ensure that your client version matches the server version for your Fiddler instance.**
> 
> When you connect to Fiddler using the code on the right, you'll receive a notification if there is a version mismatch between the client and server.
> 
> You can install a specific version of fiddler-client using pip:  
> `pip install fiddler-client==X.X.X`

```python Connect the Client
import fiddler as fdl

URL = 'https://app.fiddler.ai'
ORGANIZATION_NAME = 'my_org'
AUTH_TOKEN = 'p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58'

client = fdl.FiddlerClient(
    url=URL,
    organization_name=ORGANIZATION_NAME,
    auth_token=AUTH_TOKEN
)
```
```python Connect the Client with self-signed certs
import fiddler as fdl

URL = 'https://app.fiddler.ai'
ORG_ID = 'my_org'
AUTH_TOKEN = 'p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58'

client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN, 
		verify=False
)
```
```Text Connect the Client with Proxies
proxies = {
    'http' : 'http://proxy.example.com:1234',
    'https': 'https://proxy.example.com:5678'
}

client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN, 
		proxies=proxies
)
```

If you want to authenticate with Fiddler without passing this information directly into the function call, you can store it in a file named_ fiddler.ini_, which should be stored in the same directory as your notebook or script.

```python Writing fiddler.ini
%%writefile fiddler.ini

[FIDDLER]
url = https://app.fiddler.ai
organization_name = my_org
auth_token = p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58
```

```python Connecting the Client with a fiddler.ini file
fdl.FiddlerClient()
```