---
title: "Point Explanations"
slug: "point-explanations"
hidden: true
createdAt: "2022-12-16T23:19:37.269Z"
updatedAt: "2023-09-27T18:29:25.268Z"
---
[block:parameters]
{
  "data": {
    "h-0": "",
    "h-1": "Model Input Type",
    "h-2": "Default Reference Sice",
    "h-3": "Permutations",
    "0-0": "Point Explanations  \nSHAP and Fiddler SHAP",
    "0-1": "Tabular",
    "0-2": "200",
    "0-3": "",
    "1-0": "",
    "1-1": "Text",
    "1-2": "200",
    "1-3": "",
    "2-0": "Global Explanations  \nRandom Ablation Feature Impact (and Importance for models with tabular inputs)",
    "2-1": "Tabular",
    "2-2": "10K",
    "2-3": "",
    "3-0": "",
    "3-1": "Text",
    "3-2": "200",
    "3-3": ""
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


# How to Quantify Prediction Impact of a Feature?

One approach for explaining the prediction of a machine learning model is to measure the influence that each of its inputs has on the prediction made. This is called Feature Impact.

- SHAP and Fiddler SHAP, using Kernel SHAP implementations, are game-theory based methods. They work for all models, because they only require the ability to ask a model for predictions.
- Integrated Gradients, which is particularly performant for deep learning models with a large number of inputs. It requires the model’s prediction to be mathematically differentiable, and a prediction gradient must be made available to Fiddler.
- Tree SHAP, is not enabled by default but can be used for Tree-based model. This is a faster and model-specific method to approximate Shapley values.

These methods are discussed in more detail below.

In addition to the previous out of the box explanation methods, Fiddler allows to bring your own explanation method. This can be customized in your model’s `package.py` wrapper script.

## Tabular Models

## Language (NLP) Models

## Point Explanation Methods:

**Introduction**

To measure Feature Impact, **additive attribution methods** can be quite powerful. Fiddler includes:

- **SHAP** and **Fiddler SHAP**, which require only the ability to ask a model for predictions, and are thus suitable across all types of models; no knowledge of the model implementation is necessary.
- **Integrated Gradients**, a method that takes advantage of the gradient vector of the prediction, which is typically available in deep learning models, to efficiently explain complex models with large input dimensionality.

**Additive Attributions**

To explain a prediction with an additive attribution method, we look at how individual features contribute to the _prediction difference_. The prediction difference is a comparison between the prediction as a point in feature space (we refer to this as the _explain-point_), and a counterfactual baseline position (or a distribution of positions), representing an uninteresting or typical model inference.

Each feature is assigned a fraction of the prediction difference for which it is responsible. This fraction is called the feature attribution, and it’s what we show in our explanations.

Additive attribution methods have the following characteristics:

- The sum of feature attributions always equals the prediction difference.
- Features that have no effect on a model’s prediction receive a feature attribution of zero.
- Features that have the identical effect receive the same attribution.
- Features with mutual information share the attribution for any effect that information has on the prediction.

Additionally, each of these methods takes into account interactions between the features (e.g. two features that have no effect individually but in combination change the model output). This is explicitly built into the Shapley value formalism, and is captured in the path integral over gradients in Integrated Gradients.

**Shapley Values and their Approximation**

The Shapley value[<sup>\[1\]</sup>](#references) (proposed by Lloyd Shapley in 1953) is one way to derive feature attributions. Shapley values distribute the total payoff of a collaborative game across a coalition of cooperating players. They are computed by tabulating the average gain in payoff when a particular player is added to the coalition, over all coalition sizes and permutations of players.

In our case, we consider the “total gains” to be the prediction value, and a “player” is a single model feature. The collaborative “game” is all of the model features cooperating to form a prediction value.

Why do we create “coalitions” with only a subset of the features? In some scenarios, it may be appropriate to replace a feature with a zero value when removed from the coalition (e.g. text models where no mask token is available). In others (e.g. models with dense tabular inputs), values are swapped in from a reference distribution or baseline example as a zero value may have a specific meaning (like zero income on a credit application).

Shapley values have desirable properties including:

- **_Linearity_**: If two games are combined, then the total gains correspond to the gains derived from a linear combination of the gains of each game.
- **_Efficiency_**: The sum of the values of all players equals the value of the grand coalition, so that all the gain is distributed among the players. In our case, the efficiency property says _the feature attributions should sum to the prediction value_. The attributions can be positive or negative, since a feature can raise or lower a predicted value.

**Approximating Shapley Values**

Computation of exact Shapley values can be extremely computationally expensive—in fact, exponentially so, in the number of input features. Fiddler makes two approximation methods available:

- **SHAP**[<sup>\[2\]</sup>](#references) (SHapely Additive exPlanations) approximates Shapley values by sampling coalitions according to a combinatorially weighted kernel (compensating for the number of permutations of features in coalitions of different cardinality). It samples the feature space uniformly between baseline-like feature vectors and explain-point-like feature vectors. This has the effect of downsampling behavior in the immediate vicinity of the explain-point, a region where the model may be saturated or uniform in its prediction, and attributions may not be helpful.
- **Fiddler SHAP**[<sup>\[3\]</sup>](#references) builds on the SHAP approach and is optimized for computing distributions of Shapley values for each feature by comparing the explain-point against a distribution of baselines. This makes it possible to compute confidence intervals around the mean attribution for each feature and identify clusters in attribution space where distinct, individually relevant explanations might be important (e.g. “your loan application was rejected for a set of reasons when compared to applications in your region, and for another set of reasons when compared to applications with the same profession”).

Approximate Shapley value methods can be used to explain nearly any model, since you only need to be able to ask the model for predictions at a variety of positions in the feature space.

**Integrated Gradients**

Another additive attribution method: the Integrated Gradients method.

For models whose prediction is continuous and piecewise differentiable in the feature space, it can be useful to provide additional information through the gradient (slope vector) of a prediction.

Fiddler supports Integrated Gradients (IG)[<sup>\[4\]</sup>](#references). In this method, an approximate integral tabulates components of the slope along a linear path from baseline to explain-point, and attributes them to respective input features. This has several advantages:

1. For models with very high dimensional feature volumes (e.g. images, text), where differentiable deep-learning models typically excel, this method can be very performant (O(N) vs. the O(2^n) of the Shapley methods)
2. Attributions can be computed for intermediate layers within the model, providing fine-grained model diagnostics. This is naturally extensible to models with hybrid and multimodal inputs.
3. In comparison to local gradients and saliency methods, the IG path integral samples the large-scale behavior of the model and is resistant to amplifying noise in the possibly saturated region around the explain-point.

## References

1. <https://en.wikipedia.org/wiki/Shapley_value>
2. S. Lundberg, S Lee. “A Unified Approach to Interpreting Model Predictions.” NeurIPS, 2017 <http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions.pdf>
3. L. Merrick  and A. Taly “The Explanation Game: Explaining Machine Learning Models Using Shapley Values” <https://arxiv.org/abs/1909.08128>
4. M. Sundararajan, A. Taly, Q. Yan “Axiomatic Attribution for Deep Networks”  <http://proceedings.mlr.press/v70/sundararajan17a/sundararajan17a.pdf>

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/demo?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/4d190fd-fiddler-docs-cta-demo.png\" alt=\"Fiddler Demo\"></a>\n</div>"
}
[/block]