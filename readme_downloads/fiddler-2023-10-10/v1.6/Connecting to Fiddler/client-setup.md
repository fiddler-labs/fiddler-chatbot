---
title: "fdl.FiddlerApi"
slug: "client-setup"
hidden: false
createdAt: "2022-05-13T14:41:57.721Z"
updatedAt: "2023-01-24T14:53:30.636Z"
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
    "1-0": "org_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The organization ID for a Fiddler instance. Can be found on the General tab of the Settings page.",
    "2-0": "auth_token",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The authorization token used to authenticate with Fiddler. Can be found on the Credentials tab of the Settings page.",
    "3-0": "proxies",
    "3-1": "Optional [dict]",
    "3-2": "None",
    "3-3": "A dictionary containing proxy URLs.",
    "4-0": "verbose",
    "4-1": "Optional [bool]",
    "4-2": "False",
    "4-3": "If True, client calls will be logged verbosely.",
    "5-0": "verify",
    "5-1": "Optional  \n[bool]",
    "5-2": "True",
    "5-3": "If False, client will allow self-signed SSL certificates from the Fiddler server environment.  If True, the SSL certificates need to be signed by a certificate authority (CA)."
  },
  "cols": 4,
  "rows": 6,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

> 🚧 Warning
> 
> If verbose is set to **True**, all information required for debugging will be logged, including the authorization token.

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
ORG_ID = 'my_org'
AUTH_TOKEN = 'p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58'

client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
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



```python Defining Proxy URLs
proxies = {
    'http' : 'http://proxy.example.com:1234',
    'https': 'https://proxy.example.com:5678'
}
```



If you want to authenticate with Fiddler without passing this information directly into the function call, you can store it in a file named_ fiddler.ini_, which should be stored in the same directory as your notebook or script.

```python Writing fiddler.ini
%%writefile fiddler.ini

[FIDDLER]
url = https://app.fiddler.ai
org_id = my_org
auth_token = p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58
```



```python Connecting the Client with a fiddler.ini file
client = fdl.FiddlerApi()
```