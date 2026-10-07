import faiss
import numpy as np

from app.schema.similarity_schema import SimilarityTextSchema
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService


class SimilarityTextService:
    def __init__(
            self,
            embedding_service: EmbeddingService,
            document_service: DocumentService
        ):
        self.embedding_service = embedding_service
        self.document_service = document_service
        self.index: faiss.IndexFlatL2 | None = None
        self.documents: list[tuple[str, str]] = []


    def build_index(self) -> None:
        self.documents = []
        documents = self.document_service.read_document()
        if not documents:
            return None

        documents_embeddings:list[np.ndarray] = []
        for d in documents:
            document_chunk = self.document_service.chunk_document(chunk_size=50, chunk_overlap=10, text=d["text"])
            documents_embedding = self.embedding_service.embedding_text(text=document_chunk)
            documents_embeddings.append(documents_embedding)
            self.documents.extend((d["file_name"], c) for c in document_chunk)

        matrix = np.vstack(documents_embeddings)
        index = faiss.IndexFlatL2(matrix.shape[-1])
        index.add(matrix)
        self.index = index


    def get_similarity_file_text(self, query: str, top_k: int = 3) -> list[SimilarityTextSchema] | None:
        if self.index is None:
            return None

        embedding_query = self.embedding_service.embedding_text(text=[query])
        _, position = self.index.search(embedding_query, min(top_k, self.index.ntotal))

        result_similarity: list[SimilarityTextSchema] = []
        for p in position[0]:
            file_name, text = self.documents[int(p)]
            result_similarity.append(SimilarityTextSchema(file_name=file_name, text=text))

        return result_similarity