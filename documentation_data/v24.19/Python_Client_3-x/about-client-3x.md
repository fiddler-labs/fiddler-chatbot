---
title: About Client 3.x
slug: about-client-3x
excerpt: ''
createdAt: Mon Mar 18 2024 14:18:09 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Oct 24 2024 20:29:08 GMT+0000 (Coordinated Universal Time)
---

# About Client 3.x

The Fiddler Client contains many useful methods for sending and receiving data to and from the Fiddler platform.

Fiddler provides a Python Client that allows you to connect to Fiddler directly from a Python notebook or automated pipeline.

Each client function is documented with a description, usage information, and code examples.

### Initialization

The Client object is used to communicate with Fiddler.

#### Import Fiddler

To import fiddler client, we can use the below method:

```python
import fiddler as fdl
from fiddler import Model, Project
```

#### Authenticate and Connect

In order to use the client, you'll need to provide authentication details as shown below.

**Usage params**

| Parameter | Type            | Default | Description                                                                                                             |
| --------- | --------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| url       | str             | -       | The URL of Fiddler Platform to make a connection to.                                                                    |
| token     | str             | -       | The authorization token used to authenticate with Fiddler. Can be found on the Credentials tab of the Settings page.    |
| proxies   | Optional\[dict] | -       | Dictionary mapping protocol to the URL of the proxy                                                                     |
| timeout   | Optional\[int]  | 60      | Seconds to wait for the server to send data before giving up.                                                           |
| verify    | Optional\[bool] | True    | Controls whether we verify the server’s TLS certificate.                                                                |
| validate  | Optional\[bool] | True    | Whether to validate the server/Client Version compatibility. Some functionalities might not work if this is turned off. |

**Return params**

None

**Usage**

```python
fdl.init(
  url: str,
  token: str,
  proxies: dict[str, Any],
  timeout: int,
  verify: bool,
  validate: bool
)
```

```python
fdl.init(
  url="https://xyz.fiddler.ai",
  token="abc"
)
```

**Raises**

| Error code         | Issue                                                           |
| ------------------ | --------------------------------------------------------------- |
| ValueError         | URL or token missing while initializing the client.             |
| IncompatibleClient | Fiddler Platform version is not compatible with Client version. |

> 📘 Info
>
> To maximize compatibility, **please ensure that your Client Version matches the server version for your Fiddler instance.**
>
> When you connect to Fiddler using the code on the right, you'll receive a notification if there is a version mismatch between the client and server.
>
> You can install a specific version of fiddler-client using pip:\
> `pip install fiddler-client==X.X.X`



{% include "../.gitbook/includes/main-doc-dev-footer.md" %}
