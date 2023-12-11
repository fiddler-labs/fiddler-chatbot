---
title: "Fiddler Query Language (FQL)"
slug: "fiddler-query-language"
excerpt: ""
hidden: false
createdAt: "Mon Nov 20 2023 18:46:44 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Nov 21 2023 21:28:57 GMT+0000 (Coordinated Universal Time)"
---
# Overview

[Custom Metrics](doc:custom-metrics) are defined using the **Fiddler Query Language (FQL)**, a flexible set of constants, operators, and functions which can accommodate a large variety of metrics.

# Definitions

| Term               | Definition                                                                             |
| :----------------- | :------------------------------------------------------------------------------------- |
| Row-level function | A function which executes row-wise for a set of data. Returns a value for each row.    |
| Aggregate function | A function which executes across rows. Returns a single value for a given set of rows. |

# FQL Rules

- Every metric must return either an aggregate or a combination of aggregates (see Aggregate functions below). To clarify, you may not define a metric using purely row-level functions.
- [Column](ref:fdlcolumn) names can be referenced by name either with double quotes ("my_column") or with no quotes (my_column).
- Single quotes (') are used to represent string values.

# Example

Let’s say you wanted to create a Custom Metric for the following metric definition:

- If an event is a false negative, assign a value of -40. If the event is a false positive, assign a value of -400.  If the event is a true positive or true negative, then assign a value of 250.

We can formulate this metric using FQL with the following code:

`average(if(Prediction < 0.5 and Target == 1, -40, if(Prediction >= 0.5 and Target == 0, -400, 250)))`

(Here, we assume `Prediction` is the name of the output column for a binary classifier and `Target` is the name of our label column.)

# Data Types

FQL distinguishes between three data types:

[block:parameters]
{
  "data": {
    "h-0": "Data type",
    "h-1": "Supported values",
    "h-2": "Examples",
    "h-3": "Supported Model Schema Data Types",
    "0-0": "Number",
    "0-1": "Any numeric value (integers and floats are both included)",
    "0-2": "`10`  \n`2.34`",
    "0-3": "[`Data.Type.INTEGER`](ref:fdldatatype)  \n[`DataType.FLOAT`](ref:fdldatatype)",
    "1-0": "Boolean",
    "1-1": "Only `true` and `false`",
    "1-2": "`true`  \n`false`",
    "1-3": "[`DataType.BOOLEAN`](ref:fdldatatype)",
    "2-0": "String",
    "2-1": "Any value wrapped in single quotes (`'`)",
    "2-2": "`'This is a string.'`  \n`'200.0'`",
    "2-3": "[`DataType.CATEGORY`](ref:fdldatatype)  \n[`DataType.STRING`](ref:fdldatatype)"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


# Constants

| Symbol  | Description                            |
| :------ | :------------------------------------- |
| `true`  | Boolean constant for true expressions  |
| `false` | Boolean constant for false expressions |

# Operators

[block:parameters]
{
  "data": {
    "h-0": "Symbol",
    "h-1": "Description",
    "h-2": "Syntax",
    "h-3": "Returns",
    "h-4": "Examples",
    "0-0": "`^`",
    "0-1": "Exponentiation",
    "0-2": "`Number ^ Number`",
    "0-3": "`Number`",
    "0-4": "`2.5 ^ 4`  \n`(column1 - column2)^2`",
    "1-0": "`-`",
    "1-1": "Unary negation",
    "1-2": "`-Number`",
    "1-3": "`Number`",
    "1-4": "`-column1`",
    "2-0": "`*`",
    "2-1": "Multiplication",
    "2-2": "`Number * Number`",
    "2-3": "`Number`",
    "2-4": "`2 * 10`  \n`2 * column1`  \n`column1 * column2`  \n`sum(column1) * 10`",
    "3-0": "`/`",
    "3-1": "Division",
    "3-2": "`Number / Number`",
    "3-3": "`Number`",
    "3-4": "`2 / 10`  \n`2 / column1`  \n`column1 / column2`  \n`sum(column1) / 10`",
    "4-0": "`%`",
    "4-1": "Modulo",
    "4-2": "`Number % Number`",
    "4-3": "`Number`",
    "4-4": "`2 % 10`  \n`2 % column1`  \n`column1 % column2`  \n`sum(column1) % 10`",
    "5-0": "`+`",
    "5-1": "Addition",
    "5-2": "`Number + Number`",
    "5-3": "`Number`",
    "5-4": "`2 + 2`  \n`2 + column1`  \n`column1 + column2`  \n`average(column1) + 2`",
    "6-0": "`-`",
    "6-1": "Subtraction",
    "6-2": "`Number - Number`",
    "6-3": "`Number`",
    "6-4": "`2 - 2`  \n`2 - column1`  \n`column1 - column2`  \n`average(column1) - 2`",
    "7-0": "`<`",
    "7-1": "Less than",
    "7-2": "`Number < Number`",
    "7-3": "`Boolean`",
    "7-4": "`10 < 20`  \n`column1 < 10`  \n`column1 < column2`  \n`average(column2) < 5`",
    "8-0": "`<=`",
    "8-1": "Less than or equal to",
    "8-2": "`Number <= Number`",
    "8-3": "`Boolean`",
    "8-4": "`10 <= 20`  \n`column1 <= 10`  \n`column1 <= column2`  \n`average(column2) <= 5`",
    "9-0": "`>`",
    "9-1": "Greater than",
    "9-2": "`Number > Number`",
    "9-3": "`Boolean`",
    "9-4": "`10 > 20`  \n`column1 > 10`  \n`column1 > column2`  \n`average(column2) > 5`",
    "10-0": "`>=`",
    "10-1": "Greater than or equal to",
    "10-2": "`Number >= Number`",
    "10-3": "`Boolean`",
    "10-4": "`10 >= 20`  \n`column1 >= 10`  \n`column1 >= column2`  \n`average(column2) >= 5`",
    "11-0": "`==`",
    "11-1": "Equals",
    "11-2": "`Number == Number`",
    "11-3": "`Boolean`",
    "11-4": "`10 == 20`  \n`column1 == 10`  \n`column1 == column2`  \n`average(column2) == 5`",
    "12-0": "`!=`",
    "12-1": "Does not equal",
    "12-2": "`Number != Number`",
    "12-3": "`Boolean`",
    "12-4": "`10 != 20`  \n`column1 != 10`  \n`column1 != column2`  \n`average(column2) != 5`",
    "13-0": "`not`",
    "13-1": "Logical NOT",
    "13-2": "`not Boolean`",
    "13-3": "`Boolean`",
    "13-4": "`not true`  \n`not column1`",
    "14-0": "`and`",
    "14-1": "Logical AND",
    "14-2": "`Boolean and Boolean`",
    "14-3": "`Boolean`",
    "14-4": "`true and false`  \n`column1 and column2`",
    "15-0": "`or`",
    "15-1": "Logical OR",
    "15-2": "`Boolean or Boolean`",
    "15-3": "`Boolean`",
    "15-4": "`true or false`  \n`column1 or column2`"
  },
  "cols": 5,
  "rows": 16,
  "align": [
    "left",
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


# Constant functions

| Symbol | Description                                           | Syntax | Returns  | Examples                    |
| :----- | :---------------------------------------------------- | :----- | :------- | :-------------------------- |
| `e()`  | Base of the natural logarithm                         | `e()`  | `Number` | `e() == 2.718281828459045`  |
| `pi()` | The ratio of a circle's circumference to its diameter | `pi()` | `Number` | `pi() == 3.141592653589793` |

# Row-level functions

Row-level functions can be applied either to a single value or to a column/row expression (in which case they are mapped element-wise to each value in the column/row expression).

[block:parameters]
{
  "data": {
    "h-0": "Symbol",
    "h-1": "Description",
    "h-2": "Syntax",
    "h-3": "Returns",
    "h-4": "Examples",
    "0-0": "`if(condition, value1, value2)`",
    "0-1": "Evaluates `condition` and returns `value1` if true, otherwise returns `value2`.  \n`value1` and `value2` must have the same type.",
    "0-2": "`if(Boolean, Any, Any)`",
    "0-3": "`Any`",
    "0-4": "`if(false, 'yes', 'no') == 'no'`  \n`if(column1 == 1, 'yes', 'no')`",
    "1-0": "`length(x)`",
    "1-1": "Returns the length of string `x`.",
    "1-2": "`length(String)`",
    "1-3": "`Number`",
    "1-4": "`length('Hello world') == 11`",
    "2-0": "`to_string(x)`",
    "2-1": "Converts a value `x` to a string.",
    "2-2": "`to_string(Any)`",
    "2-3": "`String`",
    "2-4": "`to_string(42) == '42'`  \n`to_string(true) == 'true'`",
    "3-0": "`is_null(x)`",
    "3-1": "Returns `true` if `x` is null, otherwise returns `false`.",
    "3-2": "`is_null(Any)`",
    "3-3": "`Boolean`",
    "3-4": "`is_null('') == true`  \n`is_null(\"column1\")`",
    "4-0": "`abs(x)`",
    "4-1": "Returns the absolute value of number `x`.",
    "4-2": "`abs(Number)`",
    "4-3": "`Number`",
    "4-4": "`abs(-3) == 3`",
    "5-0": "`exp(x)`",
    "5-1": "Returns `e^x`, where `e` is the base of the natural logarithm.",
    "5-2": "`exp(Number)`",
    "5-3": "`Number`",
    "5-4": "`exp(1) == 2.718281828459045`",
    "6-0": "`log(x)`",
    "6-1": "Returns the natural logarithm (base `e`) of number `x`.",
    "6-2": "`log(Number)`",
    "6-3": "`Number`",
    "6-4": "`log(e) == 1`",
    "7-0": "`log2(x)`",
    "7-1": "Returns the binary logarithm (base `2`) of number `x`.",
    "7-2": "`log2(Number)`",
    "7-3": "`Number`",
    "7-4": "`log2(16) == 4`",
    "8-0": "`log10(x)`",
    "8-1": "Returns the binary logarithm (base `10`) of number `x`.",
    "8-2": "`log10(Number)`",
    "8-3": "`Number`",
    "8-4": "`log10(1000) == 3`",
    "9-0": "`sqrt(x)`",
    "9-1": "Returns the positive square root of number `x`.",
    "9-2": "`sqrt(Number)`",
    "9-3": "`Number`",
    "9-4": "`sqrt(144) == 12`"
  },
  "cols": 5,
  "rows": 10,
  "align": [
    "left",
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


# Aggregate functions

Every Custom Metric must be wrapped in an aggregate function or be a combination of aggregate functions.

| Symbol       | Description                                                                          | Syntax            | Returns  | Examples                 |
| :----------- | :----------------------------------------------------------------------------------- | :---------------- | :------- | :----------------------- |
| `sum(x)`     | Returns the sum of a numeric column or row expression `x`.                           | `sum(Number)`     | `Number` | `sum(column1 + column2)` |
| `average(x)` | Returns the arithmetic mean/average value of a numeric column or row expression `x`. | `average(Number)` | `Number` | `average(2 * column1)`   |
| `count(x)`   | Returns the number of non-null rows of a column or row expression `x`.               | `count(Any)`      | `Number` | `count(column1)`         |

# Built-in metric functions

| Symbol                          | Description                                                                                                 |                                 |          |                                 |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------- | :------------------------------ | :------- | :------------------------------ |
| `jsd(column, baseline)`         | The Jensen-Shannon distance of column `column` with respect to baseline `baseline`.                         | `jsd(Any, String)`              | `Number` | `jsd(column1, 'my_baseline')`   |
| `psi(column, baseline)`         | The population stability index of column `column` with respect to baseline `baseline`.                      | `psi(Any, String)`              | `Number` | `psi(column1, 'my_baseline')`   |
| `is_nullable_violation(column)` | Number of rows with null values in column `column`.                                                         | `is_nullable_violation(Any)`    | `Number` | `psi(column1, 'my_baseline')`   |
| `is_range_violation(column)`    | Number of rows with out-of-range values in column `column`.                                                 | `is_range_violation(Any)`       | `Number` | `is_range_violation(column1)`   |
| `is_type_violation(column)`     | Number of rows with invalid data types in column `column`.                                                  | `is_type_violation(Any)`        | `Number` | `is_type_violation(column1)`    |
| `precision()`                   | Precision between target and output. Available for binary classification model tasks.                       | `precision()`                   | `Number` | `precision()`                   |
| `recall()`                      | Recall between target and output. Available for binary classification model tasks.                          | `recall()`                      | `Number` | `recall()`                      |
| `f1_score()`                    | F1 score between target and output. Available for binary classification model tasks.                        | `f1_score()`                    | `Number` | `f1_score()`                    |
| `fpr()`                         | False positive rate between target and output. Available for binary classification model tasks.             | `fpr()`                         | `Number` | `fpr()`                         |
| `auroc()`                       | Area under the ROC curve between target and output. Available for binary classification model tasks.        | `auroc()`                       | `Number` | `auroc()`                       |
| `g_mean()`                      | `Geometric mean score between target and output. Available for binary classification model tasks.`          | `g_mean()`                      | `Number` | `g_mean()`                      |
| `expected_callibration_error()` | Expected calibration error between target and output. Available for binary classification model tasks.      | `expected_callibration_error()` | `Number` | `expected_callibration_error()` |
| `binary_cross_entropy()`        | Binary cross entropy (log loss) between target and output. Available for binary classification model tasks. | `binary_cross_entropy()`        | `Number` | `binary_cross_entropy()`        |
| `callibrated_threshold()`       | Optimal threshold value for a high TPR and a low FPR. Available for binary classification model tasks.      | `callibrated_threshold()`       | `Number` | `callibrated_threshold()`       |
| `accuracy()`                    | Accuracy score between target and outputs. Available for multiclass classification model tasks.             | `accuracy()`                    | `Number` | `accuracy()`                    |
| `log_loss()`                    | Log loss score between target and outputs. Available for multiclass classification model tasks.             | `log_loss()`                    | `Number` | `log_loss()`                    |
| `r2()`                          | R-squared score between target and output. Available for regression model tasks.                            | `r2()`                          | `Number` | `r2()`                          |
| `mse()`                         | Mean squared error between target and output. Available for regression model tasks.                         | `mse()`                         | `Number` | `mse()`                         |
| `mae()`                         | Mean absolute error between target and output. Available for regression model tasks.                        | `mae()`                         | `Number` | `mae()`                         |
| `mape()`                        | Mean absolute percentage error between target and output. Available for regression model tasks.             | `mape()`                        | `Number` | `mape()`                        |
| `wmape()`                       | Weighted mean absolute percentage error between target and output. Available for regression model tasks.    | `wmape()`                       | `Number` | `wmape()`                       |
| `map()`                         | Mean average precision score. Available for ranking model tasks.                                            | `map()`                         | `Number` | `map()`                         |
| `mean_ndcg()`                   | Mean normalized discounted cumulative gain score. Available for ranking model tasks.                        | `mean_ndcg()`                   | `Number` | `mean_ndcg()`                   |
| `query_count()`                 | Count of ranking queries. Available for ranking model tasks.                                                | `query_count()`                 | `Number` | `query_count()`                 |