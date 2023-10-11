---
title: "On-prem Installation Guide"
slug: "installation-guide"
hidden: false
createdAt: "2022-04-19T20:20:10.097Z"
updatedAt: "2022-06-01T17:54:15.752Z"
---
[block:api-header]
{
  "title": "Installation Guide"
}
[/block]
When installing Fiddler on your cloud, Fiddler will send you a zipped directory containing a `readme` and the `configuration files` to set up the various Fiddler services. The readme contains a detailed step-by-step installation guide. The steps comprise (at a high level):

1. Either identify an existing `K8s` cluster on which to install Fiddler or provision a new one within your environment of choice (_Vanilla v1.14-1.16, Azure AKS, GCP GKE, AWS EKS_)
2. Provision a `postgres SQL db` (or _Azure Postgresql, GCP Cloudsql, or AWS RDS Postgresql_)
3. Download the Fiddler deployment images from our container repo (typically `quay.io`) using the URL + credentials contained in the readme
4. Follow the steps in the readme to update the config files to point to the right db instance
5. Run the installation scripts provided in the readme