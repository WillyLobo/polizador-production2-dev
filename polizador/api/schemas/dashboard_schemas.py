from typing import List, Optional

from ninja import Schema


class SeriesPointSchema(Schema):
    period: str
    total: int


class ThroughputResponseSchema(Schema):
    series: dict[str, List[SeriesPointSchema]]


class SentryIssueSchema(Schema):
    title: str
    count: str
    url: str


class SentryHealthResponseSchema(Schema):
    configured: bool
    # True cuando Sentry está configurado pero la consulta falló.
    error: bool = False
    unresolved_count: Optional[int] = None
    # True cuando hay más issues que los contados (unresolved_count es un piso).
    truncated: bool = False
    top_issues: List[SentryIssueSchema] = []
