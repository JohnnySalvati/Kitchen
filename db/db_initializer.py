# db/db_initializer.py
from db.db import get_connection

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    tables = {
        "unit": """
                    id INTEGER PRIMARY KEY,
                    name TEXT unique,
                    short_name TEXT
        """,
        "recipe": """  
                    id INTEGER PRIMARY KEY,
                    name TEXT unique,
                    price REAL,
                    resultUnit_id INTEGER,
                    resultQuantity REAL,
                    FOREIGN KEY(resultUnit_id) REFERENCES unit(id) ON DELETE RESTRICT
        """,
        "source": """  
                    id INTEGER PRIMARY KEY,
                    recipe_id INTEGER,
                    ingredient_id INTEGER,
                    unit_id INTEGER,
                    quantity REAL,
                    FOREIGN KEY(recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
                    FOREIGN KEY(ingredient_id) REFERENCES recipe(id) ON DELETE RESTRICT,
                    FOREIGN KEY(unit_id) REFERENCES unit(id) ON DELETE RESTRICT
        """,
        "unit_converter": """
                    id INTEGER PRIMARY KEY,
                    source_unit_id INTEGER,
                    quantity REAL,
                    target_unit_id INTEGER,
                    UNIQUE(source_unit_id, target_unit_id),
                    FOREIGN KEY(source_unit_id) REFERENCES unit(id) ON DELETE CASCADE,
                    FOREIGN KEY(target_unit_id) REFERENCES unit(id) ON DELETE CASCADE
"""
    }

    for name, definition in tables.items():
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({definition})")

    conn.commit()
    conn.close()