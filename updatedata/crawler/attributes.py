# Crawls the ability hero page on dotabuff.com for attributes
def crawl_attributes(ability_soup, hero):
    attr = ability_soup.find(class_="hero_attributes").article

    main = attr.find(class_="main").tbody
    hero.prim_atr = main["class"][0][8:11]

    stats = main.tr.next_sibling

    strength = stats.td
    str_stats = strength.string.split(" ")
    hero.str_base = int(str_stats[0])
    hero.str_growth = float(str_stats[1][1:])

    agility = strength.next_sibling
    agi_stats = agility.string.split(" ")
    hero.agi_base = int(agi_stats[0])
    hero.agi_growth = float(agi_stats[1][1:])

    intelligence = agility.next_sibling
    int_stats = intelligence.string.split(" ")
    hero.int_base = int(int_stats[0])
    hero.int_growth = float(int_stats[1][1:])

    other = attr.find(class_="other").tbody

    movement_speed = other.tr
    hero.movement_speed = int(movement_speed.td.next_sibling.string)

    sight_range = movement_speed.next_sibling
    hero.sight_range = str(sight_range.td.next_sibling.string)

    armor = sight_range.next_sibling
    hero.armor = float(armor.td.next_sibling.string)

    attack_time = armor.next_sibling
    hero.attack_time = float(attack_time.td.next_sibling.string)

    damage = attack_time.next_sibling
    damage_range = damage.td.next_sibling.string.split(" - ")
    hero.dmg_min = damage_range[0]
    hero.dmg_max = damage_range[1]

    attack_point = damage.next_sibling
    hero.attack_point = float(attack_point.td.next_sibling.string)
