# db_initializer.py

import sqlite3

def createDatabase():
    conn = sqlite3.connect('kitchen.db')
    cursor = conn.cursor()

# falta validar eliminacion en cascada

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
                   action_id INTEGER,
                   resultIngredient_id INTEGER,
                   resultUnit_id INTEGER,
                   resultQuantity REAL,
                   FOREIGN KEY(recipe_id) REFERENCES recipe(id),
                   FOREIGN KEY(action_id) REFERENCES action(id),
                   FOREIGN KEY(resultIngredient_id) REFERENCES ingredient(id),
                   FOREIGN KEY(resultUnit_id) REFERENCES unit(id)
        """,
        "source": """  
                    id INTEGER PRIMARY KEY,
                    step_id INTEGER,
                    is_recipe INTEGER,
                    ingredient_id INTEGER,
                    unit_id INTEGER,
                    quantity REAL,
                    FOREIGN KEY(step_id) REFERENCES step(id),
                    FOREIGN KEY(ingredient_id) REFERENCES ingredient(id),
                    FOREIGN KEY(unit_id) REFERENCES unit(id)
        """,
    }

    for name, definition in tables.items():
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({definition})")

    conn.commit()
    conn.close()