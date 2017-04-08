from ..models.hero import Hero
from .base import BaseCrawler
from .attributes import crawl_attributes
from .abilities import crawl_abilities
from .talents import crawl_talents

from bs4 import BeautifulSoup, SoupStrainer


# Handles crawling of dotabuff.com's heroes with abilities and talents for the given language
class HeroCrawler(BaseCrawler):
    # Main crawling procedure
    def crawl(self, hero_list):
        for hero_name in hero_list:
            hero = Hero()
            hero.name = hero_name
            hero.patch = self.patch
            hero.revision = self.revision
            hero.image = None

            self.crawl_main_page(hero)

            html = self.cacher.get("dotabuff.com/heroes/" + hero.name + "/abilities")
            strainer = SoupStrainer(class_="content-inner")
            ability_soup = BeautifulSoup(html, "lxml", parse_only=strainer)

            crawl_attributes(ability_soup, hero)
            crawl_abilities(ability_soup, hero)
            crawl_talents(ability_soup, hero)

            # The following is still missing, could be acquired by crawling dota2.com:
            # hero.attack_range, hero.lore, hero.missile_speed, ability.lore

            yield hero

    # Crawls the main hero page on dotabuff.com for dname, type and roles
    def crawl_main_page(self, hero):
        html = self.cacher.get("dotabuff.com/heroes/" + hero.name)
        soup = BeautifulSoup(html, "lxml")

        sub_soup = soup.find(class_="header-content-title").h1.contents
        hero.dname = str(sub_soup[0])
        attr = sub_soup[1].string.split(", ")
        hero.type = attr[0]
        hero.roles = "|".join(attr[1:])
