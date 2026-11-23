## Milestone 1: CLI на Python, который читает результаты квиза из CSV (студент, вопрос, ответ, правильно/нет) и печатает долю верных ответов по каждому вопросу и список самых трудных вопросов

Сгенерировано task_bridge из behaviour-spec бандла cli-python-csv-20261123-ba82 (шаг 3 плана развития конвейера; группировка задач — по Feature-секциям). Личный путь: бриф одобрен владельцем в разговоре, задачи исполняются сразу.

### TASK-001: Пакет и чтение CSV с валидацией
P2 | TODO   Est: 0.5d

Реализовать сценарии BEH-01, BEH-02, BEH-03, BEH-04 (DT-01, группа solo).
Source: workstreams/cli-python-csv-20261123-ba82/spec/30-decomposition.md#DT-01

**Checklist:**
- [ ] реализовать BEH-01: Корректный CSV разбирается в строки результатов
- [ ] реализовать BEH-02: Файл с `\r\n` и кириллицей читается одинаково
- [ ] реализовать BEH-03: Недопустимое значение `correct` — ошибка с номером строки
- [ ] реализовать BEH-04: Нехватка полей в строке — ошибка с номером строки
- [ ] проверка группы: tests/test_reader.py::test_read_rows_parses_valid_file (kind: pytest), tests/test_reader.py::test_read_rows_handles_crlf_and_utf8 (kind: pytest), tests/test_reader.py::test_read_rows_rejects_bad_correct_value (kind: pytest), tests/test_reader.py::test_read_rows_rejects_short_row (kind: pytest) зелёные на BEH-01, BEH-02, BEH-03, BEH-04



### TASK-002: Агрегация по вопросам и отбор трудных
P2 | TODO   Est: 0.5d

Реализовать сценарии BEH-05, BEH-06, BEH-07, BEH-08, BEH-09 (DT-02, группа solo).
Source: workstreams/cli-python-csv-20261123-ba82/spec/30-decomposition.md#DT-02
**Depends on:** [TASK-001]

**Checklist:**
- [ ] реализовать BEH-05: Доля верных считается по каждому вопросу
- [ ] реализовать BEH-06: Порядок вопросов — порядок первого появления в CSV
- [ ] реализовать BEH-07: Трудные — строго ниже порога, от худшего
- [ ] реализовать BEH-08: Доля ровно 50% при пороге 50 не трудная
- [ ] реализовать BEH-09: Порог 40 сужает список трудных
- [ ] проверка группы: tests/test_stats.py::test_per_question_computes_share (kind: pytest), tests/test_stats.py::test_per_question_keeps_first_appearance_order (kind: pytest), tests/test_stats.py::test_hardest_sorts_worst_first (kind: pytest), tests/test_stats.py::test_hardest_excludes_value_equal_to_threshold (kind: pytest), tests/test_stats.py::test_hardest_with_threshold_40 (kind: pytest) зелёные на BEH-05, BEH-06, BEH-07, BEH-08, BEH-09



### TASK-003: CLI, порог и текстовый отчёт
P2 | TODO   Est: 0.5d

Реализовать сценарии BEH-10, BEH-11, BEH-12, BEH-13, BEH-14 (DT-03, группа solo).
Source: workstreams/cli-python-csv-20261123-ba82/spec/30-decomposition.md#DT-03
**Depends on:** [TASK-001], [TASK-002]

**Checklist:**
- [ ] реализовать BEH-10: Команда печатает отчёт и завершается кодом 0
- [ ] реализовать BEH-11: Ошибка валидации — stderr, ненулевой код, пустой stdout
- [ ] реализовать BEH-12: Отчёт содержит блок трудных вопросов в нужном порядке
- [ ] реализовать BEH-13: `--threshold 40` меняет блок трудных вопросов
- [ ] реализовать BEH-14: Порог вне диапазона — ошибка аргумента без отчёта
- [ ] проверка группы: tests/test_cli.py::test_main_prints_table_and_exits_zero (kind: pytest), tests/test_cli.py::test_main_reports_validation_error_to_stderr (kind: pytest), tests/test_cli.py::test_main_renders_hard_questions_block (kind: pytest), tests/test_cli.py::test_main_threshold_option_narrows_hard_list (kind: pytest), tests/test_cli.py::test_main_rejects_threshold_out_of_range (kind: pytest) зелёные на BEH-10, BEH-11, BEH-12, BEH-13, BEH-14



