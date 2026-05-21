"""Apply image filters to every supported image in a folder.

The module exposes a small Click command-line interface and reusable helper
functions. Each source image is converted to RGB, then saved twice: once with
blur and once with sharpen applied.
"""

# Импорты для работы с путями и файловой системой
from pathlib import Path

# Импорты для создания CLI и обработки изображений
import click  # Фреймворк для создания командной строки
from PIL import Image, ImageFilter  # Библиотека для обработки изображений

# Поддерживаемые форматы изображений для обработки
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
"""File extensions accepted by the folder processor."""

# Словарь доступных фильтров и их объектов из PIL
FILTERS = {
    "blur": ImageFilter.BLUR,  # Размытие
    "sharpen": ImageFilter.SHARPEN,  # Увеличение резкости
}
"""Filters applied to each image and used in generated output filenames."""


def process_image(image_path: Path, output_dir: Path) -> None:
    """Apply all configured filters to one image and save the results.

    Args:
        image_path: Path to the source image.
        output_dir: Directory where filtered images are written.

    The output filenames keep the original stem and extension, adding the
    filter name before the extension, for example ``photo_blur.jpg``.
    """
    # Открываем изображение в контекстном менеджере (автоматически закроется)
    with Image.open(image_path) as image:
        # Конвертируем в RGB для совместимости всех фильтров
        rgb_image = image.convert("RGB")

        # Применяем каждый фильтр из словаря FILTERS
        for filter_name, filter_obj in FILTERS.items():
            # Применяем фильтр к изображению
            filtered = rgb_image.filter(filter_obj)
            # Формируем имя выходного файла: photo_blur.jpg, photo_sharpen.jpg и т.д.
            output_path = (
                output_dir / f"{image_path.stem}_{filter_name}{image_path.suffix}"
            )
            # Сохраняем обработанное изображение
            filtered.save(output_path)
            print(f"Saved: {output_path}")


def process_folder(input_dir: Path, output_dir: Path) -> None:
    """Process every supported image in a folder.

    Args:
        input_dir: Folder containing source images.
        output_dir: Folder where generated images are saved.

    Raises:
        NotADirectoryError: If ``input_dir`` does not exist or is not a folder.
    """
    # Преобразуем пути в абсолютные (полные) пути
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()

    # Проверяем, существует ли папка с входными изображениями
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input folder does not exist: {input_dir}")

    # Создаем папку для результатов, если она не существует
    output_dir.mkdir(parents=True, exist_ok=True)

    # Фильтруем файлы: оставляем только поддерживаемые форматы изображений
    image_files = [
        p
        for p in input_dir.iterdir()
        if p.suffix.lower() in SUPPORTED_EXTENSIONS and p.is_file()
    ]

    # Если изображений не найдено, выводим сообщение и выходим
    if not image_files:
        print(f"No supported images found in {input_dir}")
        return

    # Сортируем файлы по имени и обрабатываем каждый
    for image_path in sorted(image_files):
        print(f"Processing: {image_path.name}")
        process_image(image_path, output_dir)


# Декоратор создает CLI команду
@click.command()
# Опция для входной папки (обязательный параметр)
@click.option(
    "-i",
    "--input-folder",
    required=True,  # Параметр обязателен
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Folder with source images.",
)
# Опция для выходной папки (необязательный параметр с значением по умолчанию)
@click.option(
    "-o",
    "--output-folder",
    default=Path("output"),  # По умолчанию создаст папку 'output'
    show_default=True,  # Показывать значение по умолчанию в справке
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Folder to save processed images.",
)
def main(input_folder: Path, output_folder: Path) -> None:
    """Apply blur and sharpen filters to every image in a folder.

    The command reads images from ``--input-folder`` and writes generated files
    to ``--output-folder``. If no output folder is provided, ``output`` is used.
    """
    process_folder(input_folder, output_folder)
