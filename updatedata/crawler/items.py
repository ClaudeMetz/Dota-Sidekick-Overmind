from bs4 import BeautifulSoup

import urllib.request


# Crawls dotabuff.com for all available items and saves it to new.db

def crawl_items():
    items = item_list()


# Returns a list with the names of all available items
def item_list():
    url = "https://www.dotabuff.com/items"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(html, "lxml")
    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(item.a["href"][7:])
    return clean_list
