---
title: Single Sign On with Okta
slug: okta-integration
excerpt: ''
createdAt: Mon Aug 01 2022 15:14:37 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)
---

# Okta Integration

### Overview

These instructions will help administrators configure Fiddler to be used with an existing Okta single sign on application.

### Okta Setup:

First, you must create an OIDC based application within Okta. Your application will require a callback URL during setup time. This URL will be provided to you by a Fiddler administrator. Your application should grant "Authorization Code" permissions to a client acting on behalf of a user. See the image below for how your setup might look like:

![](../.gitbook/assets/b7b67fe-Screen\_Shot\_2022-08-07\_at\_10.22.36\_PM.png)

This is the stage where you can allow certain users of your organization access to Fiddler through Okta. You can use the "Group Assignments" field to choose unique sets of organization members to grant access to. This setup stage will also allow for Role Based Access Control (i.e. RBAC) based on specific groups using your application.

Once your application has been set up, a Fiddler administrator will need to receive the following information and credentials:

* Okta domain
* Client ID
* Client Secret
* Okta Account Type (default or custom)

All of the above can be obtained from your Okta application dashboard, as shown in the pictures below:

![](../.gitbook/assets/6442827-Screen\_Shot\_2022-08-07\_at\_10.30.03\_PM.png)

![](../.gitbook/assets/f1dbcf6-Screen\_Shot\_2022-08-07\_at\_10.30.15\_PM.png)

You can also pass the above information to your Fiddler administrator via your okta.yml file.

### Deployment instructions

**Step 1** Create a `<secret-filename>.yaml` file with the following template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: fiddler-sso-okta-credentials
  namespace: <NAMESPACE_NAME>
data:
  sso-okta-issuer: <OKTA_ISSUER> # https://<okta_domain>/oauth2/default
  sso-okta-authorize-url: <AUTHORIZE_URL> # https://<okta_domain>/oauth2/default/v1/authorize
  sso-okta-token-url: <TOKEN_URL> # https://<okta_domain>/oauth2/default/v1/token
  sso-okta-user-info-url: <USER_INFO_URL> # https://<okta_domain>/oauth2/default/v1/userinfo
  sso-okta-client-id: <CLIENT_ID>
  sso-okta-client-secret: <CLIENT_SECRET>
  sso-okta-domain: <DOMAIN> # your okta domain
  authorization-type: <AUTHORIZATION_TYPE> # default
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
      provider: okta  
      azuread:  
        secretName: fiddler-sso-okta-credentials
```

> 📘 Once the deployments are updated, the new SSO settings will be applied.

### Logging into Fiddler:

Once a Fiddler administrator has successfully set up a deployment for your organization using your given Okta credentials, you should see the “Sign in with SSO” button enabled. When this button is clicked, you should be navigated to an Okta login screen. Once successfully authenticated, and assuming you have been granted access to Fiddler through Okta, you should be able to login to Fiddler.

![](../.gitbook/assets/c96a709-Screen\_Shot\_2022-08-07\_at\_10.36.40\_PM.png)

NOTES:

1. To be able to login with SSO, it is initially required for the user to register with Fiddler Application. Upon successful registration, the users will be able to login using SSO.
2. The only information Fiddler stores from Okta based logins is a user’s first name, last name, email address, and OIDC token.
3. Fiddler does not currently support using Okta based login through its API (see fiddler-client). In order to use an Okta based account through Fiddler's API, use a valid access token which can be created and copied on the “Credentials” tab on Fiddler’s “Settings” page.

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

