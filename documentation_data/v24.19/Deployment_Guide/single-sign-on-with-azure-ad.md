---
title: Single Sign on with Azure AD
slug: single-sign-on-with-azure-ad
excerpt: Configure Azure SSO with Fiddler
createdAt: Tue Jan 23 2024 06:02:09 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 16:51:51 GMT+0000 (Coordinated Universal Time)
---

# SSO with Azure AD

### Prerequisite

Set up [OIDC](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/walkthrough-register-app-azure-active-directory) configuration within Azure by selecting the type as Web and with the redirect URI pointing to your deployment, as seen in the image below.

**Redirect URL** - `{base_url}/api/sso/azuread/callback`

![](../.gitbook/assets/ce5d081-Azure\_SSO\_registration.png)

Once the registration is successful, create a new client secret and copy the secret value immediately after it is created without refreshing the page.

![](../.gitbook/assets/96042ac-Azure\_add\_new\_client\_secret.png)

> 🚧 Be careful
>
> You will not be able to access the `client secret` later because it is shown ONCE and not repeated

### Creating a new client secret

![Masked client secret value](../.gitbook/assets/1f8d791-Azure\_Client\_Secret.png)

Masked client secret value

### Setting up token permissions to the application

![Token Permissions](../.gitbook/assets/e40da63-Screenshot\_2024-04-15\_at\_12.21.03\_PM.png)

Token Permissions

### Setting up API permissions to the application

![Application Permissions](../.gitbook/assets/5e2f00e-Screenshot\_2024-04-15\_at\_12.22.12\_PM.png)

Application Permissions

In `Authentication`, fill the details as shown below

![Application Page Updates](../.gitbook/assets/00e5989-Screenshot\_2024-04-15\_at\_12.24.07\_PM.png)

Application Page Updates

Up until this point, our application configuration is complete. The following section now deals with Fiddler side of changes.

### Configure Azure SSO with Fiddler

The following details are required to configure Azure SSO with Fiddler:

* OpenID Connect metadata document `sso-azuread-identity-metadata`
* Application (client) ID `sso-azuread-client-id`
* Newly created client secret `sso-azuread-client-secret`

![OpenID Connect metadata Document can be found under Endpoints under the overview section.](../.gitbook/assets/1d18e08-Azure\_SSO\_config\_details.png)

OpenID Connect metadata Document can be found under Endpoints under the overview section.

The following details can be obtained from the `OpenID Connect metadata document` URI.

* Response Types Supported `sso-azuread-response-type`
* Response Modes Supported `sso-azuread-response-mode`
* Issuer `sso-azuread-issuer`
* Scopes Supported `sso-azuread-scope`

### Deployment instructions

**Step 1** Create a `<secret-filename>.yaml` file with the following template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: fiddler-sso-azuread-credentials
  namespace: <NAMESPACE_NAME>
data:
  sso-azuread-identity-metadata: <IDENTITY_METADATA_URL>
  sso-azuread-client-id: <CLIENT_ID>
  sso-azuread-response-type: <RESPONSE_TYPE> # set to "code id_token"
  sso-azuread-response-mode: <RESPONSE MODE> # set to "form_post"
  sso-azuread-client-secret: <CLIENT_SECRET>
  sso-azuread-validate-issuer: <VALIDATE_ISSUER> # set to "true"
  sso-azuread-issuer: <ISSUER_URL>
  sso-azuread-scope: <SCOPES> # set to "openid,offline_access,profile,email"
type: Opaque
```

> 📘 All the values must be base64 encoded
>
> In mac you can run `echo -n "string to be encoded" | base64` to get the encoded value

> 📘 Do not use doubles quotes
>
> Don’t use doubles quotes anywhere in values in above yaml. In above example, it is written set to “true” - the value is true and not “true”.

**Step 2** Update the k8s secret in the namespace of that cluster using the above file.

```shell
kubectl apply -f <secret-filename>.yaml -n fiddler
```

**Step 3** Update the Helm variable `fiddler.auth.sso.provider` and `fiddler.auth.sso.azuread.secretName` with `azuread` and `fiddler-sso-azuread-credentials` value. If you are using the helm values file, use the following settings.

```yaml
fiddler:  
  auth:  
    sso:  
      provider: azuread  
      azuread:  
        secretName: fiddler-sso-azuread-credentials
```

> 📘 Once the deployments are updated, the new SSO settings will be applied.

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

