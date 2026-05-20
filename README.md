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
