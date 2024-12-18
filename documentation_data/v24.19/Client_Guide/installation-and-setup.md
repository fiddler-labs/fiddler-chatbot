---
title: Installation and Setup
slug: installation-and-setup
excerpt: >-
  The document provides instructions on how to install, import, authorize, and
  connect the Fiddler Python SDK client to your Fiddler environment for use in
  Jupyter Notebooks or automated pipelines
metadata:
  description: >-
    The document provides instructions on how to install, import, authorize, and
    connect the Fiddler Python SDK client to your Fiddler environment for use in
    Jupyter Notebooks or automated pipelines.
  image: []
  robots: index
createdAt: Tue May 10 2022 17:14:02 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 21:03:35 GMT+0000 (Coordinated Universal Time)
---

# Installation and Setup

Fiddler offers a **Python SDK client** that lets you connect directly to your Fiddler environment from a Jupyter Notebook or automated pipeline.

***

### Install the Fiddler Client

The client is available for download from PyPI via pip:

```python
pip install -q fiddler-client
```

### Import the Fiddler Client

Once you've installed the client, you can import the `fiddler` package into any Python script:

```python
import fiddler as fdl
```

***

### Authorize the Client

To use the Fiddler client, you will need **authorization details** that contain

* The [URL](installation-and-setup.md#finding-your-url) you are connecting to
* An [authorization token](installation-and-setup.md#finding-your-authorization-token) for your user

#### Find your URL

The URL should point to **where Fiddler has been deployed** for your organization.

On-premise customers will use the URL specified by their IT operations team. If using Fiddler’s managed cloud service you will have been provided a unique URL is, and it will be in one of the forms shown below.

```html
# Managed SaaS
https://<YOUR UNIQUE APP NAME>.fiddler.ai

# Managed SaaS Peering
https://<YOUR UNIQUE APP NAME>.cloud.fiddler.ai
```

#### Find your Authorization Token

To find your authorization token, navigate to the **Settings** page, click the **Credentials** tab, and then use the **Create Key** button (if there is not already a authorization token for your user).

![](../.gitbook/assets/890613d-Screenshot\_2024-04-01\_at\_6.30.42\_AM.png)

### Connect the Client to Fiddler

Once you've located the URL of your Fiddler environment and your authorization token, you can connect the Fiddler client to your environment.

```python
URL = 'https://app.fiddler.ai'
AUTH_TOKEN = '' #Specify your authorization token available in the Fiddler Settings page - Credentials tab

# Connect to the Fiddler client
# This call will also validate the client vs server version compatibility.

fdl.init(url=URL, token=AUTH_TOKEN)

print(f'Client version: {fdl.__version__}')
print(f'Server version: {fdl.conn.server_version}')
print(f'Organization id: {fdl.conn.organization_id}')
print(f'Organization name: {fdl.conn.organization_name}')
```

### Set Log Level

Set the log level for the desired verbosity.

```
# Default log level is INFO
fdl.set_logging()

# Set DEBUG log level
fdl.set_logging(level=logging.DEBUG)
```

> 📘 Info
>
> For detailed documentation on the Fiddler Python client’s many features, check out the [API reference](../Python\_Client\_3-x/api-methods-30.md) section.

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}
