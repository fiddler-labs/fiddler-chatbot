# A Notebook for Generating Labeled Data for a Multi-class NLP Classification
This notebook generates some useful assets (data/model) that can be used by other examples and notebooks for demonstration and debugging of NLP use cases in Fiddler. In particular, we use the public 20Newsgroups dataset and apply a TF-IDF vectorization to find embedding vectors of text data. Then we split the data into training and test samples and apply a logistic regression model to predict the probability of each the target for each data point. To make the classification task simpler, We group the original targets into more general news categories. In the end, we concatenate all the results in a pandas DataFrame and store both the labeled training and labeled test data as CSV files. This data can be used as baseline and production data in Fiddler when model artifacts and surrogate models are not required. We also store the trained model as a pickle file, for scenarios where access to the model is also required.    

# Fetch the 20 Newsgroup Dataset

First, we retrieve the 20Newsgroups dataset, which is available as part of the scikit-learn real-world dataset. This dataset contains around 18,000 newsgroup posts on 20 topics. The original dataset is available [here](http://qwone.com/~jason/20Newsgroups/).


```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_20newsgroups
```


```python
data_bunch = fetch_20newsgroups(
    subset = 'train',
    shuffle=True,
    random_state=1,
    remove=('headers','footers','quotes')
)
```

A target name from 20 topics is assigned to each data sample in the above dataset, and you can access all the target names by running the: 
```
data_bunch.target_names
```
However, to make this example notebook simpler, we group similar topics and define more general targets as the following:




```python
subcategories = {
    
    'computer': ['comp.graphics',
                 'comp.os.ms-windows.misc',
                 'comp.sys.ibm.pc.hardware',
                 'comp.sys.mac.hardware',
                 'comp.windows.x'],
    
    'politics': ['talk.politics.guns',
                 'talk.politics.mideast',
                 'talk.politics.misc'],
    
    'recreation':['rec.autos',
                  'rec.motorcycles',
                  'rec.sport.baseball',
                  'rec.sport.hockey'],
    
    'science': ['sci.crypt',
                'sci.electronics',
                'sci.med',
                'sci.space',],
    
    'religion': ['soc.religion.christian',
                 'talk.religion.misc',
                 'alt.atheism'],
    
    'forsale':['misc.forsale']
}

main_category = {}
for key,l in subcategories.items():
    for item in l:
        main_category[item] = key
```

Finally, we run some preprocessing and store the data in a pandas DataFrame.


```python
data_prep = [s.replace('\n',' ').strip('\n,=,|,-, ,\,^') for s in data_bunch.data]
data_series = pd.Series(data_prep)
df = pd.DataFrame()
df['original_text'] = data_series
df['original_target'] = [data_bunch.target_names[t] for t in data_bunch.target]
df['target'] = [main_category[data_bunch.target_names[t]] for t in data_bunch.target]
df['original_text'].replace('', np.nan, inplace=True)
df.dropna(axis=0, subset=['original_text'], inplace=True)
df = df[df.target!='politics'] #delete political posts 
df.reset_index(drop=True, inplace=True)
df.head(3)
```

# TF-IDF *Vectorization*

Before training a model for predicting the targets, we transform the text data into a format that can be processed by standard ML models. This transformation step is often called "vectorization" and it is performed by embedding text data into high-dimensional vector space.  In this notebook, we use a simple TF-IDF vectorization method.


```python
from sklearn.feature_extraction.text import TfidfVectorizer
```


```python
embedding_dimension = 250
```


```python
vectorizer = TfidfVectorizer(sublinear_tf=True,
                             max_features=embedding_dimension,
                             min_df=0.01,
                             max_df=0.9,
                             stop_words='english',
                             token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b')

tfidf_sparse = vectorizer.fit_transform(df['original_text'])
embedding_cols = vectorizer.get_feature_names_out()
embedding_col_names = ['tfidf_token_{}'.format(t) for t in embedding_cols]
tfidf_df = pd.DataFrame.sparse.from_spmatrix(tfidf_sparse, columns=embedding_col_names)
```


```python
tfidf_df
```

Now we concatenate the embedding representations and the DataFrame that we generated previously.


```python
df_all = pd.concat([df,tfidf_df], axis=1)
df_all
```

# Train a Multiclass Classifier

We are now ready to train a classifier to predict the labels assigned to each data sample. We use the logistic regression classifier from scikit-learn for this task. We split the data into train and test subsets and we use 25% of data points to train a logistic regression model.


```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
```


```python
df_train, df_test = train_test_split(df_all, test_size=0.75, random_state=1)
```


```python
clf = LogisticRegression(random_state=1).fit(df_train[embedding_col_names], df_train.target)
```


```python
clf_classes = clf.classes_
prob_col_names = ['prob_%s'%c for c in clf_classes]
```

Using the logistic regression classifier for a multi-class classification problem, we get a probability for each target label. We store all the predicted class probabilities as well as the predicted target for each data point in the training and test sets and we compute the prediction accuracy in each set.


```python
predictions_df_train = pd.DataFrame(index=df_train.index)
predictions_df_train['predicted_target'] = clf.predict(df_train[embedding_col_names])
predicted_probs = clf.predict_proba(df_train[embedding_col_names])
for idx,col in enumerate(predicted_probs.T):
    predictions_df_train[prob_col_names[idx]] = col
baseline_df = pd.concat([predictions_df_train, df_train], axis=1)
acc_baseline = sum(baseline_df['predicted_target'] == baseline_df['target'])/baseline_df.shape[0]
print('accuracy on baseline:{:.2f}'.format(acc_baseline))
```


```python
predictions_df_test = pd.DataFrame(index=df_test.index)
predictions_df_test['predicted_target'] = clf.predict(df_test[embedding_col_names])
predicted_probs = clf.predict_proba(df_test[embedding_col_names])
for idx,col in enumerate(predicted_probs.T):
    predictions_df_test[prob_col_names[idx]] = col
production_df = pd.concat([predictions_df_test, df_test], axis=1)
acc_production = sum(production_df['predicted_target'] == production_df['target'])/production_df.shape[0]
print('accuracy on test data:{:.2f}'.format(acc_production))
```

# Store Data and Model


```python
baseline_df.to_csv('20newsgroups_baseline.csv',index=False)
production_df.to_csv('20newsgroups_production.csv',index=False)
```


```python
production_df
```


```python
import pickle
filename = 'LogisticRegression_clf'
pickle.dump(clf, open(filename, 'wb')) 
```
