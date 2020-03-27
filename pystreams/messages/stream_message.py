from typing import List
from faust import Record


# create a basic record
class StreamMessage(Record):
    id: str
    breadcrumbs: List[str]
