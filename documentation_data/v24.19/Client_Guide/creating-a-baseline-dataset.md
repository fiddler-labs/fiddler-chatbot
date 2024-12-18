---
title: Creating a Baseline Dataset
slug: creating-a-baseline-dataset
excerpt: >-
  This document explains the importance of setting up a baseline dataset for
  monitoring data integrity in production. It provides examples of creating
  different types of baselines such as static pre-production, static production,
  and rolling production.
metadata:
  description: >-
    This document explains the importance of setting up a baseline dataset for
    monitoring data integrity in production. It provides examples of creating
    different types of baselines such as static pre-production, static
    production, and rolling production.
  image: []
  robots: index
createdAt: Thu Apr 04 2024 09:18:41 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 12:22:36 GMT+0000 (Coordinated Universal Time)
---

# Creating a Baseline Dataset

To monitor drift or data integrity issues in production data, baseline data is needed for comparison. A baseline dataset is a **representative sample** of the data you expect to see in production. It represents the ideal data that your model works best on. For this reason, **a baseline dataset should be sampled from your model’s training set.**

**A few things to keep in mind when designing a baseline dataset:**

* It’s important to include **enough data** to ensure you have a representative sample of the training set.
* You may want to consider **including extreme values (min/max)** of each column in your training set so you can properly monitor range violations in production data. However, if you choose not to, you can manually specify these ranges before uploading, see [customizing your dataset schema](customizing-your-model-schema.md).

## Baseline Type: Static Pre-production

```python
dataset = next(fdl.Dataset.list(model_id=model.id))

static_pre_prod_baseline = fdl.Baseline(
    name='static_preprod_1',
    model_id=model.id,
    environment=fdl.EnvType.PRE_PRODUCTION,
    type_=fdl.BaselineType.STATIC,
    dataset_id=dataset.id,
)
static_pre_prod_baseline.create()

print(f'Static pre-production baseline created with id - {static_pre_prod_baseline.id}')
```

## Baseline Type: Static Production

```python
static_prod_baseline = fdl.Baseline(
    name='static_prod_1',
    model_id=model.id,
    environment=fdl.EnvType.PRODUCTION,
    type_=fdl.BaselineType.STATIC,
    start_time=(datetime.now() - timedelta(days=0.5)).timestamp(),
    end_time=(datetime.now() - timedelta(days=0.25)).timestamp(),
)
static_prod_baseline.create()

print(f'Static production baseline created with id - {static_prod_baseline.id}')
```

## Baseline Type: Rolling Production

```python
rolling_prod_baseline = fdl.Baseline(
    name='rolling_prod_1',
    model_id=model.id,
    environment=fdl.EnvType.PRODUCTION,
    type_=fdl.BaselineType.ROLLING,
    window_bin_size=fdl.WindowBinSize.WEEK,
    offset_delta=4,
)
rolling_prod_baseline.create()

print(f'Rolling production baseline created with id - {rolling_prod_baseline.id}')
```

## List Baselines

```python
for baseline in fdl.Baseline.list(model_id=model.id):
    print(f'Dataset: {baseline.id} - {baseline.name}')
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

