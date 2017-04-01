from ..classes.item import Item
from .base import BaseCrawler

from bs4 import BeautifulSoup, SoupStrainer


# Handles crawling of dotabuff.com's items for the given language
class ItemCrawler(BaseCrawler):
    # Main crawling procedure
    def crawl(self, item_list):
        for item_name in item_list:
            item = self.crawl_item(item_name)
            self.handler.insert(item)

    # Crawls the given item and returns it as an object
    def crawl_item(self, name):
        html = self.cacher.get("dotabuff.com/items/" + name)
        strainer = SoupStrainer(class_="item-tooltip")
        soup = BeautifulSoup(html, "lxml", parse_only=strainer)
        item = Item()

        item.patch = self.patch
        item.revision = 0  # Needs to be sorted out

        item.name = name
        item.dname = str(soup.find(class_="avatar").div.img["title"])
        item.lore = str(soup.find(class_="lore").string).replace("\\", "")
        item.image = None  # Needs to be sorted out

        item.recipe = recipe(soup)
        item.quality = quality(soup, name)
        item.price = price(soup)
        item.description = de_no_st(soup, "description")
        item.notes = de_no_st(soup, "notes")
        item.stats = de_no_st(soup, "stats")
        item.cooldown = cooldown(soup)
        item.manacost = manacost(soup)
        item.components = components(soup)
        item.component_in = component_in(soup)
        item.shop_info = shop(soup)

        return item


def recipe(soup):
    sub_soup = soup.find(class_="item-builds-from")
    if sub_soup:
        items = sub_soup.find_all(class_="item")
        for item in items:
            if "recipe" in item.a["href"]:
                return int(item.find(class_="cost").span.string)
    else:
        return None


def quality(soup, name):
    if name == "shadow-amulet":
        return "component"
    else:
        return str(soup.find(class_="name").span["class"][0][8:])


def price(soup):
    sub_soup = soup.find(class_="price")
    cost = sub_soup.span.span
    if cost:
        return int(cost.string)
    else:
        return None


# description, notes and stats
def de_no_st(soup, s):
    sub_soup = soup.find(class_=s)
    if sub_soup:
        tags = []
        for element in sub_soup.children:
            tags.append(str(element.text).replace("\\", ""))
        return "|".join(tags)
    else:
        return None


def cooldown(soup):
    sub_soup = soup.find(class_="cooldown")
    if sub_soup:
        return float(sub_soup.span.span.string)
    else:
        return None


def manacost(soup):
    sub_soup = soup.find(class_="manacost")
    if sub_soup:
        cost = int(sub_soup.span.span.string)
        if cost == 0:
            return None
        else:
            return cost
    else:
        return None


def component_in(soup):
    sub_soup = soup.find(class_="item-builds-into")
    if sub_soup:
        items = sub_soup.find_all(class_="icon")
        tags = []
        for item in items:
            tags.append(str(item.div.a["href"][7:]))
        return "|".join(tags)
    else:
        return None


def components(soup):
    sub_soup = soup.find(class_="item-builds-from")
    if sub_soup:
        items = sub_soup.find_all(class_="icon")
        tags = []
        for item in items:
            name = str(item.div.a["href"][7:])
            if not name.startswith("recipe"):
                tags.append(name)
        return "|".join(tags)
    else:
        return None


def shop(soup):
    sub_soup = soup.find_all(class_="shop")
    if sub_soup:
        tags = []
        for s in sub_soup:
            tags.append(str(s.string))
        return "|".join(tags)
    else:
        return None
