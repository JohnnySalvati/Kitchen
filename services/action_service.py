from models.action_model import Action
from dto.action_dto import ActionDTO


class ActionService:
    def get_by_id(self, id):
        action = Action.get_one("id", id)
        if not action.id:
            raise ValueError(f"No exite accion con ID {id}")
        return ActionDTO.from_model(action)
    
    def get_all(self):
        actions = Action.get_all()
        return [ActionDTO.from_model(action) for action in actions]
    
    def delete(self, id):
        action = Action.get_one("id", id)
        if action.id:
            action.delete()
        else:
            raise ValueError(f"No existe accion con ID {id}")

    def save(self, actionDTO):
        if actionDTO.id is None and Action.get_one("name", actionDTO.name).id is not None:
            raise ValueError("Ya existe una accion con ese nombre")
        action = ActionDTO.to_model(actionDTO, Action)
        return action.save()

   