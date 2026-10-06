import faiss

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


    def get_similarity_file_text(self, query: str):
        embedding_query = self.embedding_service.embedding_text(text=[query])
        result_similarity: list[SimilarityTextSchema] = []

        for file_item in path_file.iterdir():
            if file_item.is_file():
                file_content = self.document_service.read_document()
                chunks_document = self.document_service.text_splitter(chunk_size=20, chunk_overlap=5, text=file_content)

                if not chunks_document:
                    return None

                embedding_text = self.embedding_service.embedding_text(text=chunks_document)

                index = faiss.IndexFlatL2(embedding_text.shape[-1])
                index.add(embedding_text)
                result_index = index.search(embedding_query, min(10, index.ntotal))

                vector, position = result_index
                result_similarity.append(
                    SimilarityTextSchema(
                        file_name=file_item.name,
                        text="\n".join([chunks_document[int(p)] for p in position[0]]) or ""
                    )
                )
        return result_similarity
            