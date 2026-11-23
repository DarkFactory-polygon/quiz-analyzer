import pytest

from quiz_analyzer.reader import Row, ValidationError, read_rows

HEADER = "student,question,answer,correct"


def write(tmp_path, text, newline="\n"):
    p = tmp_path / "results.csv"
    p.write_bytes(text.replace("\n", newline).encode("utf-8"))
    return p


def test_read_rows_parses_valid_file(tmp_path):
    p = write(tmp_path, f"{HEADER}\nAnn,Q1,4,1\nBob,Q1,5,0\n")
    assert read_rows(p) == [Row("Ann", "Q1", "4", True), Row("Bob", "Q1", "5", False)]


def test_read_rows_handles_crlf_and_utf8(tmp_path):
    text = f"{HEADER}\nАнна,Q1,да,1\nБорис,Q2,нет,0\n"
    expected = [Row("Анна", "Q1", "да", True), Row("Борис", "Q2", "нет", False)]
    assert read_rows(write(tmp_path, text, "\r\n")) == expected
    assert read_rows(write(tmp_path, text, "\n")) == expected


def test_read_rows_rejects_bad_correct_value(tmp_path):
    lines = [HEADER] + ["A,Q1,x,1"] * 5 + ["A,Q1,x,yes", "A,Q1,x,1"]
    with pytest.raises(ValidationError) as exc:
        read_rows(write(tmp_path, "\n".join(lines) + "\n"))
    assert exc.value.line_no == 7
    assert "correct" in exc.value.message


def test_read_rows_rejects_short_row(tmp_path):
    p = write(tmp_path, f"{HEADER}\nA,Q1,x,1\nA,Q1,1\n")
    with pytest.raises(ValidationError) as exc:
        read_rows(p)
    assert exc.value.line_no == 3


def test_read_rows_rejects_bad_header(tmp_path):
    with pytest.raises(ValidationError) as exc:
        read_rows(write(tmp_path, "a,b\n1,2\n"))
    assert exc.value.line_no == 1


def test_read_rows_rejects_empty_file(tmp_path):
    with pytest.raises(ValidationError):
        read_rows(write(tmp_path, ""))


def test_read_rows_skips_blank_lines_and_counts_them(tmp_path):
    p = write(tmp_path, f"{HEADER}\nA,Q1,x,1\n\nA,Q1,x,maybe\n")
    with pytest.raises(ValidationError) as exc:
        read_rows(p)
    assert exc.value.line_no == 4
