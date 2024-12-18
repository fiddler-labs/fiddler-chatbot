# Product Feature Maturity Definitions

## Overview

Fiddler ships new features rapidly.
To maintain a fast development pace and ensure a stable customer experience, we define clear stages for feature maturity.
Evolution from one stage to the other is quality-bound, not time-bound.
Features evolve through the following stages.

## Generally Available (GA)

The GA stage is when a feature is not only ready for production but the SLA is guaranteed.
GA features are fully supported by our team and are backed by our comprehensive support plans, providing customers with confidence in reliability, security, and performance.

## Public Preview

Public Preview features are reasonably mature and ready for broader testing, accessible to all customers.
This allows us to gather data about the feature in the wild, including important customer feedback.
While not formally bound by our SLA, our team responds promptly to issues.
APIs and functionality may—but are not likely to—change.

### Criteria

* Has a feature flag that is on by default for all customers.
* Available to all customers.
* Does not break or degrade existing functionality when enabled.  (Does not degrade existing SLOs.)
* Docs are published publicly but noted as “preview” or “public preview”.
* Breaking changes must be minimal and noted in the release notes.  Also, Field should message and support the change to heavy users directly.
* Expectation that it WILL land in the product after some unspecified amount of time.
* SLO, but no SLA.

## Private Preview

Private Preview features are early-stage and available to select design partners only.
During this stage, no Service Level Agreement (SLA) is provided. Instead, our engineering team collaborates directly with partners to iterate on the solution, making changes as needed based on feedback during business hours.
Features, including their APIs, will change rapidly; they might also be abandoned entirely.  

Why [design partners](https://a16z.com/a-framework-for-finding-a-design-partner/)?
Having a handful of transparent, engaged users or prospective customers can guide you through your first iteration of the product’s functionality, user experience, pricing and packaging, and more.
Their critiques should help you build something useful and usable for your broader customer base.
To inquire about private preview features, please reach out to [sales@fiddler.ai](mailto:sales@fiddler.ai).

### Criteria

* Has a feature flag that is **turned off by default**.
* Only available to select customers (as decided by Eng + PM).
  * Can do a POV with Private Preview with Eng+PM agreement (supporting team and leadership must approve).
  * Can market, if desired.
* Does not break or degrade existing functionality when disabled.
* May cause unexpected side-effects when enabled.
* Docs are not published, or are published in some not publicly-accessible place.
* Supported by the engineering team directly.
* Breaking changes can be communicated via Slack, not in release notes.
* No SLA or SLO.

## Solutions Engineering

Some solutions are custom-crafted by our Solutions Engineering Team.
These features, while useful and in production, are not officially supported by our overall product SLA.
Talk directly with your SE or CSM for clarification as to any custom-developed tools fall under.
