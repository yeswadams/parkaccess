from datetime import datetime
from typing import Any, Dict, List


class BaseSchema:
    fields: List[str] = []
    datetime_fields: List[str] = []

    @classmethod
    def dump(cls, obj: Any) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for field in cls.fields:
            value = getattr(obj, field, None)
            if field in cls.datetime_fields and isinstance(value, datetime):
                result[field] = value.isoformat()
            else:
                result[field] = value
        return result

    @classmethod
    def load(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for field in cls.fields:
            if field not in data:
                continue
            value = data[field]
            if field in cls.datetime_fields and isinstance(value, str):
                result[field] = datetime.fromisoformat(value)
            else:
                result[field] = value
        return result
