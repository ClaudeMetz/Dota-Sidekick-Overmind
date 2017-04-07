from ..models.talent import Talent


# Crawls the ability hero page on dotabuff.com for talents
def crawl_talents(ability_soup, hero):
    talents = ability_soup.find(class_="hero-talents").article.table.tbody.find_all("tr")
    for raw_talent in talents:
        talent = Talent()
        talent.hero = hero.name
        talent.patch = hero.patch
        talent.revision = hero.revision

        contents = raw_talent.contents
        talent.left_talent = contents[0].text
        talent.level = int(contents[1].text)
        talent.right_talent = contents[2].text

        hero.talents.append(talent)
