---
title: "fdl.FiddlerApi"
slug: "client-setup"
hidden: false
createdAt: "2022-05-13T14:41:57.721Z"
updatedAt: "2022-05-23T16:07:05.753Z"
---
The Client object used to communicate with Fiddler.  In order to use the client, you'll need to provide authentication details as shown below.

For more information, see Authorizing the Client.
[block:parameters]
{
  "data": {
    "h-0": "Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "0-0": "url",
    "0-1": "str",
    "0-2": "None",
    "h-3": "Description",
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
    "4-3": "If True, client calls will be logged verbosely."
  },
  "cols": 4,
  "rows": 5
}
[/block]

[block:callout]
{
  "type": "warning",
  "title": "Warning",
  "body": "If verbose is set to **True**, all information required for debugging will be logged, including the authorization token."
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "To maximize compatibility, **please ensure that your client version matches the server version for your Fiddler instance.**\n\nWhen you connect to Fiddler using the code on the right, you'll receive a notification if there is a version mismatch between the client and server.\n\nYou can install a specific version of fiddler-client using pip:\npip3 install fiddler-client==X.X.X"
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import fiddler as fdl\n\nURL = 'https://app.fiddler.ai'\nORG_ID = 'my_org'\nAUTH_TOKEN = 'p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58'\n\nclient = fdl.FiddlerApi(\n    url=URL,\n    org_id=ORG_ID,\n    auth_token=AUTH_TOKEN\n)",
      "language": "python",
      "name": "Connect the Client"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "proxies = {\n    'http' : 'http://proxy.example.com:1234',\n    'https': 'https://proxy.example.com:5678'\n}",
      "language": "python",
      "name": "Defining Proxy URLs"
    }
  ]
}
[/block]
If you want to authenticate with Fiddler without passing this information directly into the function call, you can store it in a file named* fiddler.ini*, which should be stored in the same directory as your notebook or script.
[block:code]
{
  "codes": [
    {
      "code": "%%writefile fiddler.ini\n\n[FIDDLER]\nurl = https://app.fiddler.ai\norg_id = my_org\nauth_token = p9uqlkKz1zAA3KAU8kiB6zJkXiQoqFgkUgEa1sv4u58",
      "language": "python",
      "name": "Writing fiddler.ini"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "client = fdl.FiddlerApi()",
      "language": "python",
      "name": "Connecting the Client with a fiddler.ini file"
    }
  ]
}
[/block]