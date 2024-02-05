---
title: "Single Sign on with Azure AD"
slug: "single-sign-on-with-azure-ad"
excerpt: "Configure Azure SSO with Fiddler"
hidden: false
createdAt: "Tue Jan 23 2024 06:02:09 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 24 2024 05:07:46 GMT+0000 (Coordinated Universal Time)"
---
## Prerequisite

Set up [OIDC](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/walkthrough-register-app-azure-active-directory) configuration within Azure by selecting the type as Web and with the redirect URI pointing to your deployment, as seen in the image below.

**Redirect URL** - `{base_url}/api/sso/azuread/callback`

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ce5d081-Azure_SSO_registration.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Once the registration is successful, create a new client secret and copy the secret value immediately after it is created without refreshing the page. 

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/96042ac-Azure_add_new_client_secret.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


> 🚧 Be careful
> 
> You will not be able to access the `client secret` later because it is shown ONCE and not repeated

## Creating a new client secret

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1f8d791-Azure_Client_Secret.png",
        "",
        "Masked client secret value"
      ],
      "align": "center",
      "border": true,
      "caption": "Masked client secret value"
    }
  ]
}
[/block]


## Configure Azure SSO with Fiddler

The following details are required

- OpenID Connect metadata document `sso-azuread-identity-metadata`
- Application (client) ID `sso-azuread-client-id`
- Newly created client secret `sso-azuread-client-secret`

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1d18e08-Azure_SSO_config_details.png",
        "",
        "OpenID Connect metadata Document can be found under Endpoints under the overview section."
      ],
      "align": "center",
      "caption": "OpenID Connect metadata Document can be found under Endpoints under the overview section."
    }
  ]
}
[/block]


The following details can be obtained from the `OpenID Connect metadata document` URI.

- Response Types Supported `sso-azuread-response-type`
- Response Modes Supported `sso-azuread-response-mode`
- Issuer `sso-azuread-issuer`
- Scopes Supported `sso-azuread-scope`

## Deployment instructions

**Step 1** Create a `<secret-filename>.yaml` file with the following template.

[block:html]
{
  "html": "apiVersion: v1\nkind: Secret\nmetadata:\n  name: fiddler-sso-azuread-credentials\n  namespace: <NAMESPACE_NAME>\ndata:\n  sso-azuread-identity-metadata: <IDENTITY_METADATA_URL>\n  sso-azuread-client-id: <CLIENT_ID>\n  sso-azuread-response-type: <RESPONSE_TYPE> # \"code id_token\" is recommended\n  sso-azuread-response-mode: <RESPONSE MODE> # \"form_post\" is recommended\n  sso-azuread-client-secret: <CLIENT_SECRET>\n  sso-azuread-validate-issuer: <VALIDATE_ISSUER> # recommended to be set to true for all customer deployments\n  sso-azuread-issuer: <ISSUER_URL>\n  sso-azuread-scope: <SCOPES> # mulitple scopes can be passed as comma separated values. Ex: openid,offline_access\ntype: Opaque"
}
[/block]


> 📘 All the values must be base64 encoded
> 
> In mac you can run `echo -n "string to be encoded" | base64` to get the encoded value

**Step 2** Update the k8s secret in the namespace of that cluster using the above file.  

[block:html]
{
  "html": "kubectl apply -f <secret-filename>.yaml -n fiddler"
}
[/block]


**Step 3** Update the Helm variable `fiddler.auth.sso.provider` and `fiddler.auth.sso.azuread.secretName` with `azuread` and `fiddler-sso-azuread-credentials` value. If you are using the helm values file, use the following settings.

[block:html]
{
  "html": "fiddler:  \n  auth:  \n    sso:  \n      provider: azuread  \n      azuread:  \n        secretName: fiddler-sso-azuread-credentials"
}
[/block]


> 📘 Once the deployments are updated, the new SSO settings will be applied.

:clipboard: Related articles  
Detailed instructions for deploying an SSO-enabled cluster - [Creating Multi-org w/ SSO enabled cluster in Dev | SSO enabled cluster](https://fiddlerlabs.atlassian.net/wiki/spaces/FL/pages/2061140270/Creating+Multi-org+w+SSO+enabled+cluster+in+Dev#SSO-enabled-cluster)
