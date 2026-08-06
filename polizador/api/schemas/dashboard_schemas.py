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
    unresolved_count: Optional[int] = None
    top_issues: List[SentryIssueSchema] = []
