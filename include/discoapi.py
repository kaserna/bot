# Класс для работы с API
from urllib import parse, request
import re

import requests


class DiscoAPI:
    json_data = None
    query = None

    def youtube(self, finds):
        query = parse.urlencode({'search_query': finds})
        html = request.urlopen('http://www.youtube.com/results?' + query)
        results = re.findall('href=\"/watch\\?v=(.{11})', html.read().decode())
        return results

    def fox(self):
        response = requests.get('https://some-random-api.ml/img/fox')
        return response

    def anime(self):
        response = requests.get('https://some-random-api.ml/animu/pat')
        return response

    def anime2(self):
        response = requests.get('https://some-random-api.ml/animu/wink')
        return response
