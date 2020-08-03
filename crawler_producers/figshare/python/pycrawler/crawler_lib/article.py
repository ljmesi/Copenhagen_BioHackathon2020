class File(object):
    def __init__(self,
                 file_name=None,
                 url=None,
                 digital_object_id=""):
        self._file_name = file_name
        self._url = url
        self._digital_object_id = digital_object_id

    @property
    def file_name(self):
        return self._file_name

    @property
    def url(self):
        return self._url

    @property
    def digital_object_id(self):
        return self._digital_object_id

    def __str__(self):
        return str(self.__dict__)


class Article:
    def __init__(self,
                 title=None,
                 source_url=None,
                 keywords=[],
                 digital_object_id="",
                 description="",
                 parse_date=None,
                 files=[],
                 authors=[],
                 parent_request_url=""):

        self._title = title
        self._source_url = source_url
        self._keywords = keywords
        self._digital_object_id = digital_object_id
        self._description = description
        self._parse_date = parse_date
        self._files = files
        self._authors = authors
        self._parent_request_url = parent_request_url

    @property
    def title(self):
        return self._title

    @property
    def source_url(self):
        return self._source_url

    @property
    def digital_object_id(self):
        return self._digital_object_id

    @property
    def description(self):
        return self._description

    @property
    def parent_request_url(self):
        return self._parent_request_url

    def add_author(self, author: str) -> None:
        if author and author not in self._authors:
            self._authors.append(author)

    def add_keyword(self, keyword: str) -> None:
        if keyword and keyword not in self._keywords:
            self._keywords.append(keyword)

    def add_file(self, file: File) -> None:
        if file and file not in self._files:
            self._files.append(file)

    def add_upload_date(self, upload_date: str) -> None:
        ##TODO: parse date in proper format
        if upload_date:
            self.upload_date = upload_date

    @source_url.setter
    def source_url(self, value):
        self._source_url = value

    def __str__(self):
        return str(self.__dict__)
