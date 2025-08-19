class SourceDTO():
    def __init__(self,
                step_id=None,
                ingredient=None,
                unit=None,
                quantity=0,
                id=None):
        from dto.recipe_dto import RecipeDTO
        from dto.unit_dto import UnitDTO

        self.id = id
        self.step_id = step_id
        self.ingredient = ingredient if ingredient else RecipeDTO()
        self.unit = unit if unit else UnitDTO()
        self.quantity = quantity

    @classmethod
    def from_model(cls, source_model):
        """Converts a Source model to a DTO"""
        from services.recipe_service import RecipeService
        from services.unit_service import UnitService

        recipe_service = RecipeService()
        unit_service = UnitService()
        return SourceDTO(
                source_model.step_id,
                recipe_service.get_ingredient(source_model.ingredient_id),
                unit_service.get_by_id(source_model.unit_id),
                source_model.quantity, 
                source_model.id)

    def to_model(self):
        """Converts this DTO to a Source Model ready to persist"""
        from models.source_model import Source

        return Source(
            step_id = self.step_id,
            ingredient_id = self.ingredient.id,
            unit_id = self.unit.id,
            quantity = self.quantity,
            id = self.id)