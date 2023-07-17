# -*- coding: utf-8 -*-
"""Ai_Project_testing here_working.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/127h4pv1mtDyIVZb3zxWQH4DKBpjFC1Rr

This Is The Section For Classifier
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd

import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log,sqrt
import re
# %matplotlib inline

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

mails = pd.read_csv('spam.csv',encoding='latin-1')
mails.head()

totalmails = 4825 + 747
trainIndex , testIndex = list(), list()
for i in range(mails.shape[0]):
  if np.random.uniform(0,1) < 0.75:
    trainIndex += {i}
  else:
    testIndex += {i}


trainData = mails.loc[trainIndex]
testData = mails.loc[testIndex]

trainData.reset_index(inplace=True)
trainData.drop(['index'],axis=1,inplace=True)
trainData.head()

testData.reset_index(inplace=True)
testData.drop(['index'],axis=1,inplace=True)
testData.head()

spam_words = ' '.join(list(mails[mails['Category']=='spam']['Message']))
spam_wc = WordCloud(width=512,height=512).generate(spam_words)
plt.figure(figsize=(20,6))
plt.imshow(spam_wc)
plt.axis('off')
plt.show()

vectorizer = CountVectorizer()
x_train = vectorizer.fit_transform(trainData['Message']).toarray()
y_train = trainData['Category']

x_test = vectorizer.transform(testData['Message']).toarray()
y_test = testData['Category']

classifier = MultinomialNB()
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

"""# From Here Begins The Section For NN"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
from sklearn.metrics import confusion_matrix, f1_score

mails = pd.read_csv('spam.csv', encoding='latin-1')
mails['Message'] = mails['Message'].str.lower()

X = mails['Message']
y = mails['Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train).toarray()
X_test = vectorizer.transform(X_test).toarray()

X_train = tf.convert_to_tensor(X_train, dtype=tf.float32)
X_train = tf.sparse.reorder(tf.SparseTensor(indices=tf.where(X_train != 0), values=X_train[X_train != 0], dense_shape=X_train.shape))
X_test = tf.convert_to_tensor(X_test, dtype=tf.float32)
X_test = tf.sparse.reorder(tf.SparseTensor(indices=tf.where(X_test != 0), values=X_test[X_test != 0], dense_shape=X_test.shape))

encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.transform(y_test)

model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print("Loss:", loss)
print("Accuracy:", accuracy)

y_pred_prob = model.predict(X_test)
y_pred = np.where(y_pred_prob > 0.5, 1, 0)

y_pred = encoder.inverse_transform(y_pred.flatten())
y_test = encoder.inverse_transform(y_test)

confusion_mat = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(confusion_mat)

f1 = f1_score(y_test, y_pred, average='binary',pos_label="spam")
print("F1 Score:", f1)

message = "hello my name is mahd tariq"
message = message.lower()
live = [message]
live = vectorizer.transform(live).toarray()
live = tf.convert_to_tensor(live, dtype=tf.float32)

y_pred_prob_live = model.predict(live)
y_pred_live = np.where(y_pred_prob_live > 0.5, 1, 0)
y_pred_live = encoder.inverse_transform(y_pred_live.flatten())


print(y_pred_live)