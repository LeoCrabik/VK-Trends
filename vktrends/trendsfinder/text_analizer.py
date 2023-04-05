import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from trendsfinder.parser import Data as dt
from trendsfinder.news_creator import OpenAI
from trendsfinder.config import Api_key
import pymorphy2

def get_trends(domain):
    Data = dt(domain=domain)
    df = Data.get_data()
    group_name = Data.get_group_name()

    def remove_links(tweet):
        # Takes a string and removes web links from it
        tweet = re.sub(r'http\S+', '', tweet)  # remove http links
        tweet = re.sub(r'bit.ly/\S+', '', tweet)  # remove bit.ly links
        tweet = tweet.strip('[link]')  # remove [links]
        return tweet

    my_stopwords = nltk.corpus.stopwords.words('russian')
    word_rooter = nltk.stem.snowball.SnowballStemmer('russian', ignore_stopwords=False).stem

    # cleaning master function
    def clean_tweet(tweet, bigrams=False):
        # tweet = remove_users(tweet)
        tweet = remove_links(tweet)
        tweet = tweet.lower()  # lower case
        tweet = re.sub('[^A-Za-z0-9А-Яа-я]+', ' ', tweet)  # strip punctuation
        tweet = re.sub('\s+', ' ', tweet)  # remove double spacing
        tweet = re.sub('([0-9]+)', '', tweet)  # remove numbers
        tweet_token_list = [word for word in tweet.split(' ') if word not in my_stopwords]  # remove stopwords

        morph = pymorphy2.MorphAnalyzer()
        new_list = []
        for word in tweet_token_list:
            p = morph.parse(word)[0]
            root = p.normal_form
            new_list.append(root)
        tweet_token_list = new_list
        if bigrams:
            tweet_token_list = tweet_token_list + [tweet_token_list[i] + '_' + tweet_token_list[i + 1] for i in
                                                   range(len(tweet_token_list) - 1)]
        tweet = ' '.join(tweet_token_list)
        return tweet

    df['cleaned_text'] = [clean_tweet(str(text)) for text in df.text]
    print(df['cleaned_text'])

    # the vectorizer object will be used to transform text to vector form
    vectorizer = CountVectorizer(token_pattern='\w+|\$[\d\.]+|\S+')
    # apply transformation
    try:
        tf = vectorizer.fit_transform(df['cleaned_text'].apply(lambda x: np.str_(x)))
    except:
        tf = vectorizer.fit_transform(df['cleaned_text'])
    # tf_feature_names tells us what word each column in the matric represents
    tf_feature_names = vectorizer.get_feature_names_out()

    number_of_topics = 10

    model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)

    model.fit(tf)

    def display_topics(model, feature_names, no_top_words):
        topic_dict = {}
        for topic_idx, topic in enumerate(model.components_):
            topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(feature_names[i]) for i in
                                                          topic.argsort()[:-no_top_words - 1:-1]]
            topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(topic[i]) for i in
                                                            topic.argsort()[:-no_top_words - 1:-1]]
        return pd.DataFrame(topic_dict)

    no_top_words = 30
    topics = (display_topics(model, tf_feature_names, no_top_words))
    topic_words = topics['Topic 0 words']
    words_line = (", ".join(list(topic_words)))
    topic_weights = topics['Topic 0 weights']
    trends_dict = {'Тема': 'Вес'}
    for word, weight in zip(topic_words[2:], topic_weights[2:]):
        trends_dict[word] = weight
    print(words_line)
    model = OpenAI(
        api_key=Api_key,
        group_name=group_name,
        trends_list=words_line,
    )
    print(model.news())
    return topic_words


if __name__ == "__main__":
    get_trends(domain='ikakprosto')
