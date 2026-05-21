"""Apply image filters to every supported image in a folder."""

from pathlib import Path

import click
from PIL import Image, ImageFilter

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
"""File extensions accepted by the folder processor."""

FILTERS = {
    "blur": ImageFilter.BLUR,
    "sharpen": ImageFilter.SHARPEN,
}
"""Filters applied to each image and used in generated output filenames."""


def process_image(image_path: Path, output_dir: Path) -> None:
    """Apply all configured filters to one image and save the results.

    Args:
        image_path: Path to the source image.
        output_dir: Directory where filtered images are written.

    Output filenames keep the original stem and extension, adding the filter
    name before the extension, for example ``photo_blur.jpg``.
    """
    with Image.open(image_path) as image:
        rgb_image = image.convert("RGB")

        for filter_name, filter_obj in FILTERS.items():
            filtered = rgb_image.filter(filter_obj)
            output_path = (
                output_dir / f"{image_path.stem}_{filter_name}{image_path.suffix}"
            )
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
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input folder does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = [
        p
        for p in input_dir.iterdir()
        if p.suffix.lower() in SUPPORTED_EXTENSIONS and p.is_file()
    ]

    if not image_files:
        print(f"No supported images found in {input_dir}")
        return

    for image_path in sorted(image_files):
        print(f"Processing: {image_path.name}")
        process_image(image_path, output_dir)


@click.command()
@click.option(
    "-i",
    "--input-folder",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Folder with source images.",
)
@click.option(
    "-o",
    "--output-folder",
    default=Path("output"),
    show_default=True,
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Folder to save processed images.",
)
def main(input_folder: Path, output_folder: Path) -> None:
    """Apply blur and sharpen filters to every image in a folder.

    The command reads images from ``--input-folder`` and writes generated files
    to ``--output-folder``. If no output folder is provided, ``output`` is used.
    """
    process_folder(input_folder, output_folder)
