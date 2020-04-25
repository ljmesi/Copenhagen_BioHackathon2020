class Protien:
    def __init__(self, file_list=None):
        self.file_list = file_list

    def add_file(self, file: str) -> None:
        pass


class StudyParameters:
    def __init__(self, description=None, protien_list=None, author_list=None, keywords=None):
        self.description = description
        self.protein_list = protien_list
        self.author_list = author_list
        self.keywords = keywords

    def add_description(self, description: str) -> None:
        pass

    def add_protien(self, protien: Protien) -> None:
        pass

    def add_authors(self, author: str) -> None:
        pass

    def add_keyword(self, keyword: str) -> None:
        pass
