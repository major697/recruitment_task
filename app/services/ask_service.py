from pathlib import Path

from sentence_transformers import SentenceTransformer
from app.models.model import ModelEnum
from app.schema.ask_schema import ChunkSimilaritySchema
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService


class SimilarityTextService:
    def __init__(self):
        self.document_service = DocumentService()
        self.embedding_service = EmbeddingService()
        self.sentence_transformer = SentenceTransformer(ModelEnum.EMBEDDING_MODEL.value)



    def get_similarity_file_text(self, query: str):
        path_file = Path('app/data')

        if not path_file.exists() or not any(path_file.iterdir()):
            return None

        result_similarity:list[ChunkSimilaritySchema] = []
        similarity_min = 0.5

        embedding_query = self.embedding_service.embedding_text(text=query)

        for file_item in path_file.iterdir():
            if file_item.is_file():
                file_content = self.document_service.read_document(file_item)
                chunks_document = self.document_service.text_splitter(chunk_size=20, chunk_overlap=5, text=file_content)

                if not chunks_document:
                    return None


                for chunk_document in chunks_document:
                    embedding_content = self.embedding_service.embedding_text(text=chunk_document)
                    similarity_embedding = self.sentence_transformer.similarity(embeddings1=embedding_query, embeddings2=embedding_content)[0][0].item()
                    if similarity_embedding >= similarity_min:
                        result_similarity.append(ChunkSimilaritySchema(
                            embedding=similarity_embedding,
                            text=chunk_document,
                            file_name=file_item.name
                        ))
        return result_similarity
            