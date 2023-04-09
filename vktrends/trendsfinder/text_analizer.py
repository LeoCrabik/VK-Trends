import nltk
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from trendsfinder.parser import Data as dt
from trendsfinder.news_creator import OpenAI
from trendsfinder.config import *
import pymorphy2



class TopicsFinder:
    def __init__(self, domain):
        self.domain = domain
        Data = dt(domain=domain)
        self.df = Data.get_data()
        self.group_name = Data.get_group_name()
        self.df['cleaned_text'] = [self.clean_tweet(str(text)) for text in self.df.text]
        # the vectorizer object will be used to transform text to vector form
        self.vectorizer = CountVectorizer(token_pattern='\w+|\$[\d\.]+|\S+')
        # apply transformation
        try:
            tf = self.vectorizer.fit_transform(self.df['cleaned_text'].apply(lambda x: np.str_(x)))
        except:
            tf = self.vectorizer.fit_transform(self.df['cleaned_text'])
        # tf_feature_names tells us what word each column in the matric represents
        self.tf_feature_names = self.vectorizer.get_feature_names_out()

        self.number_of_topics = 10

        self.model = LatentDirichletAllocation(n_components=self.number_of_topics, random_state=0)

        self.model.fit(tf)

        self.no_top_words = 10
        self.topics = (self.display_topics())
        # self.topic_words = self.topics['Topic 0 words']
        # self.words_line = (", ".join(list(self.topic_words)))
        # self.topic_weights = self.topics['Topic 0 weights']
        # self.trends_dict = {'Тема': 'Вес'}
        # for word, weight in zip(self.topic_words, self.topic_weights):
        #     self.trends_dict[word] = weight
        # print(self.words_line)
        # for item in self.trends_dict.items():
        #     print(item)
        words_list = []
        for n in range(0, 10):
            topic_words = self.topics['Topic %d words' % n]
            words_list += (list(topic_words))
        # print(words_list)
        counted_dict = {i: words_list.count(i) for i in words_list};
        # print(counted_dict)
        self.sorted_dict_ = sorted(counted_dict.items(), key=lambda x: x[1], reverse=True)
        print(self.sorted_dict_)
        self.topic_words_ = [item[0] for item in self.sorted_dict_]
        print(self.topic_words_)
        print(' '.join(self.topic_words_))
        self.category = OpenAI(self.topic_words_, Api_key).news()


    def clean_tweet(self, tweet):
        # Takes a string and removes web links from it
        tweet = re.sub(r'http\S+', '', tweet)  # remove http links
        tweet = re.sub(r'bit.ly/\S+', '', tweet)  # remove bit.ly links
        tweet = tweet.strip('[link]')  # remove [links]

        my_stopwords = nltk.corpus.stopwords.words('russian')+Stop_list
        tweet = re.sub('[^A-Za-z0-9А-Яа-я]+', ' ', tweet)  # strip punctuation
        tweet = re.sub('\s+', ' ', tweet)  # remove double spacing
        tweet = re.sub('([0-9]+)', '', tweet)  # remove numbers
        tweet = tweet.lower()
        # print(tweet)

        # print(tweet_token_list)
        morph = pymorphy2.MorphAnalyzer()
        tweet_token_list = [morph.parse(word)[0].normal_form for word in tweet.split(' ')]
        tweet_token_list = [word for word in tweet_token_list if word not in my_stopwords]  # remove stopwords

        tweet = ' '.join(tweet_token_list)

        return tweet

    def display_topics(self):
        topic_dict = {}
        for topic_idx, topic in enumerate(self.model.components_):
            topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(self.tf_feature_names[i]) for i in
                                                          topic.argsort()[:-self.no_top_words - 1:-1]]
            topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(topic[i]) for i in
                                                            topic.argsort()[:-self.no_top_words - 1:-1]]
        return pd.DataFrame(topic_dict)

    def get_content(self):

        return {
            'data': self.topic_words_,
            'group_name': self.domain,
            'category': self.category
        }


if __name__ == "__main__":
    topics = TopicsFinder(domain='ikakprosto')

