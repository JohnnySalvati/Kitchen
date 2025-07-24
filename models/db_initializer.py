# db_initializer.py

import sqlite3

def createDatabase():
    conn = sqlite3.connect('kitchen.db')
    cursor = conn.cursor()

    tables = {
        "unit": """
                    id INTEGER PRIMARY KEY,
                    name TEXT unique,
                    short_name TEXT
        """,
        "action": """
                    id INTEGER PRIMARY KEY,
                    name TEXT unique
        """,
        "ingredient": """
                    id INTEGER PRIMARY KEY,
                    name TEXT unique
        """,
        "recipe": """  
                    id INTEGER PRIMARY KEY,
                    name TEXT unique
        """,
        "step": """
                   id INTEGER PRIMARY KEY,
                   recipe_id INTEGER,
                   ingredient_id INTEGER,
                   unit_id INTEGER,
                   quantity REAL,
                   action_id INTEGER,
                   resultIngredient_id INTEGER,
                   resultUnit_id INTEGER,
                   resultQuantity REAL,
                   FOREIGN KEY(recipe_id) REFERENCES recipe(id),
                   FOREIGN KEY(unit_id) REFERENCES unit(id),
                   FOREIGN KEY(action_id) REFERENCES action(id),
                   FOREIGN KEY(ingredient_id) REFERENCES ingredient(id),
                   FOREIGN KEY(resultIngredient_id) REFERENCES ingredient(id),
                   FOREIGN KEY(resultUnit_id) REFERENCES unit(id)
        """
    }

    for name, definition in tables.items():
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({definition})")

    conn.commit()
    conn.close()