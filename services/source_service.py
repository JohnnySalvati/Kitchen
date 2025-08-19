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

    def update_sources(self, step_id, sourcesDTO: list[SourceDTO]):
        """Checks if source need to be deleted, updated, or left as is"""
        sources = Source.get_all("step_id", step_id)
        for source in sources:
            index = self.find_source_index(sourcesDTO, source.id)
            if index >= 0:
                if SourceDTO.to_model(sourcesDTO[index]) != source:
                    self.save(sourcesDTO[index])
            else:
                source.delete()
        for sourceDTO in sourcesDTO:
            index = self.find_source_index(sources, sourceDTO.id)
            if index < 0:
                self.save(sourceDTO)
        
    def find_source_index(self, sources, source_id):
        for index, source in enumerate(sources):
            if source.id == source_id:
                return index
        return -1        