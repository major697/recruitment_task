from pathlib import Path


class DocumentService:
    def __init__(self, path_to_file: str) -> None:
        self.path = Path(path_to_file)


    def read_document(self) -> str | None:
        if not self.path.exists() or not any(self.path.iterdir()):
            return None
        with open(self.path, 'r') as file:
            return file.read()

    def text_splitter(self, chunk_size: int, chunk_overlap:int, text: str):
        text_splitted = text.split()
        step = chunk_size - chunk_overlap
        if step < 1:
            step = 1
        chunk_document:list[str] = []
        for i in range(0, len(text_splitted), step):
            chunk_text = text_splitted[i:i+chunk_size]
            chunk_document.append(" ".join(chunk_text))
        return chunk_document