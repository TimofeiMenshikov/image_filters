# Image Filter Project

[![CI](https://github.com/TimofeiMenshikov/image_filters/actions/workflows/ci.yml/badge.svg)](https://github.com/TimofeiMenshikov/image_filters/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/TimofeiMenshikov/image_filters/actions/workflows/ci.yml)

Простой Python-проект для наложения фильтров на изображения.

## Описание

Для каждого изображения в указанной папке применяются два фильтра:
- размытие (`blur`)
- увеличение резкости (`sharpen`)

Результаты сохраняются в выходной папке.

## Установка

```bash
python -m pip install -r requirements.txt
```

Также проект можно запускать через `uv`:

```bash
uv sync --extra dev
```

## Использование

```bash
python3 -m process_images --input-folder path/to/input_folder --output-folder path/to/output_folder
```

Также после установки проекта можно запускать команду из `scripts`:

```bash
image-filters --input-folder path/to/input_folder --output-folder path/to/output_folder
```

Короткие опции:

```bash
image-filters -i path/to/input_folder -o path/to/output_folder
```

Если параметр `--output-folder` не задан, результаты сохраняются в папке `output`.

Запуск через `uv`:

```bash
uv run image-filters --input-folder test_images --output-folder processed_images
```

Эта команда проверена: изображения сохраняются в папке `processed_images`.

## Run targets

Основные режимы запуска описаны через Poe the Poet в `pyproject.toml`.

Показать справку CLI:

```bash
poe help
```

Запустить обработку изображений из папки `images` в папку `output`:

```bash
poe run
```

Запустить тесты:

```bash
poe test
```

Запустить тесты через `uv`:

```bash
uv run pytest
```

Эта команда проверена: тесты проекта успешно выполняются через `uv`.

Проверить покрытие тестами:

```bash
uv run pytest --cov=process_images --cov-report=term-missing
```

Или через Poe the Poet:

```bash
poe coverage
```

Проверить аннотации типов:

```bash
uv run mypy process_images tests
```

Или через Poe the Poet:

```bash
poe typecheck
```

## Проверка требований

Проект закрывает требования к тестированию:
- `pytest` используется для тестов, есть фикстура `mock_image`;
- покрытие кода тестами составляет 100% для пакета `process_images`;
- `unittest.mock.patch` и `MagicMock` используются для изоляции работы с PIL, файловой системой и CLI;
- аннотации типов проверяются командой `mypy process_images tests`;
- CI запускает тесты с coverage и проверку типов.

Собрать HTML-документацию Sphinx:

```bash
poe docs
```

Готовые HTML-файлы появятся в `docs/_build/html`.

## Документация

Документация находится в папке `docs` и включает:
- автоматически сгенерированную API-документацию по докстрингам из `process_images.py`;
- страницу с инструкцией по запуску;
- страницу с примерами ввода-вывода приложения.

## Лицензия

Проект распространяется по лицензии MIT. Текст лицензии находится в файле `LICENSE`.
