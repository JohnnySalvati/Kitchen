from models.unit_model import Unit
from dto.unit_dto import UnitDTO

class UnitService:
    def get_by_id(self, id):
        unit = Unit.get_one("id", id)
        return UnitDTO.from_model(unit)
    
    def get_all(self):
        units = Unit.get_all()
        return [UnitDTO.from_model(unit) for unit in units]
    
    def delete(self, id):
        unit = Unit.get_one("id", id)
        if unit.id:
            unit.delete()

    def create(self, unitDTO):
        unit = UnitDTO.to_model(unitDTO, Unit)
        return unit.save()

    def update(self, unitDTO):
        unit = UnitDTO.to_model(unitDTO, Unit)
        unit.save()

   