---
title: "REST API"
slug: "api"
excerpt: ""
hidden: false
createdAt: "Mon Aug 19 2024 09:46:33 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Aug 19 2024 09:46:33 GMT+0000 (Coordinated Universal Time)"
---

## API Reference
The Fiddler API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

## API Response types
Fiddler API returns three kinds of responses

### Normal Response
Normal response are the ones which doesn’t need to be paginated.
```
{
  api_version: <API version responding back with the response>,
  kind: "NORMAL",
  data: <Actual Response Object>
}
```

### Paginated Response
Paginated response contains the relevant items along with pagination data.
```
{
  api_version: <API version responding back with the response>,
  kind: "PAGINATED",
  data: {
    page_size: <integer>,
    item_count: <integer>,
    total: <integer>,
    page_count: <integer>,
    page_index: <integer>,
    offset: <integer>,
    items: [<Array of items>]
  }
}
```

### Error Response
In case something goes wrong, error response is returned.
```
{
  api_version: <API version responding back with the response>,
  kind: "ERROR",
  error: {
    code: <Error code>,
    message: <string>,
    errors: [
      {
        reason: <string>,
        message: <string>,
        help: <string>
      }
    ]
  }
}
```

Fiddler uses conventional HTTP response codes to indicate the success or failure of an API request.
In general: Codes in the **_2xx_** range indicate success.
Codes in the **_4xx_** range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a charge failed, etc.).
Codes in the **_5xx_** range indicate an error with Fiddler’s servers (these are rare).

## List of APIs
- [Projects](projects.md)
- [Model](model.md)
- [File Upload](file-upload.md)
- [Custom Metrics](custom-metrics.md)
- [Segments](segments.md)
- [Baseline](baseline.md)
- [Jobs](jobs.md)
- [Alert Rules](alert-rules.md)
- [Environment](environment.md)
- [Explainability](explainability.md)
- [Server Info](server-info.md)

<hr />

## Just getting started?
Check out our [Quickstart Notebooks](../QuickStart\_Notebooks/quick-start.md).
