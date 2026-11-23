"""Чтение и валидация CSV с результатами квиза."""

import csv
from dataclasses import dataclass
from pathlib import Path

FIELDS = ("student", "question", "answer", "correct")


@dataclass(frozen=True)
class Row:
    student: str
    question: str
    answer: str
    correct: bool


class ValidationError(Exception):
    """Ошибка в данных; line_no — номер строки файла (заголовок = 1)."""

    def __init__(self, line_no: int, message: str) -> None:
        super().__init__(f"{line_no}: {message}")
        self.line_no = line_no
        self.message = message


def read_rows(path: str | Path) -> list[Row]:
    """Полностью разбирает файл и возвращает строки в порядке файла."""
    rows: list[Row] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None or [h.strip() for h in header] != list(FIELDS):
            raise ValidationError(1, "ожидается заголовок " + ",".join(FIELDS))
        for values in reader:
            line_no = reader.line_num
            if not values:  # пустая строка
                continue
            if len(values) < len(FIELDS):
                raise ValidationError(
                    line_no,
                    f"ожидалось {len(FIELDS)} поля, получено {len(values)}",
                )
            student, question, answer, correct = values[:4]
            if correct not in ("1", "0"):
                raise ValidationError(
                    line_no, f'поле correct должно быть 1 или 0, получено "{correct}"'
                )
            rows.append(Row(student, question, answer, correct == "1"))
    return rows
