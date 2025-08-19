from models.persistent_model import PersistentModel

class Step(PersistentModel):
    table_name = "step"
    table_fields = ["recipe_id",
                    "action_id",
                    "resultIngredient_id",
                    "resultUnit_id",
                    "resultQuantity"]
    
    def __init__(self, recipe_id, action_id=None, resultIngredient_id=None, resultUnit_id=None, resultQuantity=None, id=None):
        super().__init__(id)
        self.recipe_id = recipe_id
        self.action_id = action_id
        self.resultIngredient_id = resultIngredient_id
        self.resultUnit_id = resultUnit_id
        self.resultQuantity = resultQuantity

    def __eq__(self, value) -> bool:
        if (self.recipe_id == value.recipe_id and
            self.action_id == value.action_id and
            self.resultIngredient_id == value.resultIngredient_id and
            self.resultUnit_id == value.resultUnit_id and
            self.resultQuantity == value.resultQuantity):
            return True
        return False