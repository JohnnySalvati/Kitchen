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
    
    def __init__(self, name, steps=[], id=None):
        self.id = id
        self.name = name
        self.steps = steps # lista de objetos Step

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        if self.id is None:
            query = "INSERT INTO recipe (name) VALUES (?)"
            cursor.execute(query, (self.name, ))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE recipe SET name=? WHERE id=?"
            cursor.execute(query, (self.name, self.id))
        conn.commit()
        conn.close()
        # almacena los Step
        for step in self.steps:
            step.save()

    def delete(self):
        if self.id is None:
            return
        conn =self.get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM recipe WHERE id=?"
        cursor.execute(query, (self.id,))
        conn.commit()
        conn.close()
        # elimina los Step
        for step in self.steps:
            step.delete()

    @classmethod
    def get_by_id(cls, id):
        if id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, name FROM recipe WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(name=row[1], steps=Step.get_by_recipe(id), id=id)
        return None

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, name FROM recipe"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            all_data.append(cls(name=row[1], steps=Step.get_by_recipe(row[0]), id=row[0]))
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
    
    def __init__(self, recipe_id, ingredient, unit, quantity, action, resultIngredient, resultUnit, resultQuantity, id=None):
        self.id = id
        self.recipe_id = recipe_id
        self.ingredient = ingredient
        self.unit = unit
        self.quantity = quantity
        self.action = action
        self.resultIngredient = resultIngredient
        self.resultUnit = resultUnit
        self.resultQuantity = resultQuantity

    def save(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        if self.id is None:
            query = """INSERT INTO step (recipe_id,
                                        ingredient_id,
                                        unit_id, 
                                        quantity,
                                        action_id,
                                        resultIngredient_id,
                                        resultUnit_id,
                                        resultQuantity)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, ( self.recipe_id,
                                    self.ingredient.id,
                                    self.unit.id,
                                    self.quantity,
                                    self.action.id,
                                    self.resultIngredient.id, 
                                    self.resultUnit.id,
                                    self.resultQuantity
                                        ))
            self.id = cursor.lastrowid
        else:
            query = """UPDATE step SET recipe_id=?,
                                        ingredient_id=?,
                                        unit_id=?,
                                        quantity=?,
                                        action_id=?,
                                        resultIngredient_id=?,
                                        resultUnit_id=?,
                                        resultQuantity=?
                                WHERE id=?"""
            cursor.execute(query, ( self.recipe_id,
                                    self.ingredient.id,
                                    self.unit.id,
                                    self.quantity,
                                    self.action.id,
                                    self.resultIngredient.id, 
                                    self.resultUnit.id,
                                    self.resultQuantity,
                                    self.id
                                        ))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_recipe(cls, recipe_id):
        if recipe_id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = "SELECT id, recipe_id, ingredient_id, unit_id, quantity, action_id, resultIngredient_id, resultUnit_id, resultQuantity FROM step WHERE recipe_id=?"
        cursor.execute(query, (recipe_id,))
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            all_data.append(cls(
                recipe_id = recipe_id,
                ingredient = Ingredient.get_by_id(row[2]),
                unit = Unit.get_by_id(row[3]),
                quantity = row[4],
                action = Action.get_by_id(row[5]),
                resultIngredient = Ingredient.get_by_id(row[6]),
                resultUnit = Unit.get_by_id(row[7]),
                resultQuantity = row[8],
                id = row[0]
            ))
        return all_data
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


