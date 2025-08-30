from models.step_model import Step
from dto.step_dto import StepDTO
class StepService:
    def get_by_id(self, id):
        from services.source_service import SourceService

        source_service = SourceService()
        step = Step.get_one("id", id)
        sources = source_service.get_all(id)
        return StepDTO.from_model(step, sources)
    
    def get_all(self, recipe_id):
        from services.source_service import SourceService

        source_service = SourceService()
        stepsDTO = []
        steps = Step.get_all("recipe_id", recipe_id) 
        for step in steps:
            sources = source_service.get_all(step.id)
            stepsDTO.append(StepDTO.from_model(step, sources))
        return stepsDTO
        
    def delete(self, id):
        step = Step.get_one("id", id)
        if step.id:
            step.delete()

    def save(self, stepDTO):
        from services.source_service import SourceService

        source_service = SourceService()
        step = StepDTO.to_model(stepDTO)
        step.save()
        source_service.update_sources(step.id, stepDTO.sources)
        return 

    def update_steps(self, recipe_id,  stepsDTO: list[StepDTO]):
        """Checks if step need to be deleted, updated, or left as is"""
        steps = Step.get_all("recipe_id", recipe_id) 
        for step in steps:
            index = self.find_step_index(stepsDTO, step.id)
            if index >= 0:
                if StepDTO.to_model(stepsDTO[index]) != step:
                    self.save(stepsDTO[index])
            else:
                step.delete()
        for stepDTO in stepsDTO:
            index = self.find_step_index(steps, stepDTO.id)
            if index < 0:
                self.save(stepDTO)
   
    def find_step_index(self, steps, step_id):
        for index, step in enumerate(steps):
            if step.id == step_id:
                return index
        return -1


