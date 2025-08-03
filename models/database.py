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
    table_name = "recipe"
    table_fields = ["name"]
    
    def __init__(self, name="", steps=None, id=None):
        self.id = id
        self.name = name
        self.steps = [] if steps is None else steps

    def save(self):
        super().save() # almacena la receta
        # almacena los Step
        for step in self.steps:
            step.save()

    def delete(self):
        # elimina los Step
        for step in self.steps:
            self.delete_step(step)
        super().delete() #elimina la receta

    def add_step(self, step):
        self.steps.append(step)
        step.save()
    
    def delete_step(self, step):
        self.steps = [s for s in self.steps if s.id != step.id]
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
                    "action_id",
                    "resultIngredient_id",
                    "resultUnit_id",
                    "resultQuantity"]
    
    def __init__(self, recipe_id, sources= None, action=None, resultIngredient=None, resultUnit=None, resultQuantity=None, id=None):
        self.id = id
        self.recipe_id = recipe_id
        self.sources = sources if sources else []
        self._action = None
        self.action = action
        self._resultIngredient = None
        self.resultIngredient = resultIngredient
        self._resultUnit = None
        self.resultUnit = resultUnit
        self.resultQuantity = resultQuantity

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value
        self.action_id = value.id if value else None

    @property
    def resultIngredient(self):
        return self._resultIngredient
    
    @resultIngredient.setter
    def resultIngredient(self, value):
        self._resultIngredient = value
        self.resultIngredient_id = value.id if value else None

    @property
    def resultUnit(self):
        return self._resultUnit
    
    @resultUnit.setter
    def resultUnit(self, value):
        self._resultUnit = value
        self.resultUnit_id = value.id if value else None

    def save(self):
        super().save() # almacena el Step
        # almacena los Sources
        # borramos todos los sources anteriores por consistencia con eliminados en memoria, se grabaran nuevamente los que estan en memoria
        for source in Source.get_by_step(self.id):
            source.delete()
        for source in self.sources:
            if not source.step_id:
                source.step_id = self.id
            source.id = None # borramos el id para que lo vuelva a crear
            source.save()

    def delete(self):
        # elimina los Step
        for source in self.sources:
            self.delete_source(source)
        super().delete() #elimina la receta

    def delete_source(self, source):
        self.sources = [s for s in self.sources if s.id != source.id]
        source.delete()

    @classmethod
    def get_by_recipe(cls, recipe_id):
        if recipe_id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = """ SELECT 
                        id,
                        recipe_id, 
                        action_id,
                        resultIngredient_id,
                        resultUnit_id,
                        resultQuantity
                    FROM step WHERE recipe_id=?"""
        cursor.execute(query, (recipe_id,))
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            all_data.append(cls(
                recipe_id = row[1],
                sources = Source.get_by_step(row[0]),
                action = Action.get_by_id(row[2]),
                resultIngredient = Ingredient.get_by_id(row[3]),
                resultUnit = Unit.get_by_id(row[4]),
                resultQuantity = row[5],
                id = row[0]
            ))
        return all_data
    
    @classmethod
    def get_by_id(cls, id):
        if id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = """ SELECT 
                        id,
                        recipe_id,
                        action_id,
                        resultIngredient_id,
                        resultUnit_id,
                        resultQuantity
                    FROM step WHERE id=?"""
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()
        step =cls(
                recipe_id = row[1],
                sources = Source.get_by_step(row[0]),
                action = Action.get_by_id(row[2]),
                resultIngredient = Ingredient.get_by_id(row[3]),
                resultUnit = Unit.get_by_id(row[4]),
                resultQuantity = row[5],
                id = row[0]
            )
        return step
class Source(PersistentModel):
    table_name = "source"
    table_fields = [
                    "step_id",
                    "is_recipe",
                    "ingredient_id",
                    "unit_id",
                    "quantity"
                    ]

    def __init__(self, step_id, is_recipe=False, ingredient=None, unit=None, quantity=0 , id=None):
        self.id = id
        self.step_id = step_id
        self.is_recipe = is_recipe
        self._ingredient = None
        self.ingredient = ingredient
        self._unit = None
        self.unit = unit
        self.quantity = quantity

    @property
    def ingredient(self):
        return self._ingredient
    
    @ingredient.setter
    def ingredient(self, value):
        self._ingredient = value
        self.ingredient_id = value.id if value else None

    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, value):
        self._unit = value
        self.unit_id = value.id if value else None

    @classmethod
    def get_by_step(cls, step_id):
        if step_id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = """ SELECT 
                        id,
                        step_id,
                        is_recipe,
                        ingredient_id,
                        unit_id,
                        quantity
                    FROM source WHERE step_id=?"""
        cursor.execute(query, (step_id,))
        rows = cursor.fetchall()
        conn.close()
        all_data = []
        for row in rows:
            all_data.append(cls(
                step_id = step_id,
                is_recipe = True if row[2] == 1 else False,
                ingredient = Ingredient.get_by_id(row[3]),
                unit = Unit.get_by_id(row[4]),
                quantity = row[5],
                id = row[0]
            ))
        return all_data

    def get_by_id(cls, id):
        if id is None:
            return
        conn = cls.get_connection()
        cursor = conn.cursor()
        query = """ SELECT 
                        id,
                        step_id,
                        is_recipe,
                        ingredient_id,
                        unit_id,
                        quantity
                    FROM source WHERE id=?"""
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()
        source =cls(
                step_id = row[1],
                is_recipe = True if row[2] == 1 else False,
                ingredient = Ingredient.get_by_id(row[3]),
                unit = Unit.get_by_id(row[4]),
                quantity = row[5],
                id = row[0]
            )
        return source
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

