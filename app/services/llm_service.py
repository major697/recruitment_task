from openai import OpenAI
from settings import settings
from app.schema.ask_schema import AskResponseSchema, ChunkSimilaritySchema


class LlmService:
    def __init__(self):
        self.openai = OpenAI(
            base_url=settings.ollama_base_url,
            api_key=settings.ollama_api_key,
        )


    def generate_answer(self, query: str, similarity_text: list[ChunkSimilaritySchema]) -> AskResponseSchema:
        document_format = "\n\n".join([f"File name: {document.file_name} | Document text: {document.text}" for document in similarity_text])
        system_prompt = f"""You are a helpful support assistant. Answer the user's query using *only* the provided documents below. Do not use any outside knowledge.

        Rules:
        1. Base your response strictly on the facts presented in the documents.

        Documents:
        {document_format}"""

        response = self.openai.responses.parse(
            model="llama3.2:latest",
            input=[
                {"role": "user", "content": query},
                {"role": "system", "content": system_prompt}
            ],
            text_format=AskResponseSchema
        )
        parsed = response.output_parsed
        return AskResponseSchema(
            answer=parsed.answer if parsed else "No answer",
            document_name=parsed.document_name if parsed else "No document"
        )
