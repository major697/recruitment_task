import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, sentence_transformer: SentenceTransformer) -> None:
        self.sentence_transformer = sentence_transformer

    def embedding_text(self, text: list[str]) -> np.ndarray:
        return self.sentence_transformer.encode(inputs=text, normalize_embeddings=True).astype(np.float32)