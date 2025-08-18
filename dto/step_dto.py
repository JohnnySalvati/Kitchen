class StepDTO:
    def __init__(self,
                    recipe_id=None,
                    sources= None,
                    action=None,
                    resultIngredient=None,
                    resultUnit=None,
                    resultQuantity=None,
                    id=None):
        from dto.action_dto import ActionDTO
        from dto.recipe_dto import RecipeDTO
        from dto.unit_dto import UnitDTO

        self.id = id
        self.recipe_id = recipe_id
        self.sources = sources if sources else []
        self.action = action if action else ActionDTO()
        self.resultIngredient = resultIngredient if resultIngredient else RecipeDTO()
        self.resultUnit = resultUnit if resultUnit else UnitDTO()
        self.resultQuantity = resultQuantity

    @classmethod
    def from_model(cls, step_model):
        """Converts a Step model to a DTO"""
        from dto.source_dto import SourceDTO
        from dto.recipe_dto import RecipeDTO
        from dto.unit_dto import UnitDTO
        from dto.action_dto import ActionDTO

        return StepDTO(step_model.recipe_id,
                        [SourceDTO.from_model(source) for source in step_model.sources],
                        ActionDTO.from_model(step_model.action),
                        RecipeDTO.from_model(step_model.resultIngredient),
                        UnitDTO.from_model(step_model.resultUnit),
                        step_model.resultQuantity,
                        step_model.id)

    def to_model(self):
        """Converts this DTO to a Step Model ready to persist"""
        from models.step_model import Step

        return Step(
            recipe_id = self.recipe_id,
            sources = [source.to_model() for source in self.sources],
            action = self.action.to_model(),
            resultIngredient = self.resultIngredient.to_model(),
            resultUnit = self.resultUnit.to_model(),
            resultQuantity = self.resultQuantity,
            id = self.id)