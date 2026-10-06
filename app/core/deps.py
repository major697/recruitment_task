from fastapi import Depends, Request

from app.core.container import AppContainer
from app.services.llm_service import LlmService


def get_container(request: Request) -> AppContainer:
    return request.app.state.container

def get_similarity_text_service(
        container: AppContainer = Depends(get_container),
    ):
    return container.similarity_text_service

def get_llm_service(container: AppContainer = Depends(get_container)):
    return LlmService(openai=container.openai)