from models.action_model import Action
from dto.action_dto import ActionDTO


class ActionService:
    def get_by_id(self, id):
        unit = Action.get_one("id", id)
        return ActionDTO.from_model(unit)
    
    def get_all(self):
        units = Action.get_all()
        return [ActionDTO.from_model(unit) for unit in units]
    
    def delete(self, id):
        unit = Action.get_one("id", id)
        if unit.id:
            unit.delete()

    def create(self, unitDTO):
        unit = ActionDTO.to_model(unitDTO, Action)
        return unit.save()

    def update(self, unitDTO):
        unit = ActionDTO.to_model(unitDTO, Action)
        unit.save()

   