## Проверки

#### BEH-01: Корректный CSV разбирается в строки результатов
Передать `read_rows` файл UTF-8 с заголовком `student,question,answer,correct` и
несколькими строками, где `correct` — `1` или `0`. Возвращается список `Row` в
порядке файла, поле `correct` — `True`/`False`.
- **checked_by**: `kind: pytest` `target: tests/test_reader.py::test_read_rows_parses_valid_file`
**Критерии:** FR-01/1

#### BEH-02: Файл с `\r\n` и кириллицей читается одинаково
Передать `read_rows` файл, сохранённый с переводами строк `\r\n` и
кириллическими именами студентов в UTF-8. Строки разбираются так же, как при
`\n`, без лишних символов в полях.
- **checked_by**: `kind: pytest` `target: tests/test_reader.py::test_read_rows_handles_crlf_and_utf8`
**Критерии:** FR-01/1

#### BEH-03: Недопустимое значение `correct` — ошибка с номером строки
Передать `read_rows` файл, где в седьмой строке файла `correct` равно `yes`.
Поднимается `ValidationError` с `line_no == 7` и сообщением про поле `correct`.
- **checked_by**: `kind: pytest` `target: tests/test_reader.py::test_read_rows_rejects_bad_correct_value`
**Критерии:** FR-01/2

#### BEH-04: Нехватка полей в строке — ошибка с номером строки
Передать `read_rows` файл, где в одной из строк меньше четырёх полей.
Поднимается `ValidationError` с номером этой строки файла (заголовок — строка 1).
- **checked_by**: `kind: pytest` `target: tests/test_reader.py::test_read_rows_rejects_short_row`
**Критерии:** FR-01/2

#### BEH-05: Доля верных считается по каждому вопросу
Передать `per_question` строки, где у Q1 8 верных из 10. В результате для Q1
`correct == 8`, `total == 10`, `share == 80.0`.
- **checked_by**: `kind: pytest` `target: tests/test_stats.py::test_per_question_computes_share`
**Критерии:** FR-02/1

#### BEH-06: Порядок вопросов — порядок первого появления в CSV
Передать `per_question` строки, где вопросы впервые встречаются в порядке
Q3, Q1, Q2 (и затем перемешаны). Элементы результата идут Q3, Q1, Q2.
- **checked_by**: `kind: pytest` `target: tests/test_stats.py::test_per_question_keeps_first_appearance_order`
**Критерии:** FR-02/2

#### BEH-07: Трудные — строго ниже порога, от худшего
Передать `hardest` таблицу с долями Q1 80, Q2 30, Q3 45 и порог 50. Результат —
ровно `[Q2, Q3]` в этом порядке.
- **checked_by**: `kind: pytest` `target: tests/test_stats.py::test_hardest_sorts_worst_first`
**Критерии:** FR-03/1

#### BEH-08: Доля ровно 50% при пороге 50 не трудная
Передать `hardest` таблицу, где у вопроса доля ровно `50.0`, с порогом по
умолчанию 50. Этот вопрос в результат не попадает.
- **checked_by**: `kind: pytest` `target: tests/test_stats.py::test_hardest_excludes_value_equal_to_threshold`
**Критерии:** FR-03/2

#### BEH-09: Порог 40 сужает список трудных
Передать `hardest` ту же таблицу (80/30/45) с порогом 40. Результат — ровно
`[Q2]`.
- **checked_by**: `kind: pytest` `target: tests/test_stats.py::test_hardest_with_threshold_40`
**Критерии:** FR-03/3

#### BEH-10: Команда печатает отчёт и завершается кодом 0
Запустить `quiz-analyzer results.csv` (или `python -m quiz_analyzer`) на валидном
файле, где у Q1 8 верных из 10. Код выхода 0, в stdout строка с `Q1`, `80.0%` и
`(8/10)`.
- **checked_by**: `kind: pytest` `target: tests/test_cli.py::test_main_prints_table_and_exits_zero`
**Критерии:** FR-01/1, FR-02/1

#### BEH-11: Ошибка валидации — stderr, ненулевой код, пустой stdout
Запустить команду на файле с `correct: yes` в седьмой строке. Код выхода
ненулевой, в stderr сообщение с номером строки `7`, stdout пуст.
- **checked_by**: `kind: pytest` `target: tests/test_cli.py::test_main_reports_validation_error_to_stderr`
**Критерии:** FR-01/2

#### BEH-12: Отчёт содержит блок трудных вопросов в нужном порядке
Запустить команду на файле с долями Q1 80%, Q2 30%, Q3 45%. В stdout таблица в
порядке появления, затем блок «Самые трудные вопросы (ниже 50%)» со строками
Q2 и затем Q3, доли в формате `NN.N%`, счёт как `(3/10)`.
- **checked_by**: `kind: pytest` `target: tests/test_cli.py::test_main_renders_hard_questions_block`
**Критерии:** FR-02/2, FR-03/1, FR-03/2

#### BEH-13: `--threshold 40` меняет блок трудных вопросов
Запустить команду с `--threshold 40` на тех же данных. В блоке трудных
вопросов только Q2, код выхода 0.
- **checked_by**: `kind: pytest` `target: tests/test_cli.py::test_main_threshold_option_narrows_hard_list`
**Критерии:** FR-03/3

#### BEH-14: Порог вне диапазона — ошибка аргумента без отчёта
Запустить команду с `--threshold 150`. Код выхода ненулевой, сообщение в
stderr, отчёт в stdout не печатается.
- **checked_by**: `kind: pytest` `target: tests/test_cli.py::test_main_rejects_threshold_out_of_range`
**Критерии:** FR-03/3

## Задачи

#### DT-01: Пакет и чтение CSV с валидацией · type: implement · owner: dev
scenarios: [BEH-01, BEH-02, BEH-03, BEH-04]
depends_on: []
parallel_group: solo
**Решения дизайна:** D-01, D-03, D-04, D-09, D-10, D-11
Создать пакет `quiz_analyzer` (пустые модули по дизайну), `pyproject.toml` с
`console_scripts` и Python 3.11+, и `reader.read_rows`: открытие файла только на
чтение с `encoding="utf-8"`, `newline=""`, `csv.DictReader`, полный разбор в
память и `ValidationError(line_no, message)` на неверный `correct` или нехватку
полей. Печать и агрегация — не здесь.

#### DT-02: Агрегация по вопросам и отбор трудных · type: implement · owner: dev
scenarios: [BEH-05, BEH-06, BEH-07, BEH-08, BEH-09]
depends_on: [DT-01]
parallel_group: solo
**Решения дизайна:** D-05, D-06
Реализовать `stats.per_question` (один проход, счётчики в `dict`, порядок
первого появления, `share = 100 * correct / total`) и `stats.hardest`
(фильтр `share < threshold`, сортировка по возрастанию доли). Форматирование
строк не входит.

#### DT-03: CLI, порог и текстовый отчёт · type: implement · owner: dev
scenarios: [BEH-10, BEH-11, BEH-12, BEH-13, BEH-14]
depends_on: [DT-01, DT-02]
parallel_group: solo
**Решения дизайна:** D-02, D-07, D-08
Реализовать `cli.main` на `argparse` (позиционный путь, `--threshold` как
`float` процентов со значением по умолчанию 50 и проверкой `[0, 100]`, код
выхода 0/1, ошибки в stderr), `__main__.py` и `report.render` — таблица
«вопрос / доля / счёт» плюс блок трудных вопросов с указанием порога.
