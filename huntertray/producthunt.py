import random
import requests

urls = [
    'https://api.producthunt.com/v1/posts?days_ago=0'
]

headers = {
    'cookie': "__cfduid=dfc05e1ccfab4b424d4eb7ba90d4816d31551874540",
    'dnt': "1",
    'authorization': "Bearer b524e2abbd9fc8fe97495eb834ad8dc2a997190901894e7f25686700e258c9ff",
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
