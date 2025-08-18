class RecipeDTO:
    def __init__(self, name: str="", price: float=0, steps=[], id=None):
        self.id = id
        self.name = name
        self.price = price
        self.steps = steps if steps else []

    @classmethod
    def from_model(cls, recipe_model):
        """Converts a Recipe model to a DTO"""
        from dto.step_dto import StepDTO

        return RecipeDTO(
                        recipe_model.name,
                        recipe_model.price,
                        [StepDTO.from_model(step) for step in recipe_model.steps],
                        recipe_model.id)

    def to_model(self):
        """Converts this DTO to a Recipe Model ready to persist"""
        from models.recipe_model import Recipe

        return Recipe(
                    name = self.name,
                    price = self.price,
                    steps = [step.to_model() for step in self.steps],
                    id = self.id)
        