"""Текстовый отчёт для stdout."""

from collections.abc import Sequence

from quiz_analyzer.stats import QuestionStat


def _line(s: QuestionStat, width: int) -> str:
    return f"{s.question:<{width}}  {s.share:5.1f}%  ({s.correct}/{s.total})"


def render(table: Sequence[QuestionStat], hard: Sequence[QuestionStat], threshold: float) -> str:
    """Таблица «вопрос / доля / счёт» и блок трудных вопросов."""
    width = max((len(s.question) for s in [*table, *hard]), default=0)
    lines = [_line(s, width) for s in table]
    lines += ["", f"Самые трудные вопросы (ниже {threshold:g}%):"]
    lines += [_line(s, width) for s in hard] if hard else ["нет"]
    return "\n".join(lines)
