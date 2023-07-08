import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split #Data testing
from sklearn.feature_extraction.text import CountVectorizer #Data transformation
from sklearn.metrics import accuracy_score #Comparison between real and predicted
import re
import nltk
from nltk import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


train=pd.read_csv("sentiment_model/twitter_training.csv", header=None)
train.columns=['id','information','type','text']
train_data=train
train_data["lower"]=train_data.text.str.lower() #lowercase
train_data["lower"]=[str(data) for data in train_data.lower] #converting all to string
train_data["lower"]=train_data.lower.apply(lambda x: re.sub('[^A-Za-z0-9 ]+', ' ', x)) #regex

stopwords_nltk = nltk.corpus.stopwords
stop_words = stopwords_nltk.words('english')
bow_counts = CountVectorizer(
    tokenizer=word_tokenize,
    stop_words=stop_words, #English Stopwords
    ngram_range=(1, 1) #analysis of one word
)

reviews_train, reviews_test = train_test_split(train_data, test_size=0.2, random_state=0)
X_train_bow = bow_counts.fit_transform(reviews_train.lower)

def formatted_text(text_string):
    # print('==========formatting text ==========')
    # print(text_string)
    return bow_counts.transform(np.array([text_string.lower()]))
