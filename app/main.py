from typing import Annotated

from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException

from app.schema.ask_schema import AskRequestSchema, AskResponseSchema
from app.services.ask_service import SimilarityTextService
from app.services.llm_service import LlmService

load_dotenv()

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", description="Ask LLM")
async def ask_question(payload: Annotated[
        AskRequestSchema,
        Body(
            examples=[
                {
                    "query": "How can I return a purchased product?"
                }
            ],
        ),
    ]) -> AskResponseSchema:

    similarity_text_service = SimilarityTextService()
    llm_service = LlmService()

    if not payload.query:
        raise HTTPException(status_code=404, detail="Query is required.")

    similarity_text = similarity_text_service.get_similarity_file_text(query=payload.query)

    if similarity_text is None:
        raise HTTPException(status_code=404, detail="No documents information.")

    generated_answer = llm_service.generate_answer(query=payload.query, similarity_text=similarity_text)
    return AskResponseSchema(answer=generated_answer.answer, document_name=generated_answer.document_name)