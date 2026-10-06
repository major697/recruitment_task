from openai import OpenAI

from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.similarity_text_service import SimilarityTextService


class AppContainer():
    def __init__(self, embedding_service: EmbeddingService, openai: OpenAI, document_service: DocumentService, similarity_text_service: SimilarityTextService):
        self.openai = openai
        self.embedding_service = embedding_service
        self.document_service = document_service
        self.similarity_text_service = similarity_text_service