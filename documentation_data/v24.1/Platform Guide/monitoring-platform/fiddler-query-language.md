---
title: "Fiddler Query Language (FQL)"
slug: "fiddler-query-language"
excerpt: ""
hidden: false
createdAt: "Mon Nov 20 2023 18:46:44 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Jan 04 2024 20:08:36 GMT+0000 (Coordinated Universal Time)"
---
# Overview

[Custom Metrics](doc:custom-metrics) and [Segments](doc:segments) are defined using the **Fiddler Query Language (FQL)**, a flexible set of constants, operators, and functions which can accommodate a large variety of metrics.

# Definitions

| Term               | Definition                                                                             |
| :----------------- | :------------------------------------------------------------------------------------- |
| Row-level function | A function which executes row-wise for a set of data. Returns a value for each row.    |
| Aggregate function | A function which executes across rows. Returns a single value for a given set of rows. |

# FQL Rules

- [Column](ref:fdlcolumn) names can be referenced by name either with double quotes ("my_column") or with no quotes (my_column).
- Single quotes (') are used to represent string values.

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

[block:parameters]
{
  "data": {
    "h-0": "Symbol",
    "h-1": "Description",
    "h-2": "Syntax",
    "h-3": "Returns",
    "h-4": "Examples",
    "0-0": "`jsd(column, baseline)`",
    "0-1": "The Jensen-Shannon distance of column `column` with respect to baseline `baseline`.",
    "0-2": "`jsd(Any, String)`",
    "0-3": "`Number`",
    "0-4": "`jsd(column1, 'my_baseline')`",
    "1-0": "`psi(column, baseline)`",
    "1-1": "The population stability index of column `column` with respect to baseline `baseline`.",
    "1-2": "`psi(Any, String)`",
    "1-3": "`Number`",
    "1-4": "`psi(column1, 'my_baseline')`",
    "2-0": "`null_violation_count(column)`",
    "2-1": "Number of rows with null values in column `column`.",
    "2-2": "`null_violation_count(Any)`",
    "2-3": "`Number`",
    "2-4": "`null_violation_count(column1)`",
    "3-0": "`range_violation_count(column)`",
    "3-1": "Number of rows with out-of-range values in column `column`.",
    "3-2": "`range_violation_count(Any)`",
    "3-3": "`Number`",
    "3-4": "`range_violation_count(column1)`",
    "4-0": "`type_violation_count(column)`",
    "4-1": "Number of rows with invalid data types in column `column`.",
    "4-2": "`type_violation_count(Any)`",
    "4-3": "`Number`",
    "4-4": "`type_violation_count(column1)`",
    "5-0": "`any_violation_count(column)`",
    "5-1": "Number of rows with at least one Data Integrity violation in `column`.",
    "5-2": "`any_violation_count(Any)`",
    "5-3": "`Number`",
    "5-4": "`any_violation_count(column1)`",
    "6-0": "`traffic()`",
    "6-1": "Total row count. Includes null rows.",
    "6-2": "`traffic()`",
    "6-3": "`Number`",
    "6-4": "`traffic()`",
    "7-0": "`tp(class)`",
    "7-1": "True positive count. Available for binary classification and multiclass classification models. For multiclass, `class` is used to specify the positive class.",
    "7-2": "`tp(class=Optional[String])`",
    "7-3": "`Number`",
    "7-4": "`tp()`  \n`tp(class='class1')`",
    "8-0": "`tn(class)`",
    "8-1": "True negative count. Available for binary classification and multiclass classification models. For multiclass, `class` is used to specify the positive class.",
    "8-2": "`tn(class=Optional[String])`",
    "8-3": "`Number`",
    "8-4": "`tn()`  \n`tn(class='class1')`",
    "9-0": "`fp(class)`",
    "9-1": "False positive count. Available for binary classification and multiclass classification models. For multiclass, `class` is used to specify the positive class.",
    "9-2": "`fp(class=Optional[String])`",
    "9-3": "`Number`",
    "9-4": "`fp()`  \n`fp(class='class1')`",
    "10-0": "`fn(class)`",
    "10-1": "False negative count. Available for binary classification and multiclass classification models. For multiclass, `class` is used to specify the positive class.",
    "10-2": "`fn(class=Optional[String])`",
    "10-3": "`Number`",
    "10-4": "`fn()`  \n`fn(class='class1')`",
    "11-0": "`precision(target, threshold)`",
    "11-1": "Precision between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "11-2": "`precision(target=Optional[Any], threshold=Optional[Number])`",
    "11-3": "`Number`",
    "11-4": "`precision()`  \n`precision(target=column1)`  \n`precision(threshold=0.5)`  \n`precision(target=column1, threshold=0.5)`",
    "12-0": "`recall(target, threshold)`",
    "12-1": "Recall between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "12-2": "`recall(target=Optional[Any], threshold=Optional[Number])`",
    "12-3": "`Number`",
    "12-4": "`recall()`  \n`recall(target=column1)`  \n`recall(threshold=0.5)`  \n`recall(target=column1, threshold=0.5)`",
    "13-0": "`f1_score(target, threshold)`",
    "13-1": "F1 score between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "13-2": "`f1_score(target=Optional[Any], threshold=Optional[Number])`",
    "13-3": "`Number`",
    "13-4": "`f1_score()`  \n`f1_score(target=column1)`  \n`f1_score(threshold=0.5)`  \n`f1_score(target=column1, threshold=0.5)`",
    "14-0": "`fpr(target, threshold)`",
    "14-1": "False positive rate between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "14-2": "`fpr(target=Optional[Any], threshold=Optional[Number])`",
    "14-3": "`Number`",
    "14-4": "`fpr()`  \n`fpr(target=column1)`  \n`fpr(threshold=0.5)`  \n`fpr(target=column1, threshold=0.5)`",
    "15-0": "`auroc(target)`",
    "15-1": "Area under the ROC curve between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "15-2": "`auroc(target=Optional[Any])`",
    "15-3": "`Number`",
    "15-4": "`auroc()`  \n`auroc(target=column1)`",
    "16-0": "`geometric_mean(target, threshold)`",
    "16-1": "Geometric mean score between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "16-2": "`geometric_mean(target=Optional[Any], threshold=Optional[Number])`",
    "16-3": "`Number`",
    "16-4": "`geometric_mean()`  \n`geometric_mean(target=column1)`  \n`geometric_mean(threshold=0.5)`  \n`geometric_mean(target=column1, threshold=0.5)`",
    "17-0": "`expected_calibration_error(target)`",
    "17-1": "Expected calibration error between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "17-2": "`expected_calibration_error(target=Optional[Any])`",
    "17-3": "`Number`",
    "17-4": "`expected_calibration_error()`  \n`expected_calibration_error(target=column1)`",
    "18-0": "`log_loss(target)`",
    "18-1": "Log loss (binary cross entropy) between target and output. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "18-2": "`log_loss(target=Optional[Any])`",
    "18-3": "`Number`",
    "18-4": "`log_loss()`  \n`log_loss(target=column1)`",
    "19-0": "`calibrated_threshold(target)`",
    "19-1": "Optimal threshold value for a high TPR and a low FPR. Available for binary classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "19-2": "`calibrated_threshold(target=Optional[Any])`",
    "19-3": "`Number`",
    "19-4": "`calibrated_threshold()`  \n`calibrated_threshold(target=column1)`",
    "20-0": "`accuracy(target, threshold)`",
    "20-1": "Accuracy score between target and outputs. Available for multiclass classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "20-2": "`accuracy(target=Optional[Any], threshold=Optional[Number])`",
    "20-3": "`Number`",
    "20-4": "`accuracy()`  \n`accuracy(target=column1)`  \n`accuracy(threshold=0.5)`  \n`accuracy(target=column1, threshold=0.5)`",
    "21-0": "`log_loss(target)`",
    "21-1": "Log loss score between target and outputs. Available for multiclass classification model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "21-2": "`log_loss(target=Optional[Any])`",
    "21-3": "`Number`",
    "21-4": "`log_loss()`  \n`log_loss(target=column1)`",
    "22-0": "`r2(target)`",
    "22-1": "R-squared score between target and output. Available for regression model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "22-2": "`r2(target=Optional[Any])`",
    "22-3": "`Number`",
    "22-4": "`r2()`  \n`r2(target=column1)`",
    "23-0": "`mse(target)`",
    "23-1": "Mean squared error between target and output. Available for regression model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "23-2": "`mse(target=Optional[Any])`",
    "23-3": "`Number`",
    "23-4": "`mse()`  \n`mse(target=column1)`",
    "24-0": "`mae(target)`",
    "24-1": "Mean absolute error between target and output. Available for regression model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "24-2": "`mae(target=Optional[Any])`",
    "24-3": "`Number`",
    "24-4": "`mae()`  \n`mae(target=column1)`",
    "25-0": "`mape(target)`",
    "25-1": "Mean absolute percentage error between target and output. Available for regression model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "25-2": "`mape(target=Optional[Any])`",
    "25-3": "`Number`",
    "25-4": "`mape()`  \n`mape(target=column1)`",
    "26-0": "`wmape(target)`",
    "26-1": "Weighted mean absolute percentage error between target and output. Available for regression model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "26-2": "`wmape(target=Optional[Any])`",
    "26-3": "`Number`",
    "26-4": "`wmape()`  \n`wmape(target=column1)`",
    "27-0": "`map(target)`",
    "27-1": "Mean average precision score. Available for ranking model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "27-2": "`map(target=Optional[Any])`",
    "27-3": "`Number`",
    "27-4": "`map()`  \n`map(target=column1)`",
    "28-0": "`ndcg_mean(target)`",
    "28-1": "Mean normalized discounted cumulative gain score. Available for ranking model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "28-2": "`ndcg_mean(target=Optional[Any])`",
    "28-3": "`Number`",
    "28-4": "`ndcg_mean()`  \n`ndcg_mean(target=column1)`",
    "29-0": "`query_count(target)`",
    "29-1": "Count of ranking queries. Available for ranking model tasks.  \nIf `target` is specified, it will be used in place of the default target column.",
    "29-2": "`query_count(target=Optional[Any])`",
    "29-3": "`Number`",
    "29-4": "`query_count()`  \n`query_count(target=column1)`"
  },
  "cols": 5,
  "rows": 30,
  "align": [
    "left",
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]
