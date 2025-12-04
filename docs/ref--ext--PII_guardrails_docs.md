# Guardrails Quick Start

Fiddler Guardrails provide real-time protection for your LLM applications by detecting and preventing harmful content, PII leaks, and hallucinations before they reach your users.

**Time to complete**: \~15 minutes

## What You'll Learn

* How to set up Fiddler Guardrails
* The common execution pattern for all guardrail types
* How to interpret risk scores
* How to integrate guardrails into your LLM application

## Prerequisites

* **Fiddler Guardrails Account**: Sign up for [Free Guardrails](https://fiddler.ai/free-guardrails)
* **API Key**: Generated from your Fiddler Guardrails dashboard
* **Python 3.8+** (or any HTTP client)

***

## Quick Start: Common Execution Pattern

All Fiddler Guardrails follow the same execution pattern, making it easy to protect your application with multiple guardrail types.

### Step 1: Get Your API Key

1. Sign up at [fiddler.ai/free-guardrails](https://fiddler.ai/free-guardrails)
2. Activate your account via email
3. Generate your API key from the dashboard

For detailed setup instructions, see the [Guardrails Getting Started Guide](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/getting-started/guardrails).

### Step 2: Install Required Libraries (Optional)

```bash
# For Python
pip install requests

# Or use any HTTP client in your preferred language
```

### Step 3: Make a Guardrail Request

The execution pattern is the same for all guardrail types:

```python
import requests
import json

# Your API credentials
API_KEY = "your-api-key-here"
API_URL = "https://api.fiddler.ai/guardrails/v1"

# Content to check
content_to_check = {
    "inputs": ["What is the capital of France?"],
    # For faithfulness, include context:
    # "context": ["Paris is the capital of France..."]
}

# Choose your guardrail type:
# - "safety" - Detect harmful, toxic, or jailbreaking content
# - "pii" - Detect personally identifiable information
# - "faithfulness" - Detect hallucinations and unsupported claims

guardrail_type = "safety"  # Change this to test different guardrails

# Make API request
response = requests.post(
    f"{API_URL}/{guardrail_type}",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json=content_to_check
)

# Parse results
results = response.json()
print(json.dumps(results, indent=2))
```

### Step 4: Interpret Risk Scores

All guardrails return risk scores between 0 and 1:

* **0.0 - 0.3**: Low risk (safe to proceed)
* **0.3 - 0.7**: Medium risk (review recommended)
* **0.7 - 1.0**: High risk (block or flag for review)

```python
# Example response
{
  "scores": [0.15],  # Low risk - content is safe
  "threshold": 0.5,
  "passed": [True]   # Content passed the guardrail check
}
```

### Step 5: Integrate into Your Application

Add guardrails as a protective layer before LLM inference:

```python
def check_guardrail(content, guardrail_type="safety"):
    """Check content against Fiddler Guardrails"""
    response = requests.post(
        f"{API_URL}/{guardrail_type}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"inputs": [content]}
    )
    result = response.json()
    return result["passed"][0], result["scores"][0]

# In your LLM application
user_input = "User's message here..."

# Check input safety
is_safe, risk_score = check_guardrail(user_input, "safety")

if not is_safe:
    return "I'm sorry, I can't process that request."

# Proceed with LLM inference only if content is safe
llm_response = call_your_llm(user_input)

# Optionally, check output for PII or hallucinations
has_pii, pii_score = check_guardrail(llm_response, "pii")
if has_pii:
    llm_response = redact_pii(llm_response)

return llm_response
```

***

## Available Guardrail Types

### 🛡️ Safety Guardrails

Detect harmful, toxic, or jailbreaking content in user inputs and LLM outputs.

**Use cases:**

* Content moderation
* Jailbreak prevention
* Toxic content detection

**→** [**Safety Guardrails Tutorial**](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-safety)

### 🔒 PII Detection

Identify and prevent personally identifiable information (PII) leaks.

**Use cases:**

* Data privacy compliance
* GDPR/CCPA protection
* Sensitive data redaction

**→** [**PII Detection Tutorial**](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-pii)

### ✅ Faithfulness Detection

Detect hallucinations and unsupported claims by comparing outputs to source context.

**Use cases:**

* RAG application accuracy
* Fact-checking
* Hallucination prevention

**→** [**Faithfulness Tutorial**](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-faithfulness)

***

## Common Use Cases

### Pre-Processing (Input Guardrails)

```python
# Check user input before sending to LLM
user_input = request.get("user_message")

# Safety check
is_safe, _ = check_guardrail(user_input, "safety")
if not is_safe:
    return {"error": "Inappropriate content detected"}

# PII check
has_pii, _ = check_guardrail(user_input, "pii")
if has_pii:
    user_input = redact_pii(user_input)

# Now safe to process with LLM
response = llm.generate(user_input)
```

### Post-Processing (Output Guardrails)

```python
# Check LLM output before returning to user
llm_output = llm.generate(user_input)

# Check for hallucinations
is_faithful, _ = check_guardrail(
    llm_output,
    "faithfulness",
    context=retrieval_context
)

if not is_faithful:
    return {"warning": "Response may contain unsupported claims"}

# Check for PII in output
has_pii, _ = check_guardrail(llm_output, "pii")
if has_pii:
    llm_output = redact_pii(llm_output)

return {"response": llm_output}
```

***

## Best Practices

1. **Layer Multiple Guardrails**: Use safety + PII for inputs, faithfulness for outputs
2. **Set Appropriate Thresholds**: Adjust risk score thresholds based on your use case
3. **Log All Checks**: Track guardrail results for monitoring and improvement
4. **Handle Gracefully**: Provide helpful error messages when content is blocked
5. **Monitor Performance**: Track false positives/negatives and adjust as needed

***

## Next Steps

* **Setup**: [Complete Guardrails Setup Guide](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/protect-and-guardrails/guardrails-quick-start)
* **Concepts**: [Guardrails Overview](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/getting-started/guardrails)
* **Tutorials**:
  * [Safety Guardrails](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-safety)
  * [PII Detection](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-pii)
  * [Faithfulness](https://docs.fiddler.ai/developers/tutorials/guardrails/guardrails-faithfulness)
* **FAQ**: [Guardrails Frequently Asked Questions](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/protect-and-guardrails/guardrails-faq)
* **API Reference**: [Guardrails API Documentation](https://app.gitbook.com/s/rsvU8AIQ2ZL9arerribd/rest-api/guardrails-api-reference)


# PII

Get your sensitive information detection running in **minutes** with Fiddler's Fast PII Guardrails. This guide walks you through detecting PII, PHI, and custom entities to protect sensitive data across your applications.

## What You'll Build

In this quick start, you'll implement a sensitive information detection system that:

* Detects 35+ types of personally identifiable information (PII)
* Identifies 7 types of protected health information (PHI)
* Configures custom entity detection for organization-specific data
* Provides real-time detection with sub-second latency

{% hint style="info" %}
**Interactive Tutorial**

For more advanced examples, including batch processing, performance optimization, and production deployment patterns:

[**Open the Complete Sensitive Information Guardrail Notebook in Google Colab →**](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Sensitive_Information_Guardrail.ipynb)

[**Or download the notebook from GitHub →**](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Sensitive_Information_Guardrail.ipynb)
{% endhint %}

## Prerequisites

* Fiddler account with [access token](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/reference/settings#credentials)
* Python 3.10+ environment
* Basic understanding of data privacy concepts

## Overview

Fiddler's Fast PII and PHI detection provides enterprise-grade protection against data leakage by automatically detecting sensitive information across multiple categories. These guardrails integrate seamlessly with Fiddler's AI Observability platform, enabling continuous monitoring and automated compliance reporting.

### Key Capabilities

* **PII Detection**: 35+ entity types, including names, addresses, SSN, credit cards, emails, phone numbers
* **PHI Detection**: 7 healthcare-specific entity types for HIPAA compliance
* **Custom Entities**: Define organization-specific sensitive data patterns
* **Real-time Processing**: Sub-second latency for production applications

{% stepper %}
{% step %}
**Set Up Your Environment**

Connect to Fiddler and configure the Sensitive Information Guardrail API:

```python
import json
import pandas as pd
import requests
import time
import fiddler as fdl

# Replace with your actual values
URL = 'https://your_company.fiddler.ai'
TOKEN = 'your_token_here'

# API Configuration
SENSITIVE_INFORMATION_URL = f"{URL}/v3/guardrails/sensitive-information"
FIDDLER_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Connect to Fiddler
fdl.init(url=URL, token=TOKEN)
print("✅ Connected to Fiddler successfully!")
```

{% endstep %}

{% step %}
**Define Helper Functions**

Create reusable functions for interacting with the API:

```python
def get_sensitive_information_response(
    text: str,
    entity_categories: str | list[str] = 'PII',
    custom_entities: list[str] = None,
):
    """
    Detect sensitive information in text.

    Args:
        text: Input text to analyze
        entity_categories: 'PII', 'PHI', 'Custom Entities', or list
        custom_entities: Custom entity patterns (when using 'Custom Entities')

    Returns:
        Tuple of (API response dict, latency in seconds)
    """
    data = {'input': text}

    # Add entity configuration if specified
    if entity_categories != 'PII' or custom_entities:
        data['entity_categories'] = entity_categories
        if custom_entities:
            data['custom_entities'] = custom_entities

    start_time = time.monotonic()

    try:
        response = requests.post(
            SENSITIVE_INFORMATION_URL,
            headers=FIDDLER_HEADERS,
            json={'data': data},
        )
        response.raise_for_status()
        return response.json(), (time.monotonic() - start_time)

    except requests.exceptions.RequestException as e:
        print(f'❌ API call failed: {e}')
        return {}, (time.monotonic() - start_time)


def print_detection_results(response, latency):
    """Display detection results in a formatted way."""
    entities = response.get('fdl_sensitive_information_scores', [])

    print(f"\n🔍 Detection Results (⏱️ {latency:.3f}s)")
    print(f"📊 Total Entities Found: {len(entities)}\n")

    if not entities:
        print("✅ No sensitive information detected.")
        return

    # Group by entity type
    by_type = {}
    for entity in entities:
        label = entity.get('label', 'unknown')
        if label not in by_type:
            by_type[label] = []
        by_type[label].append(entity)

    # Display grouped results
    for label, group in sorted(by_type.items()):
        print(f"🏷️  {label.upper()} ({len(group)} found):")
        for entity in group:
            print(f"   • '{entity['text']}' (confidence: {entity['score']:.3f})")
        print()
```

{% endstep %}

{% step %}
**Example 1: PII Detection**

Detect common personally identifiable information:

```python
# Sample text with various PII types
sample_text = """
I'm John Doe and I live at 1234 Maple Street, Springfield, IL 62704.
You can reach me at john.doe@email.com or call me at (217) 555-1234.
My social security number is 123-45-6789, and I was born on January 15, 1987.
My credit card number is 4111 1111 1111 1111 with CVV 123.
"""

print("🧪 Testing PII Detection")
print("📄 Input Text:")
print(sample_text)

# Call the API with default PII configuration
response, latency = get_sensitive_information_response(sample_text)

# Display results
print_detection_results(response, latency)
```

**Expected Output:**

```
🔍 Detection Results (⏱️ 0.125s)
📊 Total Entities Found: 8

🏷️  PERSON (1 found):
   • 'John Doe' (confidence: 0.987)

🏷️  ADDRESS (1 found):
   • '1234 Maple Street, Springfield, IL 62704' (confidence: 0.945)

🏷️  EMAIL (1 found):
   • 'john.doe@email.com' (confidence: 0.998)

🏷️  PHONE NUMBER (1 found):
   • '(217) 555-1234' (confidence: 0.976)

🏷️  SOCIAL SECURITY NUMBER (1 found):
   • '123-45-6789' (confidence: 0.991)

🏷️  CREDIT CARD NUMBER (1 found):
   • '4111 1111 1111 1111' (confidence: 0.989)

🏷️  CVV (1 found):
   • '123' (confidence: 0.892)

🏷️  DATE OF BIRTH (1 found):
   • 'January 15, 1987' (confidence: 0.923)
```

{% endstep %}

{% step %}
**Example 2: PHI Detection for Healthcare**

Detect protected health information in medical contexts:

```python
# Sample text with PHI information
healthcare_text = """
Patient report: John Smith was prescribed metformin for his diabetes condition.
His health insurance number is HI-987654321, and medical record shows
serial number MED-2024-001 for his glucose monitor device.
Birth certificate number is BC-IL-1987-001234.
Current medication includes aspirin and lisinopril for blood pressure management.
"""

print("🏥 Testing PHI Detection for Healthcare Data")
print("📄 Input Text:")
print(healthcare_text)

# Call the API with PHI configuration
response, latency = get_sensitive_information_response(
    healthcare_text,
    entity_categories="PHI"
)

# Display results
print_detection_results(response, latency)
```

**Expected Output:**

```
🔍 Detection Results (⏱️ 0.098s)
📊 Total Entities Found: 5

🏷️  PERSON (1 found):
   • 'John Smith' (confidence: 0.976)

🏷️  MEDICATION (3 found):
   • 'metformin' (confidence: 0.945)
   • 'aspirin' (confidence: 0.932)
   • 'lisinopril' (confidence: 0.928)

🏷️  HEALTH INSURANCE NUMBER (1 found):
   • 'HI-987654321' (confidence: 0.887)
```

{% endstep %}

{% step %}
**Example 4: Custom Entity Detection**

Define and detect organization-specific sensitive data:

```python
# Sample text with custom entities
custom_text = """
Employee ID: EMP-2024-001, Badge Number: BD-789456
Project code: PROJ-AI-2024, Server hostname: srv-prod-01
API key: sk-abc123xyz789
Internal ticket: TICK-2024-5678
"""

# Define custom entities for your organization
custom_entities = [
    'employee id',
    'badge number',
    'project code',
    'api key',
    'server hostname',
    'ticket number'
]

print("🎯 Testing Custom Entity Detection")
print(f"🏷️ Custom entities: {custom_entities}")

# Call the API with custom entity configuration
response, latency = get_sensitive_information_response(
    custom_text,
    entity_categories='Custom Entities',
    custom_entities=custom_entities
)

# Display results
print_detection_results(response, latency)
```

**Expected Output:**

```
🔍 Detection Results (⏱️ 0.112s)
📊 Total Entities Found: 6

🏷️  EMPLOYEE ID (1 found):
   • 'EMP-2024-001' (confidence: 0.923)

🏷️  BADGE NUMBER (1 found):
   • 'BD-789456' (confidence: 0.911)

🏷️  PROJECT CODE (1 found):
   • 'PROJ-AI-2024' (confidence: 0.897)

🏷️  API KEY (1 found):
   • 'sk-abc123xyz789' (confidence: 0.945)

🏷️  SERVER HOSTNAME (1 found):
   • 'srv-prod-01' (confidence: 0.878)

🏷️  TICKET NUMBER (1 found):
   • 'TICK-2024-5678' (confidence: 0.902)
```

{% endstep %}
{% endstepper %}

## API Reference

### Endpoint

```
POST /v3/guardrails/sensitive-information
```

### Request Format

```json
{
  "data": {
    "input": "Text to analyze for sensitive information",
    "entity_categories": "PII" | "PHI" | "Custom Entities" | ["PII", "PHI"],
    "custom_entities": ["api key", "employee id", "custom pattern"]
  }
}
```

### Request Parameters

| Parameter           | Type            | Description                                                    | Default  |
| ------------------- | --------------- | -------------------------------------------------------------- | -------- |
| `input`             | string          | Text to analyze for sensitive information                      | Required |
| `entity_categories` | string or array | Detection mode(s) to use                                       | "PII"    |
| `custom_entities`   | array           | Custom entity patterns (required when using "Custom Entities") | None     |

### Response Format

```json
{
  "fdl_sensitive_information_scores": [
    {
      "score": 0.987,
      "label": "email",
      "start": 78,
      "end": 100,
      "text": "jane.smith@company.com"
    }
  ]
}
```

### Response Fields

| Field   | Type    | Description                            |
| ------- | ------- | -------------------------------------- |
| `score` | float   | Confidence score (0.0 to 1.0)          |
| `label` | string  | Entity type identifier                 |
| `start` | integer | Character position where entity starts |
| `end`   | integer | Character position where entity ends   |
| `text`  | string  | The detected entity text               |

### Supported Entity Types

#### PII Entities (35+ types)

* **Personal**: person, date\_of\_birth
* **Contact**: email, email\_address, phone\_number, mobile\_phone\_number, landline\_phone\_number, address, postal\_code
* **Financial**: credit\_card\_number, credit\_card\_expiration\_date, cvv, cvc, bank\_account\_number, iban
* **Government IDs**: social\_security\_number, passport\_number, drivers\_license\_number, tax\_identification\_number, cpf, cnpj, national\_health\_insurance\_number
* **Digital**: ip\_address, digital\_signature
* **And more...**

#### PHI Entities (7 types)

* **Medical**: medication, medical\_condition, medical\_record\_number
* **Insurance**: health\_insurance\_number, health\_plan\_id
* **Identifiers**: birth\_certificate\_number, device\_serial\_number

### Code Examples

{% tabs %}
{% tab title="Python - Requests" %}

```python
import requests

url = "https://your_company.fiddler.ai/v3/guardrails/sensitive-information"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

payload = {
    "data": {
        "input": "Contact John at john@email.com",
        "entity_categories": "PII"
    }
}

response = requests.post(url, json=payload, headers=headers)
entities = response.json().get("fdl_sensitive_information_scores", [])

for entity in entities:
    print(f"Found {entity['label']}: {entity['text']} (confidence: {entity['score']})")
```

{% endtab %}

{% tab title="Python - Error Handling" %}

```python
def safe_detect_pii(text):
    """Detect PII with proper error handling."""
    try:
        response = requests.post(
            SENSITIVE_INFORMATION_URL,
            headers=FIDDLER_HEADERS,
            json={'data': {'input': text}},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. Try again or check your connection.")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Authentication failed. Check your API token.")
        elif e.response.status_code == 429:
            print("Rate limit exceeded. Wait before retrying.")
        else:
            print(f"HTTP error {e.response.status_code}: {e.response.text}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

{% endtab %}

{% tab title="cURL" %}

```bash
curl -X POST 'https://your_company.fiddler.ai/v3/guardrails/sensitive-information' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "data": {
      "input": "My SSN is 123-45-6789",
      "entity_categories": "PII"
    }
  }'
```

{% endtab %}
{% endtabs %}

## Next Steps

After completing this quick start:

* Explore other [Fiddler guardrails](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/protect-and-guardrails/guardrails-faq) for comprehensive AI safety
* Review the complete [guardrails documentation](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/getting-started/guardrails) for all available guardrail types
* [Integrate guardrails into your applications ](https://app.gitbook.com/s/82RHcnYWV62fvrxMeeBB/observability/llm/guardrails)for production use

## Summary

You've learned how to:&#x20;

* ✅ Detect 35+ types of PII in text data&#x20;
* ✅ Identify PHI for healthcare compliance&#x20;
* ✅ Configure custom entities for your organization&#x20;
* ✅ Integrate the Fast PII Guardrails API into your applications.

The Fast PII Guardrails offer enterprise-grade protection for sensitive information with sub-second latency, making them ideal for real-time applications while ensuring compliance with privacy regulations such as GDPR, HIPAA, and CCPA.


---

# Guardrails API Reference : Fast PII Model (Sensitive Information Detection)

{% hint style="info" %}
For the free guardrails experience, the Fast PII guardrails are restricted to a 4096 token length. To increase these limits, please contact sales.
{% endhint %}

This Fiddler Trust Model detects and identifies sensitive information including personally identifiable information (PII), protected health information (PHI), and custom-defined entities in text data.

The model supports three detection modes:

1. **PII Detection**: 35+ entity types including personal, financial, and government identifiers
2. **PHI Detection**: 7 healthcare-specific entity types for HIPAA compliance
3. **Custom Entity Detection**: Organization-specific sensitive data patterns

The model requires a single string input and outputs an array of detected entities with confidence scores, labels, and text positions.

**Key Features**

* **High Performance**: 0.1 confidence threshold with top-1024 entity filtering
* **Comprehensive Coverage**: Supports 35+ PII and 7 PHI entity types
* **Custom Entities**: Define organization-specific sensitive patterns
* **Detailed Output**: Returns entity text, type, confidence score, and character positions

**Supported PII Entity Types (35+)**

* **Personal Identifiers**: person, date\_of\_birth
* **Contact Information**: email, email\_address, phone\_number, mobile\_phone\_number, landline\_phone\_number, address, postal\_code
* **Financial Data**: credit\_card\_number, credit\_card\_expiration\_date, cvv, cvc, bank\_account\_number, iban
* **Government IDs**: social\_security\_number, passport\_number, drivers\_license\_number, tax\_identification\_number, cpf, cnpj, national\_health\_insurance\_number
* **Digital Identifiers**: ip\_address, digital\_signature

**Supported PHI Entity Types (7)**

* **Medical Information**: medication, medical\_condition, medical\_record\_number
* **Insurance Data**: health\_insurance\_number, health\_plan\_id
* **Healthcare Identifiers**: birth\_certificate\_number, device\_serial\_number

**How to Use Thresholding**

The Fast PII model uses a default confidence threshold of 0.1, which works well for most applications. Entities with scores above this threshold are considered valid detections. You can adjust this threshold based on your specific requirements:

* **Lower thresholds (< 0.1)**: Catch more potential sensitive data but may include more false positives
* **Higher thresholds (> 0.1)**: Reduce false positives but might miss some valid sensitive information

**Fast PII Model OpenAPI Spec**

```yaml
openapi: 3.0.3
info:
  title: Fiddler Fast PII (Sensitive Information Detection)
  version: 1.0.0
servers:
  - url: "https://{fiddler_endpoint}"
paths:
  /v3/guardrails/sensitive-information:
    post:
      summary: Detect sensitive information (PII, PHI, custom entities) in text
      operationId: detectSensitiveInformation
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  required:
                    - input
                  properties:
                    input:
                      type: string
                      description: The text to analyze for sensitive information
                      example: "John Doe's SSN is 123-45-6789 and email is john@example.com"
                    entity_categories:
                      oneOf:
                        - type: string
                          enum: ["PII", "PHI", "Custom Entities"]
                        - type: array
                          items:
                            type: string
                            enum: ["PII", "PHI", "Custom Entities"]
                      default: "PII"
                      description: Entity detection mode(s) to use
                      example: ["PII", "PHI"]
                    custom_entities:
                      type: array
                      items:
                        type: string
                      description: Custom entity patterns (required when using "Custom Entities" mode)
                      example: ["employee id", "api key", "project code"]
      responses:
        '200':
          description: Successfully detected sensitive information
          content:
            application/json:
              schema:
                type: object
                properties:
                  fdl_sensitive_information_scores:
                    type: array
                    description: Array of detected sensitive entities
                    items:
                      type: object
                      properties:
                        score:
                          type: number
                          format: float
                          description: Confidence score (0.0 to 1.0)
                          example: 0.987
                        label:
                          type: string
                          description: Entity type identifier
                          example: "social_security_number"
                        text:
                          type: string
                          description: The detected entity text
                          example: "123-45-6789"
                        start:
                          type: integer
                          description: Character position where entity starts
                          example: 78
                        end:
                          type: integer
                          description: Character position where entity ends
                          example: 89
        '400':
          description: Bad request (invalid input data or missing custom_entities when required)
        '401':
          description: Unauthorized (missing or invalid Bearer token)
        '413':
          description: Input exceeds 4096 token limit

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

#### Fiddler Trust Service Error Codes

| Error Code  | Reason                                           | Resolution                                                                                                                                                                                                                                                         |
| ----------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 400         | Invalid Input                                    | Adjust API input to follow above API specification.                                                                                                                                                                                                                |
| 401         | Invalid Auth Token                               | The authentication token is invalid or expired. Please double-check your token if it is invalid, and contact <sales@fiddler.ai>                                                                                                                                    |
| 404         | Invalid guardrail endpoint called                | API called must be either `ftl-safety` (safety model), `ftl-response-faithfulness` (faithfulness model), or `sensitive-information` (Fast PII model).                                                                                                              |
| 413         | Input token length exceeds API token size limits | The safety guardrail has a limit of 4096 tokens. The faithfulness guardrail has a limit of 3500 tokens for the context field, and 350 tokens for the response field. The Fast PII guardrail has a limit of 4096 tokens. These limits are higher in our paid plans. |
| 429         | Rate Limits exceeded                             | The rate limits for the free guardrails experience is 2 requests per second, 70 requests per minute, and 200 requests per day. These limits are higher in our paid plans                                                                                           |
| 500/503/504 | Internal Server Error                            | We are experiencing some internal service errors. Please watch #fiddler-guardrails-support on Slack or contact technical support.                                                                                                                                  |
