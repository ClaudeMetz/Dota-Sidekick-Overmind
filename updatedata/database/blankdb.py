import sqlite3


# Creates a blank database at the desired path
def blank_db(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(items)
    cursor.execute(heroes)
    cursor.execute(abilities)
    cursor.execute(talents)
    connection.commit()
    connection.close()


# Queries

items = ("CREATE TABLE items ("
         "name TEXT NOT NULL PRIMARY KEY,"
         "dname TEXT NOT NULL,"
         "recipe INTEGER NOT NULL,"
         "quality TEXT NOT NULL,"
         "price INTEGER,"
         "description TEXT,"
         "notes TEXT,"
         "stats TEXT,"
         "cooldown TEXT,"
         "manacost TEXT,"
         "components TEXT,"
         "component_in TEXT,"
         "shop_info TEXT,"
         "lore TEXT,"
         "image TEXT,"
         "patch TEXT NOT NULL,"
         "revision INTEGER NOT NULL);")


heroes = ("CREATE TABLE heroes ("
          "name TEXT NOT NULL PRIMARY KEY,"
          "dname TEXT NOT NULL,"
          "type TEXT NOT NULL,"
          "roles TEXT NOT NULL,"
          "prim_atr TEXT NOT NULL,"
          "str_base INTEGER NOT NULL,"
          "str_growth REAL NOT NULL,"
          "agi_base INTEGER NOT NULL,"
          "agi_growth REAL NOT NULL,"
          "int_base INTEGER NOT NULL,"
          "int_growth REAL NOT NULL,"
          "dmg_min INTEGER NOT NULL,"
          "dmg_max INTEGER NOT NULL,"
          "armor REAL NOT NULL,"
          "movement_speed INTEGER NOT NULL,"
          "sight_range TEXT NOT NULL,"
          "attack_range INTEGER,"
          "attack_time REAL NOT NULL,"
          "attack_point REAL NOT NULL,"
          "missile_speed INTEGER,"
          "lore TEXT,"
          "image TEXT,"
          "patch TEXT NOT NULL,"
          "revision INTEGER NOT NULL);")


abilities = ("CREATE TABLE abilities ("
             "hero TEXT NOT NULL,"
             "name TEXT NOT NULL,"
             "dname TEXT NOT NULL,"
             "spot INTEGER NOT NULL,"
             "hotkey TEXT,"
             "behavior TEXT,"
             "affects TEXT,"
             "damage_type TEXT,"
             "pierces_SI TEXT,"
             "description TEXT,"
             "aghs_description TEXT,"
             "notes TEXT,"
             "stats TEXT,"
             "cooldown TEXT,"
             "manacost TEXT,"
             "lore TEXT,"
             "image TEXT,"
             "patch TEXT NOT NULL,"
             "revision INTEGER NOT NULL,"
             "FOREIGN KEY(hero) REFERENCES heroes(name));")


talents = ("CREATE TABLE talents ("
           "hero TEXT NOT NULL,"
           "level INTEGER NOT NULL,"
           "left_talent TEXT NOT NULL,"
           "right_talent TEXT NOT NULL,"
           "patch TEXT NOT NULL,"
           "revision INTEGER NOT NULL,"
           "FOREIGN KEY(hero) REFERENCES heroes(name));")
