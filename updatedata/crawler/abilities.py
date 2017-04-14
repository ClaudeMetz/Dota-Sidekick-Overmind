from ..models.ability import Ability


# Crawls the ability hero page on dotabuff.com for abilities
def crawl_abilities(ability_soup, hero):
    abilities = ability_soup.find(class_="col-8").find_all("section")
    spot = 1
    for raw_ability in abilities:
        ability = Ability()
        ability.hero = hero.name
        ability.patch = hero.patch
        ability.revision = hero.revision
        ability.image = None

        ability.spot = spot
        spot += 1

        header = raw_ability.header
        dname = str(header.contents[0])
        ability.dname = dname
        ability.name = format_name(dname)  # Kind of hack-y for now, could be replaced with actual crawling
        ability.hotkey = hotkey(header)

        body = raw_ability.article.div.div

        ability.behavior = effects(body, "behavior")
        ability.affects = effects(body, "affects")
        ability.damage_type = effects(body, "damage_type")
        ability.pierces_SI = effects(body, "spell_immunity_type")

        ability.description = de_no_st(body, "description", "p")
        ability.aghs_description = aghs(body)
        ability.notes = de_no_st(body, "notes", "p")
        ability.stats = de_no_st(body, "stats", "div")

        ability.cooldown = cd_mc(body, "cooldown")
        ability.manacost = cd_mc(body, "manacost")

        hero.abilities.append(ability)


# Formats long strings correctly
def parse_strings(string):
    string = " ".join(string.split())
    return string


# Transforms a 'dname' into a 'name'
def format_name(dname):
    return dname.lower().replace("\\", "").replace("\'", "").replace(":", "").replace(".", "").replace(" ", "-")


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


# description, notes and stats
def de_no_st(soup, name, tag):
    sub_soup = soup.find(class_=name)
    if sub_soup:
        tags = []
        for element in sub_soup.find_all(tag):
            tags.append(parse_strings(element.text))
        return "|".join(tags)
    else:
        return None


# aghanim_description
def aghs(soup):
    sub_soup = soup.find(class_="aghanim_description")
    if sub_soup:
        return parse_strings(sub_soup.text)
    else:
        return None


def cd_mc(soup, name):
    sub_soup = soup.find(class_=name)
    if sub_soup:
        return sub_soup.span.text.replace(" ", " / ")
    else:
        return None
