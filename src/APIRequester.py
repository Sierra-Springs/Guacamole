import pandas as pd
import numpy as np
import os
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth
from Utils.pathDefinitions import *
import requests
from pprint import pprint
import json


class APIRequester:
    def __init__(self):
        self.url = 'https://guacamole.univ-avignon.fr/dblp1/_search'
        with open(authPath) as authfile:
            auth = json.load(authfile)
        self.auth = HTTPBasicAuth(auth["username"], auth["password"])
        self.es = es = Elasticsearch([{'host': 'guacamole.univ-avignon.fr/dblp1/_search',
                                       'port': 9200,
                                       "scheme": "https"}],
                                     basic_auth=(auth["username"], auth["password"])
                                     )
        # Elasticsearch({'host': self.url, 'port': '9200'}, http_auth=(auth["username"], auth["password"]))

    def request(self, research, size=1000):
        payload = {"q": research, "size": size}
        # res = requests.get(self.url, payload, auth=self.auth)
        res = self.es.search(index="test-index", query=payload)
        return res.json()

    def request_by_field(self, field, value, size=1000):
        payload = {"q": f"_{field}:{value}", "size": size}
        res = requests.get(self.url, payload, auth=self.auth)
        return res.json()

    def request_by_doc_id(self, id):  # Retourne le noeud correspondant à l'id avec ses attributs
        return self.get_articles_from_result(self.request_by_field("id", id))

    def request_doc_references_by_id(self, id):  # Retourne les noeuds qui ont l'id parmi leurs references
        return self.get_articles_from_result(self.request_by_field("references", id))

    def get_articles_from_result(self, res):
        return res['hits']['hits']

    def request_articles(self, research, size=1000):
        return self.get_articles_from_result(self.request(research, size=size))


if __name__ == '__main__':
    apiRequester = APIRequester()
    # pprint(apiRequester.request_articles("Romain Deveaud"))
    ##pprint(apiRequester.request_by_doc_id(id=1564531496))

    pprint(apiRequester.request("Romain Deveaud"))
