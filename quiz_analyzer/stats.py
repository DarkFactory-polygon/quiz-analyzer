"""Агрегация по вопросам и отбор трудных."""

from collections.abc import Iterable
from dataclasses import dataclass

from quiz_analyzer.reader import Row

DEFAULT_THRESHOLD = 50.0


@dataclass(frozen=True)
class QuestionStat:
    question: str
    correct: int
    total: int
    share: float  # 100 * correct / total


def per_question(rows: Iterable[Row]) -> list[QuestionStat]:
    """Доля верных по вопросам, в порядке первого появления в CSV."""
    counts: dict[str, list[int]] = {}
    for row in rows:
        c = counts.setdefault(row.question, [0, 0])
        c[0] += row.correct
        c[1] += 1
    return [QuestionStat(q, c, t, 100 * c / t) for q, (c, t) in counts.items()]


def hardest(
    table: Iterable[QuestionStat], threshold: float = DEFAULT_THRESHOLD
) -> list[QuestionStat]:
    """Вопросы с долей строго ниже порога, от худшего (sorted стабилен)."""
    return sorted((s for s in table if s.share < threshold), key=lambda s: s.share)
