from models.db import get_connection

class PersistentModel:
    table_name = None # debe ser definido por las subclases
    table_fields = [] # debe ser definido por las subclases

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        field_values = tuple(getattr(self, field) for field in self.table_fields)

        if self.id is None:
            placeholders = ",".join("?" for _ in self.table_fields)
            fields = ",".join(self.table_fields)
            query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
            cursor.execute(query, field_values)
            self.id = cursor.lastrowid
        else:
            set_clause = ", ".join(f"{field}=?" for field in self.table_fields)
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE id=?"
            cursor.execute(query, field_values + (self.id,))

        conn.commit()
        conn.close()

    def delete(self):
        if self.id is None:
            return
        conn =self.get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM {self.table_name} WHERE id=?"
        cursor.execute(query, (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, id):
        if id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        fields = ",".join(cls.table_fields)
        query = f"SELECT id, {fields} FROM {cls.table_name} WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            field_data = {field: row[i + 1] for i, field in enumerate(cls.table_fields)}
            return cls( **field_data, id=row[0])
        return None

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        fields = ",".join(cls.table_fields)
        query = f"SELECT id, {fields} FROM {cls.table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            field_data = {field: row[i + 1] for i, field in enumerate(cls.table_fields)}
            all_data.append(cls(**field_data, id=row[0]))
        return all_data

    @classmethod
    def get_connection(cls):
        return get_connection()
    
class Ingredient(PersistentModel):
    table_name = "ingredient"
    table_fields =  ["name"]

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

class Recipe(PersistentModel):
    # table_name = "recipe"
    # table_fields = ["name"]
    
    def __init__(self, name, steps, id=None):
        self.id = id
        self.name = name
        self.steps = steps #lista de objetos Step

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        if self.id is None:
            query = f"INSERT INTO recipe (name) VALUES (?)"
            cursor.execute(query, (self.name, ))
            self.id = cursor.lastrowid
        else:
            query = f"UPDATE recipe SET name=? WHERE id=?"
            cursor.execute(query, (self.name, self.id))

        conn.commit()
        conn.close()

    def delete(self):
        if self.id is None:
            return
        conn =self.get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM recipe WHERE id=?"
        cursor.execute(query, (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, id):
        if id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = f"SELECT id, name FROM recipe WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(name=row[1], steps=[], id=row[0])
        return None

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = f"SELECT id, name FROM recipe"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            all_data.append(cls(name=row[1], steps=[], id=row[0]))
        return all_data
class Step(PersistentModel):
    table_name = "step"
    table_fields = ["recipe_id",
                    "ingredient_id",
                    "unit_id",
                    "quantity",
                    "action_id",
                    "resultIngredient_id",
                    "resultUnit_id",
                    "resultQuantity"]
    
    def __init__(self, ingredient, unit, quantity, action, resultIngredient, resultQuantity, id=None):
        self.id = id
        self.ingredient = ingredient
        self.unit = unit
        self.quantity = quantity
        self.action = action
        self.resultIngredient = resultIngredient
        self.resultQuantity = resultQuantity

class Unit(PersistentModel):
    table_name = "unit"
    table_fields = ["name", "short_name"]

    def __init__(self, name, short_name, id=None):
        self.id = id
        self.name = name
        self.short_name = short_name

class Action(PersistentModel):
    table_name = "action"
    table_fields = ["name"]

    def __init__(self, name, id=None):
        self.id = id
        self.name = name


