class RecipeDTO:
    def __init__(self, name: str="", price: float=0, steps=[], id=None):
        self.id = id
        self.name = name
        self.price = price
        self.steps = steps if steps else []

    @classmethod
    def from_model(cls, recipe_model, steps = []):
        """Converts a Recipe model to a DTO"""
        from dto.step_dto import StepDTO
        from services.step_service import StepService

        step_service = StepService()
        return RecipeDTO(
                        recipe_model.name,
                        recipe_model.price,
                        [step_service.get_by_id(step.id) for step in steps],
                        recipe_model.id)

    def to_model(self):
        """Converts this DTO to a Recipe Model ready to persist"""
        from models.recipe_model import Recipe
        
        return Recipe(
                    name = self.name,
                    price = self.price,
                    id = self.id)
        
