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
        """
        saves a unit_converter.
        :raises DuplicateUnitConverterError: if exist conversion
        :return: saved UnitConverterDTO
        """
        unit_convertersDTO_db = self.get_all(unit_converterDTO.source_unit.id)
        for unit_converterDTO_db in unit_convertersDTO_db:
            if unit_converterDTO_db == unit_converterDTO: # if exists in database
                if not unit_converterDTO.target_unit.id: # Trying to save as new an existing unit_converter
                    raise DuplicateUnitConverterError(unit_converterDTO)
                else:
                    break  # it's ok it's an update
        unit_converter = UnitConverterDTO.to_model(unit_converterDTO)
        return UnitConverterDTO.from_model(unit_converter.save()) 
    
    def match(self, source_unit_id, target_unit_id):
        unit_converters = self.get_all(source_unit_id)
        for unit_converter in unit_converters:
            if unit_converter.target_unit.id == target_unit_id:
                return unit_converter
        unit_converters = self.get_all(target_unit_id)
        for unit_converter in unit_converters:
            if unit_converter.target_unit.id == source_unit_id:
                return unit_converter
        return None
    
    def convert(self, quantity, source_unit_id, target_unit_id):
        from services.unit_service import UnitService

        unit_service = UnitService()
        unit_converter = self.match(source_unit_id, target_unit_id)
        if unit_converter:
            if unit_converter.source_unit.id == source_unit_id:
                return quantity * unit_converter.quantity
            else:
                return quantity / unit_converter.quantity
        else:
            source_unit = unit_service.get_by_id(source_unit_id)
            target_unit = unit_service.get_by_id(target_unit_id)
            raise ConversionNotFoundError(f"No existe una conversion que relacione {source_unit.name} con {target_unit.name}")
        return quantity
class DuplicateUnitConverterError(Exception):
    """Se intenta crear un unit_converter duplicado"""
    pass

class ConversionNotFoundError(Exception):
    pass