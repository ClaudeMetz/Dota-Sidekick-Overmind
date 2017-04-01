from ..classes.ability import Ability


# Crawls the ability hero page on dotabuff.com for abilities
def crawl_abilities(ability_soup, hero):
    abilities = ability_soup.find(class_="col-8").find_all("section")
    spot = 1
    for raw_ability in abilities:
        ability = Ability()
        ability.hero = hero.name
        ability.patch = hero.patch
        ability.revision = hero.revision

        ability.spot = spot
        spot += 1

        header = raw_ability.header
        ability.dname = str(header.contents[0])
        ability.hotkey = hotkey(header)

        ability.name = ability.dname.lower().replace("\'", "").replace(":", "").replace(".", "").replace(" ", "-")
        # Kind of hack-y for now, could be replaced with actual crawling

        body = raw_ability.article.div.div

        ability.behavior = effects(body, "behavior")
        ability.affects = effects(body, "affects")
        ability.damage_type = effects(body, "damage_type")
        ability.pierces_SI = effects(body, "spell_immunity_type")

        ability.description = de_ag_no(body, "description")
        ability.aghs_description = aghs(body)
        ability.notes = de_ag_no(body, "notes")
        ability.stats = stats(body)

        ability.cooldown = cd_mc(body, "cooldown")
        ability.manacost = cd_mc(body, "manacost")

        hero.append(ability)


def hotkey(header):
    if header.big:
        return str(header.big.string)
    else:
        return None


def effects(soup, name):
    sub_soup = soup.find(class_=name)
    if sub_soup:
        return sub_soup.parent.text
    else:
        return None


# description and notes
def de_ag_no(soup, name):
    sub_soup = soup.find(class_=name)
    if sub_soup:
        tags = []
        for element in sub_soup.children:
            tags.append(str(element.text).replace("\\", ""))
        return "|".join(tags)
    else:
        return None


# aghanim_description
def aghs(soup):
    sub_soup = soup.find(class_="aghanim_description")
    if sub_soup:
        return str(sub_soup.text)
    else:
        return None


def stats(soup):
    sub_soup = soup.find(class_="stats")
    if sub_soup:
        tags = []
        for element in sub_soup.children:
            tags.append(str(element.text).replace("\\", ""))
        return "|".join(tags)
    else:
        return None


def cd_mc(soup, name):
    sub_soup = soup.find(class_=name)
    if sub_soup:
        return sub_soup.span.text.replace(" ", " / ")
    else:
        return None
