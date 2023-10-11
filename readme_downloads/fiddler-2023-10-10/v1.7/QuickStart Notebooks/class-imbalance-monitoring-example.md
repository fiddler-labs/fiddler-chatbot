---
title: "Class Imbalance Monitoring Example"
slug: "class-imbalance-monitoring-example"
hidden: false
createdAt: "2023-05-05T13:48:45.125Z"
updatedAt: "2023-05-08T13:41:15.784Z"
---
Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the _class imbalance problem_. This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class. This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the shear number of inferences seen in the majority class. 

This guide showcases how Fiddler uses a class weighting parameter to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach..

Click the following link to get started using Google Colab:

<div class="colab-box">
    <a href="https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/Fiddler_Quickstart_Imbalanced_Data.ipynb" target="_blank">
        <div>
            Open in Google Colab →
        </div>
    </a>
    <div>
            <img src="https://colab.research.google.com/img/colab_favicon_256px.png" />
    </div>
</div>