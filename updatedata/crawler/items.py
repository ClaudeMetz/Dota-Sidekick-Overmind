from bs4 import BeautifulSoup


# Crawls dotabuff.com for all available items and saves it to new.db

def crawl_items(cacher):
    items = item_list(cacher)


# Returns a list with the names of all available items
def item_list(cacher):
    html = cacher.get("https://www.dotabuff.com/items")
    soup = BeautifulSoup(html, "lxml")

    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(item.a["href"].lstrip("/items/"))
    return clean_list
