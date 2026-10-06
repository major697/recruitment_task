from fastapi import Depends, Request

from app.core.container import AppContainer
from app.services.llm_service import LlmService
from app.services.similarity_text_service import SimilarityTextService


def get_container(request: Request) -> AppContainer:
    return request.app.state.container

def get_similarity_text_service(container: AppContainer = Depends(get_container)) -> SimilarityTextService:
    return container.similarity_text_service

def get_llm_service(container: AppContainer = Depends(get_container)) -> LlmService:
    return container.llm_service