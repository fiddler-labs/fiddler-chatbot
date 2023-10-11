---
title: "System Architecture"
slug: "system-architecture"
hidden: false
createdAt: "2022-04-19T20:19:53.311Z"
updatedAt: "2022-06-01T17:51:54.469Z"
---
[block:api-header]
{
  "title": "System Architecture"
}
[/block]
Fiddler conceptual diagram depicts the various Fiddler services and shows how the traffic gets routed in and out of the application. All access to the Fiddler application and its services are through Load Balancer. The application consists of three layers
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a914f86-Architecture.png",
        "Architecture.png",
        847,
        573,
        "#f3f3f4"
      ]
    }
  ]
}
[/block]
* __Layer 1__: comprises an external facing load balancer and internal facing Envoy proxy or Ingress-nginx controller, a Kubernetes built-in configuration for HTTP load balancing that defines rules for external connectivity to Kubernetes services
* __Layer 2__: comprises Fiddler services; Admin, Authz, Compacter, Data, Executor, Event, and Monitoring services. These services are scalable to match the customer needs. 
* __Layer 3__: comprises Queue, Storage and Databases.

* __Logging & Monitoring__: have a log collector and aggregation service using FluentD and Loki and use Prometheus-Grafana for visualization and alerting.


[^1]: _Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions_