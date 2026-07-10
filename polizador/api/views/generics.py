from typing import Any, List, Optional

from ninja import Field, Schema
from ninja.pagination import PaginationBase


class PerPagePagination(PaginationBase):
    """Replicates this API's original `?page=&per_page=` contract
    (`{count, next, previous, results}`) on top of ninja's pagination hook."""

    class Input(Schema):
        page: int = Field(1, ge=1)
        per_page: int = Field(50, ge=1, le=200)

    class Output(Schema):
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None
        results: List[Any]

    items_attribute = "results"

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        per_page = pagination.per_page
        start = (page - 1) * per_page
        end = start + per_page
        total = self._items_count(queryset)
        return {
            "results": queryset[start:end],
            "count": total,
            "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
            "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        }
