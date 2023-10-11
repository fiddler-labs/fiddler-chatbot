---
title: "Point Explainability"
slug: "point-explainability"
hidden: false
createdAt: "2022-04-19T20:25:41.102Z"
updatedAt: "2022-05-10T16:23:52.501Z"
---
Fiddler provides powerful visualizations that can explain your model's behavior. These explanations can be queried at an individual prediction level in the **Explain** tab, at a model level in the **Analyze** tab or within the monitoring context in the **Monitor** tab.

Explanations are available in the UI for structured (tabular) and natural language (NLP) models. They are also supported via API using the `fiddler` Python package. Explanations are available for both production and dataset queries.

Fiddler’s explanations are interactive — you can change feature inputs and immediately view an updated prediction and explanation. We have productized several popular **explanation methods** to work fast and at scale:

* SHAP and Fiddler SHAP, game-theory based methods that work for all models, because they only require the ability to ask a model for predictions.
* Integrated Gradients, which is particularly performant for deep learning models with a large number of inputs. It requires the model’s prediction to be mathematically differentiable, and a prediction gradient must be made available to Fiddler.

These methods are discussed in more detail below.
[block:api-header]
{
  "title": "Tabular Models"
}
[/block]
For tabular models, Fiddler’s Point Explanation tool shows how any given model prediction can be attributed to its individual input features.

The following is an example of an explanation for a model predicting the likelihood of customer churn:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b8e4f81-Tabular_Explain.png",
        "Tabular_Explain.png",
        2878,
        1522,
        "#e3e4e9"
      ]
    }
  ]
}
[/block]
A brief tour of the features above:

* ***Explanation Method***: The explanation method is selected from the **Explanation Type** dropdown.
* ***Input Vector***: The far left column contains the input vector. Each input can be adjusted.
* ***Model Prediction***: The box in the upper-left shows the model’s prediction for this input vector.

   * If the model produces multiple outputs (e.g. probabilities in a multiclass classifier), you can click on the prediction field to select and explain any of the output components. This can be particularly useful when diagnosing misclassified examples.

* ***Feature Attributions***: The colored bars on the right represent how the prediction is attributed to the individual feature inputs.

   * A positive value (blue bar) indicates a feature is responsible for driving the prediction in the positive direction.
   * A negative value (red bar) is responsible for driving the prediction in a negative direction.

* ***Baseline Prediction***: The thin colored line just above the bars shows the difference between the baseline prediction and the model prediction. The specifics of the baseline calculation vary with the explanation method, but usually it's approximately the mean prediction of the training/reference data distribution (i.e. the dataset specified when importing the model into Fiddler). The baseline prediction represents a typical model prediction.

**Two numbers** accompany each feature’s attribution bar in the UI.

* *The first number* is the **attribution**. The sum of these values over all features will always equal the difference between the model prediction and a baseline prediction value.

* *The second number*, the percentage in parentheses, is the **feature attribution divided by the sum of the absolute values of all the feature attributions**. This provides an easy to compare, relative measure of feature strength and directionality (notice that negative attributions have negative percentages) and is bounded by ±100%.
[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "An input box labeled **“Top N”** controls how many attributions are visible at once.  If the values don’t add up as described above, it’s likely that weaker attributions are being filtered-out by this control."
}
[/block]
Finally, it’s important to note that **feature attributions combine model behavior with characteristics of the data distribution**.
[block:api-header]
{
  "title": "Language (NLP) Models"
}
[/block]
For language models, Fiddler’s Point Explanation provides the word-level impact on the prediction score when using perturbative methods (SHAP and Fiddler); for the Integrated Gradients method, tokenization can be customized in your model’s `package.py` wrapper script. The explanations are interactive—edit the text, and the explanation updates immediately.

Here is an example of an explanation of a prediction from a sentiment analysis model:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/970a86b-NLP_Explain.png",
        "NLP_Explain.png",
        2738,
        1378,
        "#f9f9fa"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Point Explanation Methods: How to Quantify Prediction Impact of a Feature?"
}
[/block]
**Introduction**

One strategy for explaining the prediction of a machine learning model is to measure the influence that each of its inputs have on the prediction made. This is called Feature Impact.

To measure Feature Impact, **additive attribution methods** can be quite powerful. Fiddler includes:

* **SHAP** and **Fiddler SHAP**, which require only the ability to ask a model for predictions, and are thus suitable across all types of models; no knowledge of the model implementation is necessary.
* **Integrated Gradients**, a method that takes advantage of the gradient vector of the prediction, which is typically available in deep learning models, to efficiently explain complex models with large input dimensionality.

**Additive Attributions**

To explain a prediction with an additive attribution method, we look at how individual features contribute to the *prediction difference*. The prediction difference is a comparison between the prediction as a point in feature space (we refer to this as the *explain-point*), and a counterfactual baseline position (or a distribution of positions), representing an uninteresting or typical model inference.

Each feature is assigned a fraction of the prediction difference for which it is responsible. This fraction is called the feature attribution, and it’s what we show in our explanations.

Additive attribution methods have the following characteristics:

* The sum of feature attributions always equals the prediction difference.
* Features that have no effect on a model’s prediction receive a feature attribution of zero.
* Features that have the identical effect receive the same attribution.
* Features with mutual information share the attribution for any effect that information has on the prediction.

Additionally, each of these methods takes into account interactions between the features (e.g. two features that have no effect individually but in combination change the model output). This is explicitly built into the Shapley value formalism, and is captured in the path integral over gradients in Integrated Gradients.


**Shapley Values and their Approximation**

The Shapley value[<sup>[1]</sup>](#references) (proposed by Lloyd Shapley in 1953) is one way to derive feature attributions. Shapley values distribute the total payoff of a collaborative game across a coalition of cooperating players. They are computed by tabulating the average gain in payoff when a particular player is added to the coalition, over all coalition sizes and permutations of players.

In our case, we consider the “total gains” to be the prediction value, and a “player” is a single model feature. The collaborative “game” is all of the model features cooperating to form a prediction value.

Why do we create “coalitions” with only a subset of the features? In some scenarios, it may be appropriate to replace a feature with a zero value when removed from the coalition (e.g. text models where no mask token is available). In others (e.g. models with dense tabular inputs), values are swapped in from a reference distribution or baseline example as a zero value may have a specific meaning (like zero income on a credit application).

Shapley values have desirable properties including:

* ***Linearity***: If two games are combined, then the total gains correspond to the gains derived from a linear combination of the gains of each game.
* ***Efficiency***: The sum of the values of all players equals the value of the grand coalition, so that all the gain is distributed among the players. In our case, the efficiency property says *the feature attributions should sum to the prediction value*. The attributions can be positive or negative, since a feature can raise or lower a predicted value.

**Approximating Shapley Values**

Computation of exact Shapley values can be extremely computationally expensive—in fact, exponentially so, in the number of input features. Fiddler makes two approximation methods available:

* **SHAP**[<sup>[2]</sup>](#references) (SHapely Additive exPlanations) approximates Shapley values by sampling coalitions according to a combinatorially weighted kernel (compensating for the number of permutations of features in coalitions of different cardinality). It samples the feature space uniformly between baseline-like feature vectors and explain-point-like feature vectors. This has the effect of downsampling behavior in the immediate vicinity of the explain-point, a region where the model may be saturated or uniform in its prediction, and attributions may not be helpful.
* **Fiddler SHAP**[<sup>[3]</sup>](#references) builds on the SHAP approach and is optimized for computing distributions of Shapley values for each feature by comparing the explain-point against a distribution of baselines. This makes it possible to compute confidence intervals around the mean attribution for each feature and identify clusters in attribution space where distinct, individually relevant explanations might be important (e.g. “your loan application was rejected for a set of reasons when compared to applications in your region, and for another set of reasons when compared to applications with the same profession”).

Approximate Shapley value methods can be used to explain nearly any model, since you only need to be able to ask the model for predictions at a variety of positions in the feature space.

**Integrated Gradients**

Another additive attribution method: the Integrated Gradients method.

For models whose prediction is continuous and piecewise differentiable in the feature space, it can be useful to provide additional information through the gradient (slope vector) of a prediction.

Fiddler supports Integrated Gradients (IG)[<sup>[4]</sup>](#references). In this method, an approximate integral tabulates components of the slope along a linear path from baseline to explain-point, and attributes them to respective input features. This has several advantages:

1. For models with very high dimensional feature volumes (e.g. images, text), where differentiable deep-learning models typically excel, this method can be very performant (O(N) vs. the O(2^n) of the Shapley methods)
2. Attributions can be computed for intermediate layers within the model, providing fine-grained model diagnostics. This is naturally extensible to models with hybrid and multimodal inputs.
3. In comparison to local gradients and saliency methods, the IG path integral samples the large-scale behavior of the model and is resistant to amplifying noise in the possibly saturated region around the explain-point.
[block:api-header]
{
  "title": "References"
}
[/block]
1. https://en.wikipedia.org/wiki/Shapley_value
2. S. Lundberg, S Lee. “A Unified Approach to Interpreting Model Predictions.” NeurIPS, 2017 http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf
3. L. Merrick  and A. Taly “The Explanation Game: Explaining Machine Learning Models Using Shapley Values” https://arxiv.org/abs/1909.08128
4. M. Sundararajan, A. Taly, Q. Yan “Axiomatic Attribution for Deep Networks”  http://proceedings.mlr.press/v70/sundararajan17a/sundararajan17a.pdf

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*