class UnitConverterDTO:
    def __init__(self, source_unit=None, quantity=float(0), target_unit=None, id=None):
        from dto.unit_dto import UnitDTO

        self.id = id
        self.source_unit = source_unit if source_unit else UnitDTO()
        self.quantity = quantity
        self.target_unit = target_unit if target_unit else UnitDTO()

    @classmethod
    def from_model(cls, unit_converter_model):
        """Converts a Unit model to a DTO"""
        from services.unit_service import UnitService

        unit_service = UnitService()
        return UnitConverterDTO(unit_service.get_by_id(unit_converter_model.source_unit_id),
                                unit_converter_model.quantity,
                                unit_service.get_by_id(unit_converter_model.target_unit_id),
                                unit_converter_model.id)

    def to_model(self):
        """Converts this DTO to a Unit Model ready to persist"""
        from models.unit_converter_model import UnitConverter

        return UnitConverter(source_unit_id = self.source_unit.id,
                            quantity = self.quantity,
                            target_unit_id = self.target_unit.id,
                            id = self.id)