class Protien:
    def __init__(self, file_list=None):
        self.file_list = file_list

    def add_file(self, file: str) -> None:
        if file not in self.file_list:
            self.file_list.append(file)


class StudyParameters:
    def __init__(self, title=None, description=None, protien_list=None,
                 author_list=None, keywords=None, categories=None):
        self.description = description
        self.protein_list = protien_list
        self.author_list = author_list
        self.keywords = keywords
        self.categories = categories
        self.title = title

    def add_title(self, title: str) -> None:
        self.title = title

    def add_description(self, description: str) -> None:
        self.description = description

    def add_protien(self, protien: Protien) -> None:
        if protien not in self.protein_list:
            self.protein_list.append(protien)

    def add_authors(self, author: str) -> None:
        if author not in self.author_list:
            self.author_list.append(author)

    def add_keyword(self, keyword: str) -> None:
        if keyword not in self.keywords:
            self.keywords.append(keyword)

    def add_category(self, category: str) -> None:
        if category not in self.categories:
            self.categories.append(category)
