from bs4 import BeautifulSoup

# Handles crawling of the overview pages to get lists of all the individual pages to crawl afterwards


# Returns a list with the names of all available items
def list_items(cacher):
    html = cacher.get("dotabuff.com/items")
    soup = BeautifulSoup(html, "lxml")

    raw_list = soup.find_all(class_="cell-xlarge")
    clean_list = []
    for item in raw_list:
        clean_list.append(item.a["href"][7:])
    return clean_list


# Returns a list with the names of all available heroes
def list_heroes(cacher):
    html = cacher.get("dotabuff.com/heroes")
    soup = BeautifulSoup(html, "lxml")

    div = soup.find(class_="hero-grid")
    raw_list = div.find_all("a")
    clean_list = []
    for item in raw_list:
        clean_list.append(item["href"][8:])
    return clean_list
