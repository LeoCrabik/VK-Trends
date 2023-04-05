import os
import shutil
import requests
from trendsfinder.config import *
from collections import Counter
import pandas as pd


class Data:
    def __init__(self, token=Token, version=Version, domain=Domain, count=Count, stop_list=Stop_list):
        self.token = token
        self.version = version
        self.domain = domain
        self.count = count
        self.stop_list = stop_list
        self.posts = self.get_posts()

    def get_posts(self):
        response = requests.get(
            "https://api.vk.com/method/wall.get/",
            params={
                'access_token': self.token,
                'v': self.version,
                'domain': self.domain,
                'count': self.count,
            }
        )
        data = response.json()['response']['items']
        return data

    def get_data(self):
        text_list = []
        likes_list = []
        reposts_list = []
        views_list = []

        for post in self.posts:
            text = post['text']
            text_list.append(text)

            likes = post['likes']['count']
            likes_list.append(likes)

            reposts = post['reposts']['count']
            reposts_list.append(reposts)

            views = post['views']['count']
            views_list.append(views)

        d = {'text': text_list, 'likes': likes_list, 'reposts': reposts_list, 'views': views_list}
        df = pd.DataFrame(data=d)

        return df

    def get_group_name(self):
        response = requests.get(
            "https://api.vk.com/method/groups.getById/",
            params={
                'access_token': self.token,
                'v': self.version,
                'group_id': self.domain,
            }
        )
        data = response.json()['response'][0]['name']
        return data


if __name__ == "__main__":
    parser = Data(domain='ikakprosto')
    data = parser.get_data()
    data.to_csv('out.csv')
    print(parser.get_group_name())
