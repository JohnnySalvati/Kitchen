from models.source_model import Source
from dto.source_dto import SourceDTO

class SourceService:
    def get_by_id(self, id):
        source = Source.get_one("id", id)
        if not source.id:
            raise ValueError(f"No exite ingrediente original con ID {id}")
        return SourceDTO.from_model(source)
    
    def get_all(self, step_id):
        sources = Source.get_all("step_id", step_id)
        return [SourceDTO.from_model(source) for source in sources]
    
    def delete(self, id):
        source = Source.get_one("id", id)
        if source.id:
            source.delete()
        else:
            raise ValueError(f"No exite ingrediente original con ID {id}")

    def save(self, sourceDTO):
        source = SourceDTO.to_model(sourceDTO)
        return source.save()
