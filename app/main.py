from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from app.core.container import AppContainer
from app.core.deps import get_llm_service, get_similarity_text_service
from app.models.model import ModelEnum
from app.schema.ask_schema import AskRequestSchema, AskResponseSchema
from app.services.similarity_text_service import SimilarityTextService
from app.services.llm_service import LlmService
from app.settings import settings


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sentence_transformer = SentenceTransformer(ModelEnum.EMBEDDING_MODEL.value)
    openai = OpenAI(base_url=settings.ollama_base_url, api_key=settings.ollama_api_key)
    app.state.container = AppContainer(sentence_transformer=sentence_transformer, openai=openai)
    yield
    app.state.container.openai.close()

app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", description="Ask LLM")
async def ask_question(payload: Annotated[
        AskRequestSchema,
        Body(examples=[{"query": "How can I return a purchased product?"}]),
    ],
    similarity_text_service: SimilarityTextService = Depends(get_similarity_text_service),
    llm_service: LlmService = Depends(get_llm_service)):


    if not payload.query:
        raise HTTPException(status_code=404, detail="Query is required.")

    similarity_text = similarity_text_service.get_similarity_file_text(query=payload.query)

    if similarity_text is None:
        raise HTTPException(status_code=404, detail="No documents information.")

    generated_answer = llm_service.generate_answer(query=payload.query, similarity_text=similarity_text)
    return AskResponseSchema(answer=generated_answer.answer, document_name=generated_answer.document_name)