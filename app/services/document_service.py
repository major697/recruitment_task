from pathlib import Path


class DocumentService:
    def __init__(self):
        pass

    @staticmethod
    def read_document(file_path: Path):
        with open(file_path, 'r') as file:
            return file.read()
        return None

    @staticmethod
    def text_splitter(chunk_size: int, chunk_overlap:int, text: str):
        text_splitted = text.split()
        step = chunk_size - chunk_overlap
        if step < 1:
            step = 1
        chunk_document:list[str] = []
        for i in range(0, len(text_splitted), step):
            chunk_text = text_splitted[i:i+chunk_size]
            chunk_document.append(" ".join(chunk_text))
        return chunk_document