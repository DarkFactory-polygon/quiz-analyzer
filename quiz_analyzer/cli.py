"""Разбор аргументов, код выхода, stderr."""

import argparse
import sys

from quiz_analyzer import report
from quiz_analyzer.reader import ValidationError, read_rows
from quiz_analyzer.stats import DEFAULT_THRESHOLD, hardest, per_question


def _percent(value: str) -> float:
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"не число: {value!r}") from None
    if not 0 <= number <= 100:
        raise argparse.ArgumentTypeError(f"порог должен быть в диапазоне 0..100, получено {value}")
    return number


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="quiz-analyzer",
        description="Доля верных ответов по вопросам квиза и самые трудные вопросы.",
    )
    p.add_argument("path", help="CSV: student,question,answer,correct")
    p.add_argument(
        "--threshold",
        type=_percent,
        default=DEFAULT_THRESHOLD,
        help="порог трудных вопросов в процентах, 0..100 (по умолчанию 50)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)  # ошибка аргументов: SystemExit(2), stderr
    try:
        rows = read_rows(args.path)
    except ValidationError as e:
        print(f"Ошибка в строке {e.line_no}: {e.message}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Ошибка: не удалось прочитать файл: {e}", file=sys.stderr)
        return 1
    table = per_question(rows)
    print(report.render(table, hardest(table, args.threshold), args.threshold))
    return 0
