from pathlib import Path


class DocumentService:
    def __init__(self, path_to_file: str) -> None:
        self.path = Path(path_to_file)


    def read_document(self) -> list[dict[str, str]]:
        if not self.path.exists():
            return []
        
        files = [f for f in self.path.iterdir() if f.is_file()]
        if not files:
            return []

        return [{"file_name": f.name, "text": f.read_text(encoding="utf-8")} for f in files]
        

    def chunk_document(self, chunk_size: int, chunk_overlap:int, text: str):
        text_splitted = text.split()
        step = chunk_size - chunk_overlap
        if step < 1:
            step = 1
        chunk_document:list[str] = []
        for i in range(0, len(text_splitted), step):
            chunk_text = text_splitted[i:i+chunk_size]
            chunk_document.append(" ".join(chunk_text))
        return chunk_document