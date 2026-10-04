from pydantic import BaseModel

class SimilarityTextSchema(BaseModel):
    file_name: str
    text: str