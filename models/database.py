from models.db import get_connection
class PersistentModel:
    table_name = None # to be defined by the subclasses
    table_fields = [] # to be defined by the subclasses

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
    def get_one(cls, field=None, value=None): # returns Object or None
        conn = cls.get_connection()
        cursor = conn.cursor()
        fields = ",".join(cls.table_fields)
        if field:
            query = f"SELECT id, {fields} FROM {cls.table_name} WHERE {field}=?"
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            conn.close()
            if row:
                field_data = {field: row[i + 1] for i, field in enumerate(cls.table_fields)}
                return cls( **field_data, id=row[0])

    @classmethod
    def get_all(cls, field=None, value=None): # returns Objects list or []
        conn = cls.get_connection()
        cursor = conn.cursor()
        fields = ",".join(cls.table_fields)
        if field:
            query = f"SELECT id, {fields} FROM {cls.table_name} WHERE {field}=?"
            cursor.execute(query, (value,))
        else:
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
class Recipe(PersistentModel):
    def __init__(self, name="", price=0, steps=None, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.steps = [] if steps is None else steps

    table_name = "recipe"
    table_fields = ["name", "price"]

    @classmethod
    def get_one(cls, field=None, value=None):  # returns Object or None
        recipe = super().get_one(field, value)
        if recipe:
            recipe.steps = Step.get_all("recipe_id", recipe.id)
        return recipe

    @classmethod
    def get_all(cls, field=None, value=None):  # returns Object or None
        recipes = super().get_all(field, value)
        for recipe in recipes:
            recipe.steps = Step.get_all("recipe_id", recipe.id)
        return recipes

    @classmethod
    def get_ingredient(cls, id): #  return a recipe object to be used by other classes that don't need steps to avoid recursivity
        return super().get_one("id", id)

    def save(self):
        super().save() # stores Recipe
        # stores Steps
        for step in self.steps:
            step.save()

    def delete(self):
        # delete Steps
        for step in self.steps:
            self.delete_step(step)
        super().delete() # delete Recipe

    def add_step(self, step):
        self.steps.append(step)
        step.save()
    
    def delete_step(self, step):
        self.steps = [s for s in self.steps if s.id != step.id]
        step.delete()

    def is_complete(self): # Determines if Recipe is complete to be used like ingredient
        if not self.name:
            return False
        if self.steps == []:
            return True
        elif self.steps[-1].resultIngredient_id == self.id:
            return True
        return False

class Step(PersistentModel):
    def __init__(self, recipe_id, sources= None, action_id=None, action=None, resultIngredient_id=None, resultIngredient=None, resultUnit_id=None, resultUnit=None, resultQuantity=None, id=None):
        self.id = id
        self.recipe_id = recipe_id
        self.sources = sources if sources else []
        self.action_id = action_id
        self._action = None
        self.action = action
        self.resultIngredient_id = resultIngredient_id
        self._resultIngredient = None
        self.resultIngredient = resultIngredient
        self.resultUnit_id = resultUnit_id
        self._resultUnit = None
        self.resultUnit = resultUnit
        self.resultQuantity = resultQuantity

    table_name = "step"
    table_fields = ["recipe_id",
                    "action_id",
                    "resultIngredient_id",
                    "resultUnit_id",
                    "resultQuantity"]
    
    @classmethod
    def get_one(cls, field=None, value=None):
        step = super().get_one(field, value)
        if step:
            step.sources = Source.get_all("step_id", step.id)
        return step

    @classmethod
    def get_all(cls, field=None, value=None):
        steps = super().get_all(field, value)
        for step in steps:
            step.sources = Source.get_all("step_id", step.id)
        return steps

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value:
            self._action = value
            self.action_id = value.id
        else:
            if self.action_id:
                self._action = Action.get_one("id", self.action_id)
            else:
                self._action = None

    @property
    def resultIngredient(self):
        return self._resultIngredient
    
    @resultIngredient.setter
    def resultIngredient(self, value):
        if value:
            self._resultIngredient = value
            self.resultIngredient_id = value.id if value else None
        else:
            if self.resultIngredient_id:
                self._resultIngredient =  Recipe.get_ingredient(self.resultIngredient_id)
            else:
                self._resultIngredient = None

    @property
    def resultUnit(self):
        return self._resultUnit
    
    @resultUnit.setter
    def resultUnit(self, value):
        if value:
            self._resultUnit = value
            self.resultUnit_id = value.id if value else None
        else:
            if self.resultUnit_id:
                self._resultUnit = Unit.get_one("id", self.resultUnit_id)
            else:
                self._resultUnit = None

    def save(self):
        super().save() # almacena el Step
        # almacena los Sources
        # borramos todos los sources anteriores por consistencia con eliminados en memoria, se grabaran nuevamente los que estan en memoria
        for source in Source.get_all("step_id", self.id):
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
class Source(PersistentModel):
    def __init__(self, step_id, is_recipe=False, ingredient_id=None, ingredient=None, unit_id=None, unit=None, quantity=0 , id=None):
        self.id = id
        self.step_id = step_id
        self.is_recipe = is_recipe
        self.ingredient_id = ingredient_id
        self._ingredient = None
        self.ingredient = ingredient
        self.unit_id = unit_id
        self._unit = None
        self.unit = unit
        self.quantity = quantity

    table_name = "source"
    table_fields = [
                    "step_id",
                    "is_recipe",
                    "ingredient_id",
                    "unit_id",
                    "quantity"
                    ]

    @property
    def ingredient(self):
        return self._ingredient
    
    @ingredient.setter
    def ingredient(self, value):
        if value:
            self._ingredient = value
            self.ingredient_id = value.id
        else:
            if self.ingredient_id:
                self._ingredient = Recipe.get_ingredient(self.ingredient_id)
            else:
                self._ingredient = None

    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, value):
        if value:
            self._unit = value
            self.unit_id = value.id
        else:
            if self.unit_id:
                self._unit = Unit.get_one("id", self.unit_id)
            else:
                self._unit = None
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
