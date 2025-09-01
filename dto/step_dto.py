class StepDTO:
    def __init__(self,
                    recipe_id=None,
                    sources= None,
                    action=None,
                    resultIngredient=None,
                    resultUnit=None,
                    resultQuantity=float(0),
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
    def from_model(cls, step_model, sources=[]):
        """Converts a Step model to a DTO"""
        from services.source_service import SourceService
        from services.action_service import ActionService
        from services.recipe_service import RecipeService
        from services.unit_service import UnitService
        
        source_service = SourceService()
        action_service = ActionService()
        recipe_service = RecipeService()
        unit_service = UnitService()
        return StepDTO( 
                step_model.recipe_id,
                [source_service.get_by_id(source.id) for source in sources],
                action_service.get_by_id(step_model.action_id),
                recipe_service.get_ingredient(step_model.resultIngredient_id),
                unit_service.get_by_id(step_model.resultUnit_id),
                step_model.resultQuantity,
                step_model.id)

    def to_model(self):
        """Converts this DTO to a Step Model ready to persist"""
        from models.step_model import Step

        return Step(
            recipe_id = self.recipe_id,
            action_id = self.action.id,
            resultIngredient_id = self.resultIngredient.id,
            resultUnit_id = self.resultUnit.id,
            resultQuantity = self.resultQuantity,
            id = self.id)
