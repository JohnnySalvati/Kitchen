from models.unit_converter_model import UnitConverter
from dto.unit_converter_dto import UnitConverterDTO

class UnitConverterService:
    def get_by_id(self, id):
        unit_converter = UnitConverter.get_one("id", id)
        return UnitConverterDTO.from_model(unit_converter)
    
    def get_all(self, source_unit_id):
        unit_converters = UnitConverter.get_all("source_unit_id", source_unit_id) 
        return [UnitConverterDTO.from_model(unit_converter) for unit_converter in unit_converters]
        
    def delete(self, id):
        unit_converter = UnitConverter.get_one("id", id)
        if unit_converter.id:
            unit_converter.delete()

    def save(self, unit_converterDTO):
        # Checks if exist unit converter
        unit_converters = self.get_all(unit_converterDTO.source_unit.id)
        for unit_converter in unit_converters:
            if unit_converter.target_unit.id == unit_converterDTO.target_unit.id:
                raise DuplicateUnitConverterError(f"Ya existe una unidad de conversion {unit_converterDTO.source_unit.name} = {unit_converterDTO.target_unit.name} ")
        unit_converter = UnitConverterDTO.to_model(unit_converterDTO)
        unit_converter.save()
        return 

class DuplicateUnitConverterError(Exception):
    """Se intenta crear un unit_converter duplicado"""
    pass