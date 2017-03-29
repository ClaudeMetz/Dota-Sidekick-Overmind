from ..classes.item import Item

from bs4 import BeautifulSoup


# Crawls dotabuff.com for all available items and saves it to new.db
# --- Incomplete for of this commit ---
def crawl_items(handler, cacher, lang):
    item_list = list_items(cacher, lang)
    for item_name in item_list:
        pass


# Returns a list with the names of all available items
def list_items(cacher, lang):
    html = cacher.get("https://" + lang + ".dotabuff.com/items")
    soup = BeautifulSoup(html, "lxml")

    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(str(item.a["href"].lstrip("/items/")))
    return clean_list


#
def get_item(name, handler, cacher ):
    pass  # soupstrainer
