from models.persistent_model import PersistentModel

class Source(PersistentModel):
    def __init__(self, recipe_id, ingredient_id=None, unit_id=None, quantity=0 , id=None):
        super().__init__(id)
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.unit_id = unit_id
        self.quantity = quantity

    table_name = "source"
    table_fields = [
                    "recipe_id",
                    "ingredient_id",
                    "unit_id",
                    "quantity"
                    ]

   