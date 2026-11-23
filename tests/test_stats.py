from quiz_analyzer.reader import Row
from quiz_analyzer.stats import QuestionStat, hardest, per_question


def _rows(question: str, correct: int, total: int) -> list[Row]:
    return [Row(f"s{i}", question, "a", i < correct) for i in range(total)]


def _table(*shares: float) -> list[QuestionStat]:
    return [QuestionStat(f"Q{i}", 0, 0, s) for i, s in enumerate(shares, 1)]


def test_per_question_computes_share():
    (stat,) = per_question(_rows("Q1", 8, 10))
    assert (stat.question, stat.correct, stat.total, stat.share) == ("Q1", 8, 10, 80.0)


def test_per_question_keeps_first_appearance_order():
    rows = [Row("a", q, "x", True) for q in ("Q3", "Q1", "Q2", "Q1", "Q3", "Q2")]
    assert [s.question for s in per_question(rows)] == ["Q3", "Q1", "Q2"]


def test_hardest_sorts_worst_first():
    result = hardest(_table(80, 30, 45), 50)
    assert [s.question for s in result] == ["Q2", "Q3"]


def test_hardest_excludes_value_equal_to_threshold():
    assert hardest(_table(50.0)) == []


def test_hardest_with_threshold_40():
    assert [s.question for s in hardest(_table(80, 30, 45), 40)] == ["Q2"]


def test_per_question_empty():
    assert per_question([]) == []
