---
title: Enrichments (Private Preview)
slug: enrichments-private-preview
excerpt: ''
createdAt: Mon Apr 22 2024 18:53:35 GMT+0000 (Coordinated Universal Time)
updatedAt: Tues Jun 18 2024 20:47:16 GMT+0000 (Coordinated Universal Time)
---

# Enrichments (Private Preview)

* Enrichments are [custom features](../../Python\_Client\_3-x/api-methods-30.md#customfeature) designed to augment data provided in events.
* Enrichments augment existing columns with new metrics that are defined during model onboarding.
* The new metrics are available for use within the analyze, charting, and alerting functionalities in Fiddler.

Below is an example of an enrichment onboarded onto fiddler. See [enrichments](../../Python\_Client\_3-x/api-methods-30.md#fdlenrichment-private-preview) for more details about all enrichments.

```
fiddler_custom_features = [
        fdl.TextEmbedding(
            name='question_cf',
            source_column='question',
            column='question_embedding',
        ),
    ]

model_spec = fdl.ModelSpec(
    inputs=['question'],
    custom_features=fiddler_custom_features,
)
```

***

### Embedding (Private Preview)

Embeddings are a series of numerical representations (a vector) generated by a model for input text. Each number within the vector represents a different dimension of the text input. The meaning of each number depends on how the embedding generating model was trained.

Fiddler uses publicly available embeddings to power the 3D UMAP experience. Because all of the embeddings should be generated by the same model, the points will naturally cluster together in a way such that can enable quick visual anomaly detection.

In order to create embeddings and leverage them for the UMAP visualization, you must create a new `TextEmbedding` enrichment on this embedding column. If you want to bring your own embeddings onto the Fiddler platform, you can direct Fiddler to consume the embeddings vector directly from your data.

For a list of supported embedding models to choose from as well as usage examples, see [here](../../Python\_Client\_3-x/api-methods-30.md#embedding-private-preview).

***

### Centroid Distance (Private Preview)

Fiddler uses KMeans to determine cluster membership for a given enrichment. The Centroid Distance enrichment provides information about the distance between the selected point and the closest centroid. Centroid Distance is automatically added if the `TextEmbedding` enrichment is created for any given model.

For a usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#centroid-distance-private-preview).

***

### Personally Identifiable Information (Private Preview)

The PII (Personally Identifiable Information) enrichment is a critical tool designed to detect and flag the presence of sensitive information within textual data. Whether user-entered or system-generated, this enrichment aims to identify instances where PII might be exposed, helping to prevent privacy breaches and the potential misuse of personal data. In an era where digital privacy concerns are paramount, mishandling or unintentionally leaking PII can have serious repercussions, including privacy violations, identity theft, and significant legal and reputational damage.

For list of PII Entities and usage, see [here](../../Python\_Client\_3-x/api-methods-30.md#personally-identifiable-information-private-preview).

***

### Evaluate (Private Preview)

This enrichment provides classic Metrics for evaluating QA results like Bleu, Rouge and Meteor.

For supported evaluation metrics and usage, see [here](../../Python\_Client\_3-x/api-methods-30.md#evaluate-private-preview).

***

### Textstat (Private Preview)

The Textstat enrichment generates various text statistics such as character/letter count, flesh kinkaid, and others metrics on the target text column.

For supported statistics and usage, see [here](../../Python\_Client\_3-x/api-methods-30.md#textstat-private-preview).

***

### Sentiment (Private Preview)

The Sentiment enrichment uses NLTK's VADER lexicon to generate a score and corresponding sentiment for all specified columns. To enable set enrichment parameter to `sentiment`.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#sentiment-private-preview).

***

### Profanity (Private Preview)

The Profanity enrichment is designed to detect and flag the use of offensive or inappropriate language within textual content. This enrichment is essential for maintaining the integrity and professionalism of digital platforms, forums, social media, and any user-generated content areas.

The profanity enrichment uses searches the target text for words from the below two sources

* The Obscenity List from [https://github.com/surge-ai/profanity/blob/main/profanity\_en.csv](https://github.com/surge-ai/profanity/blob/main/profanity\_en.csv)
* Google banned words [https://github.com/coffee-and-fun/google-profanity-words/blob/main/data/en.txt](https://github.com/coffee-and-fun/google-profanity-words/blob/main/data/en.txt)

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#profanity-private-preview).

***

### Toxicity (Private Preview)

The toxicity enrichment classifies whether a piece of text is toxic or not. A RoBERTa based model is fine-tuned with a mix of toxic and non-toxic data. The model predicts score between 0-1 where scores closer to 1 indicate toxicity.

For performance of enrichment and usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#toxicity-private-preview).

***

### Regex Match (Private Preview)

The Regex Match enrichment is designed to evaluate text responses or content based on their adherence to specific patterns defined by regular expressions (regex). By accepting a regex as input, this metric offers a highly customizable way to check if a string column in the dataset matches the given pattern. This functionality is essential for scenarios requiring precise formatting, specific keyword inclusion, or adherence to particular linguistic structures.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#regex-match-private-preview).

***

### Topic (Private Preview)

The Topic enrichment leverages the capabilities of Zero Shot Classifier [Zero Shot Classifier](https://huggingface.co/tasks/zero-shot-classification) models to categorize textual inputs into a predefined list of topics, even without having been explicitly trained on those topics. This approach to text classification is known as zero-shot learning, a groundbreaking method in natural language processing (NLP) that allows models to intelligently classify text into categories they haven't encountered during training. It's particularly useful for applications requiring the ability to understand and organize content dynamically across a broad range of subjects or themes.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#topic-private-preview).

***

### Banned Keyword Detector (Private Preview)

The Banned Keyword Detector enrichment is designed to scrutinize textual inputs for the presence of specified terms, particularly focusing on identifying content that includes potentially undesirable or restricted keywords. This enrichment operates based on a list of terms defined in its configuration, making it highly adaptable to various content moderation, compliance, and content filtering needs.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#banned-keyword-detector-private-preview).

***

### Language Detector (Private Preview)

The Language Detector enrichment is designed to identify the language of the source text. This enrichment operates from a pretrained text identification model.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#language-detector-private-preview).

***

### Answer Relevance (Private Preview)

The Answer Relevance enrichment evaluates the pertinence of AI-generated responses to their corresponding prompts. This enrichment operates by assessing whether the content of a response accurately addresses the question or topic posed by the initial prompt, providing a simple yet effective binary outcome: relevant or not relevant. Its primary function is to ensure that the output of AI systems, such as chatbots, virtual assistants, and content generation models, remains aligned with the user's informational needs and intentions.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#answer-relevance-private-preview).

***

### Faithfulness (Private Preview)

The Faithfulness (Groundedness) enrichment is a binary indicator designed to evaluate the accuracy and reliability of facts presented in AI-generated text responses. It specifically assesses whether the information used in the response correctly aligns with and is grounded in the provided context, often in the form of referenced documents or data. This enrichment plays a critical role in ensuring that the AI's outputs are not only relevant but also factually accurate, based on the context it was given.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#faithfulness-private-preview).

***

### Coherence (Private Preview)

The Coherence enrichment assesses the logical flow and clarity of AI-generated text responses, ensuring they are structured in a way that makes sense from start to finish. This enrichment is crucial for evaluating whether the content produced by AI maintains a consistent theme, argument, or narrative, without disjointed thoughts or abrupt shifts in topic. Coherence is key to making AI-generated content not only understandable but also engaging and informative for the reader.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#faithfulness-private-preview).

***

### Conciseness (Private Preview)

The Conciseness enrichment evaluates the brevity and clarity of AI-generated text responses, ensuring that the information is presented in a straightforward and efficient manner. This enrichment identifies and rewards responses that effectively communicate their message without unnecessary elaboration or redundancy. In the realm of AI-generated content, where verbosity can dilute the message's impact or confuse the audience, maintaining conciseness is crucial for enhancing readability and user engagement.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#conciseness-private-preview).

***

### Fast Safety (Private Preview)

The Fast safety enrichment evaluates the safety of the text along ten different dimensions: `illegal, hateful, harassing, racist, sexist, violent, sexual, harmful, unethical, jailbreaking` Fast safety is generated through the [Fast Trust Models](llm-based-metrics.md).

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#fast-safety-private-preview).

***

### Fast Faithfulness (Private Preview)

The Fast faithfulness enrichment is designed to evaluate the accuracy and reliability of facts presented in AI-generated text responses. Fast safety is generated through the [Fast Trust Models](llm-based-metrics.md).

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#fast-faithfulness-private-preview).

***

### SQL Validation (Private Preview)

The SQL Validation enrichment is designed to evaluate different query dialects for syntax correctness.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#sql-validation-private-preview).

***

### JSON Validation (Private Preview)

The JSON Validation enrichment is designed to validate JSON for correctness and optionally against a user-defined schema for validation.

For usage example, see [here](../../Python\_Client\_3-x/api-methods-30.md#json-validation-private-preview).

{% include "../../.gitbook/includes/main-doc-footer.md" %}



***