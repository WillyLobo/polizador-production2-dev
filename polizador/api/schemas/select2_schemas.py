from ninja import Schema
from typing import List


class Select2ItemSchema(Schema):
    id: int
    text: str

# Overall response wrapper format
class Select2ResponseSchema(Schema):
    results: List[Select2ItemSchema]
    pagination: dict = {"more": False}  # Optional, set to True for pagination