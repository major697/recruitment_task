from typing import Sequence

from sentence_transformers import SentenceTransformer

from app.models.model import ModelEnum


class EmbeddingService:
    def __init__(self):
        self.sentence_transformer = SentenceTransformer(ModelEnum.EMBEDDING_MODEL.value)
        

    def embedding_text(self, text: list[str] | str):
        encode_text = self.sentence_transformer.encode(inputs=text)
        return encode_text