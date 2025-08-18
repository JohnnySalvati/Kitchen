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
        from dto.recipe_dto import RecipeDTO
        from dto.unit_dto import UnitDTO

        return SourceDTO(source_model.step_id,
                        RecipeDTO.from_model(source_model.ingredient),
                        UnitDTO.from_model(source_model.unit),
                        source_model.quantity, 
                        source_model.id)

    def to_model(self):
        """Converts this DTO to a Source Model ready to persist"""
        from models.source_model import Source

        return Source(step_id = self.step_id,
                                ingredient = self.ingredient.to_model(),
                                unit = self.unit.to_model(),
                                quantity = self.quantity,
                                id = self.id)