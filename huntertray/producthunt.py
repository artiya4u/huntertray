import random
import requests

urls = [
    'https://api.producthunt.com/v1/posts?days_ago=0'
]

headers = {
    'cookie': "__cfduid=dfc05e1ccfab4b424d4eb7ba90d4816d31551874540",
    'dnt': "1",
    'authorization': "Bearer 794fc11a800313370e67e5a967d155ea8691955c8f6d5add45b62d93f39b5789",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}


class ProductHunt:
    def __init__(self):
        pass

    @staticmethod
    def getHomePage():
        random.shuffle(urls)
        for i in urls:
            r = requests.get(i, headers=headers)
            try:
                return r.json()['posts']
            except ValueError:
                continue
