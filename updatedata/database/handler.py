import sqlite3


# Handles all database interactions
class Handler:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    # Inserts a full object (including appendages) into the current database
    def insert(self, obj):
        if type(obj).__name__ == "Item":
            sql = ("INSERT INTO items VALUES (:name, :dname, :recipe, :quality, :price, :description, :notes, :stats, "
                   ":cooldown, :manacost, :components, :component_in, :shop_info, :lore, :image, :patch, :revision);")
            data = ({"name": obj.name, "dname": obj.dname, "recipe": obj.recipe, "quality": obj.quality,
                     "price": obj.price, "description": obj.description, "notes": obj.notes, "stats": obj.stats,
                     "cooldown": obj.cooldown, "manacost": obj.manacost, "components": obj.components,
                     "component_in": obj.component_in, "shop_info": obj.shop_info, "lore": obj.lore,
                     "image": obj.image, "patch": obj.patch, "revision": obj.revision})
            self.cursor.execute(sql, data)
        else:
            sql_hero = ("INSERT INTO heroes VALUES (:name, :dname, :type, :roles, :prim_atr, :str_base, :str_growth, "
                        ":agi_base, :agi_growth, :int_base, :int_growth, :dmg_min, :dmg_max, :armor, :movement_speed,"
                        ":sight_range, :attack_range, :attack_time, :attack_point, :missile_speed, :lore, :image,"
                        ":patch, :revision);")
            data_hero = ({"name": obj.name, "dname": obj.dname, "type": obj.type, "roles": obj.roles, 
                          "prim_atr": obj.prim_atr, "str_base": obj.str_base, "str_growth": obj.str_growth, 
                          "agi_base": obj.agi_base, "agi_growth": obj.agi_growth, "int_base": obj.int_base,
                          "int_growth": obj.int_growth, "dmg_min": obj.dmg_min, "dmg_max": obj.dmg_max,
                          "armor": obj.armor, "movement_speed": obj.movement_speed, "sight_range": obj.sight_range,
                          "attack_range": obj.attack_range, "attack_time": obj.attack_time, 
                          "attack_point": obj.attack_point, "missile_speed": obj.missile_speed, "lore": obj.lore,
                          "image": obj.image, "patch": obj.patch, "revision": obj.revision})
            self.cursor.execute(sql_hero, data_hero)
            
            sql_ability = ("INSERT INTO abilities VALUES (:hero, :name, :dname, :spot, :hotkey, :behavior, :affects, "
                           ":damage_type, :pierces_SI, :description, :aghs_description, :notes, :stats, :cooldown, "
                           ":manacost, :lore, :image, :patch, :revision);")
            for ability in obj.abilities:
                data_ability = ({"hero": ability.hero, "name": ability.name, "dname": ability.dname,
                                 "spot": ability.spot, "hotkey": ability.hotkey, "behavior": ability.behavior,
                                 "affects": ability.affects, "damage_type": ability.damage_type,
                                 "pierces_SI": ability.pierces_SI, "description": ability.description,
                                 "aghs_description": ability.aghs_description, "notes": ability.notes,
                                 "stats": ability.stats, "cooldown": ability.cooldown, "manacost": ability.manacost,
                                 "lore": ability.lore, "image": ability.image, "patch": ability.patch,
                                 "revision": ability.revision})
                self.cursor.execute(sql_ability, data_ability)

            sql_talent = "INSERT INTO talents VALUES (:hero, :level, :left_talent, :right_talent, :patch, :revision)"
            for talent in obj.talents:
                data_talent = ({"hero": talent.hero, "level": talent.level, "left_talent": talent.left_talent,
                                "right_talent": talent.right_talent, "patch": talent.pach, "revision": talent.revision})
                self.cursor.execute(sql_talent, data_talent)
