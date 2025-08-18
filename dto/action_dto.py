class ActionDTO:
    def __init__(self, name=None, id=None):
        self.id = id
        self.name = name

    @classmethod
    def from_model(cls, action_model):
        """Converts a Action model to a DTO"""
        return ActionDTO(action_model.name,
                        action_model.id)

    def to_model(self):
        """Converts this DTO to a Action Model ready to persist"""
        from models.action_model import Action

        return Action(name = self.name,
                                id = self.id)