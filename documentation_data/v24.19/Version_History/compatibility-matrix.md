---
title: Compatibility Matrix
slug: compatibility-matrix
excerpt: ''
hidden: false
createdAt: Fri Apr 05 2024 19:54:39 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Oct 24 2024 20:18:26 GMT+0000 (Coordinated Universal Time)
---

# Compatibility Matrix

This table summarizes the compatibility between the Fiddler Python client and the Fiddler application. You can find:

* **Corresponding Fiddler Platform(s)**: Exactly the same features / API objects in both python client and the Fiddler Platform version
* **Lower Fiddler Platform**: Python client has features or API objects that may not be present in the Fiddler Platform, either due to that python client has additional new methods, or that the server has removed old APIs. However, everything they have in common (i.e., most APIs) will work.
* **Higher Fiddler Platform**: The Fiddler Platform has features the python client can't use, either due to the server has additional new APIs, or that python client has removed old API. However, everything they share in common (i.e., most APIs) will work.

| Client version   | Corresponding Fiddler Platform(s) ✅ | Lower Fiddler Platform | Higher Fiddler Platform |
|------------------|-------------------------------------|------------------------|--------------------------|
| 3.7              | 24.18                               | Between 24.17 and 24.4 |                           
| 3.6              | 24.17                               | Between 24.16 and 24.4 | 28.18 or above           |
| 3.5              | 24.16                               | Between 24.15 and 24.4 | 24.17 or above           |
| 3.4              | 24.13, 24.14, 24.15                 | Between 24.12 and 24.4 | 24.16 or above           |
| 3.3              | 24.10, 24.11, 24.12                 | Between 24.9 and 24.4  | 24.13 or above           |
| 3.2              | 24.8, 24.9                          | Between 24.7 and 24.4  | 24.10 or above           |
| 3.1              | 24.5, 24.6, 24.7                    | 24.4                   | 24.8 or above            |
| 3.0              | 24.4                                | Not compatible         | 24.5 or above            |
