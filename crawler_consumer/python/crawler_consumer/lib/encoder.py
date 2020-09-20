#!/usr/bin/env python3

from lib.models import Article, File, Keyword
from flask.json import JSONEncoder

class ConsumerJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return {
                "id": obj.id,
                "title": obj.title,
                "source_url": obj.source_url,
                "keywords": [ self.default(x) for x in obj.keywords],
                "files": [ self.default(x) for x in obj.files],
                "digital_object_id": obj.digital_object_id,
                "parent_request_url": obj.parent_request_url,
                "description": obj.description,
                "parse_date": obj.parse_date.isoformat() if obj.parse_date is not None else None,
                "upload_date": obj.upload_date.isoformat() if obj.upload_date is not None else None,
                "created_date": obj.created_date.isoformat() if obj.created_date is not None else None,
                "modified_date": obj.modified_date.isoformat() if obj.modified_date is not None else None,
                "parsed": obj.parsed,
                "enriched": obj.enriched,
                "published": obj.published }
        if isinstance(obj, File):
            return {
                "id": obj.id,
                "file_name": obj.file_name,
                "url": obj.url,
                "download_url": obj.download_url,
                "digital_object_id": obj.digital_object_id,
                "size": obj.size
            }
        if isinstance(obj, Keyword):
            return {
                "id": obj.id,
                "word": obj.word,
                "created_date": obj.created_date.isoformat() if obj.created_date is not None else None,
                "modified_date": obj.modified_date.isoformat() if obj.modified_date is not None else None
            }

