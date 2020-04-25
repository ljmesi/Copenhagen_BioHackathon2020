class Protien:
    def __init__(self, file_list=[]):
        self.file_list = file_list

    def add_file(self, file: str) -> None:
        if file and file not in self.file_list:
            self.file_list.append(file)


class StudyParameters:
    def __init__(self, source_url=None, title=None, description=None,
                 protien_list=[], author_list=[], keywords=[], categories=[]):
        self.description = description
        self.protein_list = protien_list
        self.author_list = author_list
        self.keywords = keywords
        self.categories = categories
        self.title = title
        self.source_url = source_url

    def add_source_url(self, url:str) -> None:
        if url:
            self.source_url = url

    def add_title(self, title: str) -> None:
        if title:
            self.title = title

    def add_description(self, description: str) -> None:
        if description:
            self.description = description

    def add_protien(self, protien: Protien) -> None:
        if protien and protien not in self.protein_list:
            self.protein_list.append(protien)

    def add_authors(self, author: str) -> None:
        if author and author not in self.author_list:
            self.author_list.append(author)

    def add_keyword(self, keyword: str) -> None:
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)

    def add_category(self, category: str) -> None:
        if category and category not in self.categories:
            self.categories.append(category)

    def __str__(self):
        return str(self.__dict__)