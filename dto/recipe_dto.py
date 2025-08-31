from dto.unit_dto import UnitDTO
class RecipeDTO:
    def __init__(self, name: str="", price: float=0, unit: UnitDTO= UnitDTO(), quantity: float=0, steps=[], id=None):
        self.id = id
        self.name = name
        self.price = price
        self.unit = unit
        self.quantity = quantity
        self.steps = steps if steps else []

    @classmethod
    def from_model(cls, recipe_model, steps = []):
        """Converts a Recipe model to a DTO"""
        from services.step_service import StepService
        from services.unit_service import UnitService

        step_service = StepService()
        unit_service = UnitService()
        return RecipeDTO(
                        recipe_model.name,
                        recipe_model.price,
                        unit_service.get_by_id(recipe_model.unit_id),
                        recipe_model.quantity,
                        [step_service.get_by_id(step.id) for step in steps],
                        recipe_model.id)

    def to_model(self):
        """Converts this DTO to a Recipe Model ready to persist"""
        from models.recipe_model import Recipe
        
        return Recipe(
                    name = self.name,
                    price = self.price,
                    unit_id = self.unit.id if self.unit.id else 0,
                    quantity= self.quantity,
                    id = self.id)
        
