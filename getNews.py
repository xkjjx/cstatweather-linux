from newsapi import NewsApiClient
import json

with open("keys.json") as file:
    key = json.load(file)["NewsKey"]

import requests


def NewsFromBBC():
    # BBC news api
    # following query parameters are used
    # source, sortBy and apiKey
    query_params = {
        "q" : "College Station",
        "source": "cnn",
        "sortBy": "top",
        "apiKey": key
    }
    main_url = " https://newsapi.org/v1/articles"

    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
    print(open_bbc_page)

    # getting all articles in a string article
    article = open_bbc_page["articles"]

    # empty list which will
    # contain all trending news
    results = []

    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        # printing all trending news
        print(i + 1, results[i])

# Driver Code
if __name__ == '__main__':
    NewsFromBBC()

