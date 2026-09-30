# REPORT — Практическая работа: pip + Poetry

## 1. Версия Python, Poetry и ОС

### Python

В работе использовался Python 3.12.

Проверка:

```bash
poetry run python --version
````

Результат:

```text
Python 3.12.14
```

### Poetry

Проверка:

```bash
poetry --version
```

Результат:

```text
Poetry (version 2.5.1)
```

### Операционная система

Работа выполнялась на macOS.

---

## 2. Пути к интерпретаторам обеих частей

### pip_project

Для `pip_project` было создано виртуальное окружение `.venv`.

Путь к интерпретатору:

```text
/Users/mariabyckova/Documents/питончик/mlops/lab_2/pip_project/.venv/bin/python
```

Используемая версия:

```text
Python 3.12.14
```

Проверка выполнялась командой:

```bash
python -c "import sys; print(sys.executable)"
```

### poetry_project

Для Poetry было настроено создание виртуального окружения внутри проекта.

Файл `poetry.toml`:

```toml
[virtualenvs]
in-project = true
```

Проверка:

```bash
poetry env info
```

Результат:

```text
Python:         3.12.14
Implementation: CPython
Path:           /Users/mariabyckova/Documents/питончик/mlops/lab_2/poetry_project/.venv
Executable:     /Users/mariabyckova/Documents/питончик/mlops/lab_2/poetry_project/.venv/bin/python
Valid:          True
```

---

## 3. Прямые зависимости

Для программы `plt_temp.py` используются следующие прямые зависимости:

| Зависимость  | Версия | Назначение                              |
| ------------ | -----: | --------------------------------------- |
| `requests`   | 2.34.2 | HTTP-запрос к Open-Meteo API            |
| `pandas`     |  3.0.6 | Обработка данных и создание `DataFrame` |
| `matplotlib` | 3.11.2 | Построение графика температуры          |

Зависимости были добавлены командой:

```bash
poetry add requests pandas matplotlib
```

В `pyproject.toml` они представлены следующим образом:

```toml
dependencies = [
    "requests (>=2.34.2,<3.0.0)",
    "pandas (>=3.0.6,<4.0.0)",
    "matplotlib (>=3.11.2,<4.0.0)"
]
```

---

## 4. Примеры транзитивных зависимостей

Дерево зависимостей было просмотрено командой:

```bash
poetry show --tree
```

Примеры транзитивных зависимостей:

```text
matplotlib
└── contourpy
```

```text
pandas
└── numpy
```

```text
requests
└── certifi
```

Таким образом:

* `numpy` устанавливается как зависимость `pandas`;
* `contourpy` устанавливается как зависимость `matplotlib`;
* `certifi` устанавливается как зависимость `requests`.

---

## 5. Результат восстановления pip_project


Зависимости проекта были зафиксированы в `requirements.txt`.

Для проверки воспроизводимости окружение было восстановлено из этого файла:

```bash
pip install -r requirements.txt
```


Результат: В нём зафиксированы установленные версии зависимостей.

Пример содержимого:

```text
certifi==2026.7.22
charset-normalizer==3.5.2
contourpy==1.4.0
cycler==0.12.1
fonttools==4.66.1
idna==3.20
kiwisolver==1.5.1
matplotlib==3.11.2
numpy==2.5.3
packaging==26.3
pandas==3.0.6
pillow==12.3.0
pyparsing==3.3.3
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
urllib3==2.8.0
```

Программа была запущена командой:

```bash
python plt_temp.py
```

Результат:

```text
Сохранено в temperature_24h.csv
```

---

## 6. Результат проверки групп Poetry

В Poetry были созданы две дополнительные группы зависимостей.

### Группа `test`

В группу `test` добавлен `pytest`:

```bash
poetry add --group test pytest
```

Проверка:

```bash
poetry show --only test
```

Результат содержит:

```text
pytest 9.1.1
```

### Группа `dev`

В группу `dev` добавлен `ruff`:

```bash
poetry add --group dev ruff
```

Проверка:

```bash
poetry show --only dev
```

Результат:

```text
ruff 0.16.9
```

В `pyproject.toml` группы имеют вид:

```toml
[dependency-groups]
test = [
    "pytest (>=9.1.1,<10.0.0)"
]

dev = [
    "ruff (>=0.16.9,<0.17.0)"
]
```

### Эксперимент с группами

Были проверены три варианта окружения.

| Окружение           | `plt_temp.py` | `pytest`     | `ruff`       |
| ------------------- | ------------- | ------------ | ------------ |
| `main`              |  работает    |  недоступен |  недоступен |
| `main + test`       |  работает    |  работает   |  недоступен |
| `main + test + dev` |  работает    |  работает   |  работает   |

### Только `main`

Использовалась команда:

```bash
poetry sync --only main
```

Результат:

```text
plt_temp.py → работает
pytest → Command not found
ruff → Command not found
```

### `main + test`

Использовалась команда:

```bash
poetry sync --only main,test
```

Результат:

```text
plt_temp.py → работает
pytest → 1 passed
ruff → Command not found
```

### `main + test + dev`

Использовалась команда:

```bash
poetry sync
```

Результат:

```text
plt_temp.py → работает
pytest → 1 passed
ruff → ruff 0.16.9
```

Эксперимент показывает, что группы позволяют отделять зависимости, необходимые для запуска программы, тестирования и разработки.

---

## 7. Изменения после точечного обновления зависимости

Для проверки точечного обновления была выбрана прямая зависимость `requests`.

Исходное ограничение в `pyproject.toml`:

```toml
"requests (>=2.34.2,<3.0.0)"
````

Была выполнена команда:

```bash
poetry update requests
```

Результат:

```text
Updating dependencies
Resolving dependencies...

No dependencies to install or update
```

После этого была проверена установленная версия:

```bash
poetry show requests
```

Результат:

```text
name         : requests
version      : 2.34.2
```

Также была выполнена проверка устаревших зависимостей:

```bash
poetry show --outdated
```

Устаревших зависимостей обнаружено не было.

### Анализ результата

* Ограничение прямой зависимости `requests` в `pyproject.toml` **не изменилось**: `>=2.34.2,<3.0.0`.
* Установленная версия `requests` **не изменилась** и осталась `2.34.2`.
* Транзитивные зависимости `requests` **не изменились**, поскольку обновление не было выполнено.
* Обновление не может перейти на версию `3.x`, поскольку задано ограничение `<3.0.0`.
* Отсутствие обновления не является ошибкой: более новой совместимой версии в заданном диапазоне на момент проверки не было.

Таким образом, после выполнения точечного обновления состояние зависимостей проекта не изменилось.

---

## 8. Результат чистого восстановления Poetry-проекта

Для проверки воспроизводимости сначала было удалено виртуальное окружение:

```bash
poetry env remove --all
```

Результат:

```text
Deleted virtualenv:
.../poetry_project/.venv
```

После этого окружение было полностью восстановлено командой:

```bash
poetry install
```

Poetry автоматически обнаружил подходящую версию Python:

```text
Using python3.12 (3.12.14)
```

и создал новое виртуальное окружение:

```text
Creating virtualenv poetry-project in .../poetry_project/.venv
```

Зависимости были установлены из lock-файла:

```text
Installing dependencies from lock file
```

### Проверка Python

```bash
poetry run python --version
```

Результат:

```text
Python 3.12.14
```

### Проверка тестов

```bash
poetry run pytest
```

Результат:

```text
tests/test_dataframe.py . [100%]

1 passed in 16.10s
```

### Проверка Ruff

```bash
poetry run ruff --version
```

Результат:

```text
ruff 0.16.9
```

### Проверка основной программы

```bash
poetry run python plt_temp.py
```

Результат:

```text
Сохранено:
- temperature_24h.csv
- temperature_24h.png
```

Таким образом, после полного удаления `.venv` окружение было успешно восстановлено из `pyproject.toml` и `poetry.lock`.

---

## 9. Сравнение venv + pip и Poetry

### venv + pip

При использовании `venv + pip` виртуальное окружение создаётся отдельно:

```text
pip_project/.venv
```

Зависимости фиксируются в файле:

```text
requirements.txt
```

Для восстановления окружения используется:

```bash
pip install -r requirements.txt
```

Основное преимущество такого подхода — простота и распространённость.

### Poetry

В Poetry используются:

```text
pyproject.toml
poetry.lock
```

`pyproject.toml` содержит информацию о проекте, диапазоны версий зависимостей и группы зависимостей.

`poetry.lock` фиксирует конкретные версии зависимостей, включая транзитивные зависимости.

Восстановление выполняется:

```bash
poetry install
```

или:

```bash
poetry sync
```

Poetry также позволяет разделять зависимости по группам:

```text
main
test
dev
```

Например:

```bash
poetry sync --only main
```

устанавливает только основные зависимости, а:

```bash
poetry sync
```

восстанавливает полное окружение.

### Итоговое сравнение

| Характеристика           | venv + pip                        | Poetry                           |
| ------------------------ | --------------------------------- | -------------------------------- |
| Виртуальное окружение    | `.venv`                           | `.venv`                          |
| Файл зависимостей        | `requirements.txt`                | `pyproject.toml` + `poetry.lock` |
| Фиксация версий          | `requirements.txt`                | `poetry.lock`                    |
| Транзитивные зависимости | фиксируются в requirements.txt    | фиксируются в lock-файле         |
| Группы зависимостей      | отдельно не предусмотрены         | `test`, `dev` и др.              |
| Восстановление окружения | `pip install -r requirements.txt` | `poetry install` / `poetry sync` |
| Управление зависимостями | `pip install/uninstall`           | `poetry add/remove/update`       |

В рамках работы оба подхода позволили создать изолированное окружение и воспроизвести зависимости проекта. Poetry дополнительно предоставляет централизованное описание проекта, lock-файл и механизм группировки зависимостей.
