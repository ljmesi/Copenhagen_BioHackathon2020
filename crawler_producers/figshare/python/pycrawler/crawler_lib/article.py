import json


class File(object):
    def __init__(self,
                 file_name=None,
                 url=None,
                 download_url=None,
                 digital_object_id=""):
        self._file_name = file_name
        self._url = url
        self._download_url = download_url
        self._digital_object_id = digital_object_id

    @property
    def file_name(self):
        return self._file_name

    @property
    def url(self):
        return self._url

    @property
    def download_url(self):
        return self._download_url

    @property
    def digital_object_id(self):
        return self._digital_object_id

    @url.setter
    def url(self, value):
        self._url = value

    def __str__(self):
        return str(self.__dict__)

    def to_json(self):
        return json.dumps({"file_name": self.file_name, "url": self.url,
                           "download_url": self.download_url,
                           "digital_object_id": self.digital_object_id})



class Article:
    def __init__(self,
                 title=None,
                 source_url=None,
                 keywords=[],
                 digital_object_id="",
                 description="",
                 parse_date=None,
                 upload_date=None,
                 files=[],
                 authors=[],
                 parent_request_url="",
                 enriched=False,
                 published=False):

        self._title = title
        self._source_url = source_url
        self._keywords = keywords
        self._digital_object_id = digital_object_id
        self._description = description
        self._parse_date = parse_date
        self._upload_date = upload_date
        self._files = files
        self._authors = authors
        self._parent_request_url = parent_request_url
        self._enriched = enriched
        self._published = published

    @property
    def title(self):
        return self._title

    @property
    def source_url(self):
        return self._source_url

    @property
    def parse_date(self):
        return self._parse_date

    @property
    def upload_date(self):
        return self._upload_date

    @property
    def digital_object_id(self):
        return self._digital_object_id

    @property
    def description(self):
        return self._description

    @property
    def parent_request_url(self):
        return self._parent_request_url

    @property
    def authors(self):
        return self._authors

    def add_author(self, author: str) -> None:
        if author and author not in self._authors:
            self._authors.append(author)

    def add_keyword(self, keyword: str) -> None:
        if keyword and keyword not in self._keywords:
            self._keywords.append(keyword)

    def add_file(self, file: File) -> None:
        if file and file not in self._files:
            self._files.append(file)

    @source_url.setter
    def source_url(self, value):
        self._source_url = value

    @parent_request_url.setter
    def parent_request_url(self, value):
        self._parent_request_url = value

    def __str__(self):
        return str(self.__dict__)

    def to_json(self):
        return json.dumps({
            "title": self.title,
            "source_url": self.source_url,
            "keywords": self._keywords,
            "digital_object_id": self.digital_object_id,
            "description": self.description,
            "parse_date": self.parse_date,
            "upload_date": self.upload_date,
            "files": [json.loads(x.to_json()) for x in self._files],
            "authors": self.authors,
            "parent_request_url": self.parent_request_url,
            "enriched": self._enriched,
            "published": self._enriched
        })
