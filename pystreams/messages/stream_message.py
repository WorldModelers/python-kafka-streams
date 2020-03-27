from typing import List
from faust import Record

class StreamMessage(Record):
    id: str
    breadcrumbs: List[str]
