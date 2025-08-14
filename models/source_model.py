from models.persistent_model import PersistentModel

class Source(PersistentModel):
    def __init__(self, step_id, is_recipe=False, ingredient_id=None, ingredient=None, unit_id=None, unit=None, quantity=0 , id=None):
        super().__init__(id)
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
        from models.recipe_model import Recipe
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
        from models.unit_model import Unit
        if value:
            self._unit = value
            self.unit_id = value.id
        else:
            if self.unit_id:
                self._unit = Unit.get_one("id", self.unit_id)
            else:
                self._unit = None
