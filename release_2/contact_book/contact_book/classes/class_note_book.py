from pickle import dump, load
import os
from collections import UserDict


class NoteBook(UserDict):

    __instance = None

    def __new__(cls):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, file_path=os.path.join("saved_files", "node_book")):
        super().__init__()
        self.file_path = f"{file_path}.bin"

    def iterator(self, number: str):
        number_int = int(number)
        page, cnt = [], 0
        for record in self.data.values():
            page.append(record)
            cnt += 1

            if cnt == number_int:
                yield page
                page, cnt = [], 0
        if page:
            yield page
    def save_to_file(self) -> str:
        with open(self.file_path, "wb") as file:
            dump(self.data, file)
        return f"Successfully save NoteBook to file {self.file_path}"

    def load_from_file(self) -> str:
        with open(self.file_path, "rb") as file:
            self.data = load(file)
        return f"Successfully load NoteBook from file {self.file_path}"


class Note:

    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        #self._tags = None
        self.tags = tags
        self.text = text

    # @property
    # def tags(self):
    #     return self._tags
    #
    # @tags.setter
    # def tags(self, value):
    #     if len(value) < 1:
    #         self._tags = []
    #     else:
    #         self._tags = [*value]

    def add_content(self, info):
        for piece in info:  # Ищем теги в тексте, именно так они добавляются изначально
            if piece.startswith("#"):
                self._tags.append(piece)

        self.text += info + " "
        return f"Text successfully added to Note '{self.name}'"

    def clear_text(self):
        self.text = ""

    def clear_tags(self):
        self._tags = []


