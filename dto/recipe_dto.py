from dto.unit_dto import UnitDTO
class RecipeDTO:
    def __init__(self, name: str="", price: float=0, result_unit: UnitDTO= UnitDTO(), result_quantity: float=0, sources=[], id=None):
        self.id = id
        self.name = name
        self.price = price
        self.result_unit = result_unit
        self.result_quantity = result_quantity
        self.sources = sources if sources else []

    @classmethod
    def from_model(cls, recipe_model, sources ):
        """Converts a Recipe model to a DTO"""
        from services.source_service import SourceService
        from services.unit_service import UnitService

        source_service = SourceService()
        unit_service = UnitService()
        return RecipeDTO(
                        recipe_model.name,
                        recipe_model.price,
                        unit_service.get_by_id(recipe_model.resultUnit_id),
                        recipe_model.resultQuantity,
                        [source_service.get_by_id(source.id) for source in sources],
                        recipe_model.id)

    def to_model(self):
        """Converts this DTO to a Recipe Model ready to persist"""
        from models.recipe_model import Recipe
        
        return Recipe(
                    name = self.name,
                    price = self.price,
                    resultUnit_id = self.result_unit.id if self.result_unit.id else 0,
                    resultQuantity= self.result_quantity,
                    id = self.id)
        
    def __eq__(self, value) -> bool:
        from services.source_service import SourceService

        source_service = SourceService()        
        if (self.name == value.name and
            self.price == value.price and
            self.result_unit.id == value.result_unit.id and
            self.result_quantity == value.result_quantity and
            source_service.are_equals(self.sources, value.sources)):
            return True
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((
            self.name,
            self.price,
            self.result_unit.id,
            self.result_quantity,
            self.sources
        ))