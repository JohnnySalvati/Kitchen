from models.unit_model import Unit
from dto.unit_dto import UnitDTO

class UnitService:
    def get_by_id(self, id):
        if id:
            unit = Unit.get_one("id", id)
            return UnitDTO.from_model(unit)
        else:
            return UnitDTO()
    
    def get_all(self):
        units = Unit.get_all()
        return [UnitDTO.from_model(unit) for unit in units]
    
    def delete(self, id):
        unit = Unit.get_one("id", id)
        if unit.id:
            unit.delete()

    def save(self, unitDTO):
        unit = UnitDTO.to_model(unitDTO)
        return unit.save()

   