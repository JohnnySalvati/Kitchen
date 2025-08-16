from models.step_model import Step

class RecipeDTO:
    def __init__(self, name: str="", price: float=0, steps: list[Step]=[], id=None):
        self.id = id
        self.name = name
        self.price = price
        self.steps = steps if steps else []

    @classmethod
    def from_model(cls, recipe_model):
        """Converts a Recipe model to a DTO"""
        return RecipeDTO(recipe_model.name,
                        recipe_model.price,
                        recipe_model.steps,
                        recipe_model.id)

    def to_model(self, RecipeModelClass):
        """Converts this DTO to a Recipe Model ready to persist"""
        return RecipeModelClass(name = self.name,
                                price = self.price,
                                steps = self.steps,
                                id = self.id)