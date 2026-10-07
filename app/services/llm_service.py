from openai import OpenAI

from app.models.model import ModelEnum
from app.schema.ask_schema import AskResponseSchema
from app.schema.similarity_schema import SimilarityTextSchema


class LlmService:
    def __init__(self, openai: OpenAI) -> None:
        self.openai = openai

    def generate_answer(self, query: str, similarity_text: list[SimilarityTextSchema]) -> AskResponseSchema:
        document_format = "\n\n".join([f"File name: {document.file_name or "Unknown file name"} | Document text: {document.text or "File content unknown"}" for document in similarity_text])
        system_prompt = f"""You are a helpful support assistant. Answer the user's query using *only* the provided documents below. Do not use any outside knowledge.

        Rules:
        1. Base your response strictly on the facts presented in the documents.
        2. If documents list are empty, answer: "I don't have documents, so I can't answer you."

        Documents:
        {document_format}"""

        response = self.openai.responses.parse(
            model=ModelEnum.LLAMA_MODEL.value,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            text_format=AskResponseSchema
        )
        parsed = response.output_parsed
        return AskResponseSchema(
            answer=parsed.answer if parsed else "No answer",
            document_name=parsed.document_name if parsed else "No document"
        )
