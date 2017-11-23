# ---------------------- Importing necessary libraries
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from datetime import datetime
import sys
import os
from xgboost.sklearn import XGBClassifier
from sklearn.externals import joblib

# ---------------------- Reading csv file
base_dir = os.getcwd()
os.chdir(os.path.join(base_dir, "ML_Train_Folder"))
df = pd.read_csv("cleaned_news_data.csv")

# ---------------------- Using Tfidf to extract important words

vectorizer = TfidfVectorizer(min_df=0.017, max_df=0.97, stop_words='english',  smooth_idf=True,
                             norm="l2", sublinear_tf=False, use_idf=True, ngram_range=(1, 2))
def top_words(categories, n = 20):
    word_list = []
    for each in categories:
        X = vectorizer.fit_transform(df[df['news_category'] == each]['news_overall'])
        idf = vectorizer.idf_
        diction = dict(zip(vectorizer.get_feature_names(), idf))
        cat_list = sorted(diction, key= diction.get , reverse=True)[:n]
        word_list.extend(cat_list)
    return list(set(word_list))

words = top_words(list(set(df['news_category'])), 200)
for word in words:
    df[word] = df['news_overall'].str.count(word)


# ---------------------- Splitting into train and test
Y = df['news_category']
df.drop(['news_overall','news_category'], axis=1, inplace=True)
X = df
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=125)

# --------------------- Creating model
time1 = datetime.now()
xgbclassifier = XGBClassifier(n_estimators=100, nthread=-1, silent=False, seed=125, learning_rate=0.2, max_depth=4)
xgbmodel = xgbclassifier.fit(X_train, Y_train)
print(xgbmodel.score(X_test, Y_test))
# pred = xgbmodel.predict(X_test)
print(datetime.now()-time1)

# --------------------- Testing Model F1-score -- Weighted: 75.49, Micro: 75.8
from sklearn.metrics import f1_score
labels=list(set(Y_train))
f1_score(y_true=Y_test, y_pred=xgbmodel.predict(X_test), average='weighted')

# --------------------- Saving model
joblib.dump(xgbmodel, 'BOW_XGBClassifier.pkl')

# --------------------- Classification test
df2 = pd.DataFrame()
df2['news_overall'] = ["The Patriots are preparing to face the Dolphins twice in the next three weeks, while the Celtics ready themselves for a test of their winning streak against the Miami Heat on Wednesday night."]
# Expected outcome - Sport
for word in words:
    df2[word] = df2['news_overall'].str.count(word)
df2.drop(['news_overall'], axis=1, inplace=True)
model = joblib.load('BOW_XGBClassifier.pkl')
model.predict(df2)