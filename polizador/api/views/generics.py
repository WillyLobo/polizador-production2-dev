from django.db.models import Model, QuerySet
from typing import TypeVar, Generic, Type, List, Optional, Any
from ninja import Schema


T = TypeVar("T", bound=Model)


class PaginatedResponse(Schema):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[dict[str, Any]]
