class SourceDTO():
    def __init__(self,
                recipe_id=None,
                ingredient=None,
                unit=None,
                quantity=0,
                id=None):
        from dto.recipe_dto import RecipeDTO
        from dto.unit_dto import UnitDTO

        self.id = id
        self.recipe_id = recipe_id
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
        try:
            return SourceDTO(
                    source_model.recipe_id,
                    recipe_service.get_by_id(source_model.ingredient_id),
                    unit_service.get_by_id(source_model.unit_id),
                    source_model.quantity, 
                    source_model.id)
        except RecursionError as e:
            raise RecursionError(f"Se produjo una recursion infinita: {e}")

    def to_model(self):
        """Converts this DTO to a Source Model ready to persist"""
        from models.source_model import Source

        return Source(
            recipe_id = self.recipe_id,
            ingredient_id = self.ingredient.id,
            unit_id = self.unit.id,
            quantity = self.quantity,
            id = self.id)
    
    def __eq__(self, value) -> bool:
        if (self.recipe_id == value.recipe_id and 
            self.ingredient.id == value.ingredient.id and
            self.unit.id == value.unit.id and
            self.quantity == value.quantity):
            return True
        return False
    
    def __hash__(self) -> int:
        return hash((
            self.recipe_id,
            self.ingredient.id,
            self.unit.id,
            self.quantity
        ))