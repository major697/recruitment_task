from openai import OpenAI
from sentence_transformers import SentenceTransformer


class AppContainer():
    def __init__(self, sentence_transformer: SentenceTransformer, openai: OpenAI):
        self.sentence_transformer = sentence_transformer
        self.openai = openai