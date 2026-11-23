import pytest

from quiz_analyzer.cli import main

HEADER = "student,question,answer,correct\n"


def _csv(tmp_path, correct=(("Q1", 8), ("Q2", 3), ("Q3", 4))):
    lines = [f"s{i},{q},x,{int(i < ok)}" for q, ok in correct for i in range(10)]
    p = tmp_path / "r.csv"
    p.write_text(HEADER + "\n".join(lines) + "\n", encoding="utf-8")
    return str(p)


def test_main_prints_table_and_exits_zero(tmp_path, capsys):
    assert main([_csv(tmp_path)]) == 0
    out = capsys.readouterr().out
    q1 = next(line for line in out.splitlines() if line.startswith("Q1"))
    assert "80.0%" in q1 and "(8/10)" in q1


def test_main_reports_validation_error_to_stderr(tmp_path, capsys):
    p = tmp_path / "r.csv"
    p.write_text(HEADER + "a,Q1,x,1\n" * 5 + "a,Q1,x,yes\n", encoding="utf-8")
    assert main([str(p)]) != 0
    cap = capsys.readouterr()
    assert "7" in cap.err and cap.out == ""


def test_main_renders_hard_questions_block(tmp_path, capsys):
    assert main([_csv(tmp_path)]) == 0
    out = capsys.readouterr().out
    head, block = out.split("Самые трудные вопросы (ниже 50%)")
    assert head.index("Q1") < head.index("Q2") < head.index("Q3")
    assert block.index("Q2") < block.index("Q3")
    assert "30.0%" in block and "(3/10)" in block and "Q1" not in block


def test_main_threshold_option_narrows_hard_list(tmp_path, capsys):
    assert main([_csv(tmp_path), "--threshold", "40"]) == 0
    block = capsys.readouterr().out.split("Самые трудные вопросы (ниже 40%)")[1]
    assert "Q2" in block and "Q3" not in block


def test_main_rejects_threshold_out_of_range(tmp_path, capsys):
    with pytest.raises(SystemExit) as e:
        main([_csv(tmp_path), "--threshold", "150"])
    assert e.value.code != 0
    cap = capsys.readouterr()
    assert cap.err and cap.out == ""


def test_main_reports_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 1
    cap = capsys.readouterr()
    assert cap.err and cap.out == ""


def test_main_prints_none_when_no_hard_questions(tmp_path, capsys):
    assert main([_csv(tmp_path), "--threshold", "0"]) == 0
    assert capsys.readouterr().out.rstrip().endswith("нет")


def test_main_reports_non_utf8_file(tmp_path, capsys):
    p = tmp_path / "r.csv"
    p.write_bytes(HEADER.encode() + b"\xff,Q1,x,1\n")
    assert main([str(p)]) == 1
    cap = capsys.readouterr()
    assert cap.err and cap.out == ""
