from fastapi import Depends, Request

from app.core.container import AppContainer
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LlmService
from app.services.similarity_text_service import SimilarityTextService


def get_container(request: Request) -> AppContainer:
    return request.app.state.container

def get_embedding_service(container: AppContainer = Depends(get_container)):
    return EmbeddingService(sentence_transformer=container.sentence_transformer)

def get_similarity_text_service(
        container: AppContainer = Depends(get_container),
        embedding_service: EmbeddingService = Depends(get_embedding_service)
    ):
    return SimilarityTextService(
        embedding_service=embedding_service,
        sentence_transformer=container.sentence_transformer
    )

def get_llm_service(container: AppContainer = Depends(get_container)):
    return LlmService(openai=container.openai)