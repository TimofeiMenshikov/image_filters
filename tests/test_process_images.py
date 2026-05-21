from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

import process_images


@pytest.fixture
def mock_image() -> MagicMock:
    """Return a fake PIL image object."""
    image = MagicMock()
    filtered_image = MagicMock()
    image.convert.return_value = image
    image.filter.return_value = filtered_image
    filtered_image.save = MagicMock()
    return image


def test_process_image_applies_filters_and_saves(
    mock_image: MagicMock, tmp_path: Path
) -> None:
    image_path = tmp_path / "sample.jpg"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    image_context = MagicMock()
    image_context.__enter__.return_value = mock_image

    with patch("process_images.Image.open", return_value=image_context) as open_patch:
        process_images.process_image(image_path, output_dir)

    open_patch.assert_called_once_with(image_path)
    image_context.__exit__.assert_called_once()
    mock_image.convert.assert_called_once_with("RGB")
    assert mock_image.filter.call_count == len(process_images.FILTERS)

    expected_paths = [
        output_dir / f"sample_{name}.jpg" for name in process_images.FILTERS
    ]
    actual_save_calls = [
        call.args[0] for call in mock_image.filter.return_value.save.call_args_list
    ]
    assert actual_save_calls == expected_paths


def test_process_folder_creates_output_and_processes_files(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "one.jpg").write_text("fake")
    (input_dir / "two.png").write_text("fake")
    (input_dir / "ignore.txt").write_text("ignore")

    with patch("process_images.process_image") as process_image_patch:
        process_images.process_folder(input_dir, output_dir)

    assert output_dir.exists()
    assert process_image_patch.call_count == 2
    assert process_image_patch.call_args_list[0].args[0].name == "one.jpg"
    assert process_image_patch.call_args_list[1].args[0].name == "two.png"


def test_process_folder_skips_non_supported_files_and_logs_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "readme.md").write_text("ignore")

    with patch("pathlib.Path.iterdir", return_value=[]):
        process_images.process_folder(input_dir, output_dir)

    captured = capsys.readouterr()
    assert "No supported images found" in captured.out
    assert output_dir.exists()


def test_process_folder_raises_for_missing_directory(tmp_path: Path) -> None:
    missing_dir = tmp_path / "missing"
    output_dir = tmp_path / "output"

    with pytest.raises(NotADirectoryError, match="Input folder does not exist"):
        process_images.process_folder(missing_dir, output_dir)


def test_module_entrypoint_shows_help(capsys, monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["python", "--help"])

    with pytest.raises(SystemExit) as excinfo:
        __import__("runpy").run_module("process_images", run_name="__main__")

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "Apply blur and sharpen filters" in captured.out


def test_cli_uses_default_output_folder(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    runner = CliRunner()

    with patch("process_images.process_folder") as process_folder_patch:
        result = runner.invoke(process_images.main, ["--input-folder", str(input_dir)])

    assert result.exit_code == 0
    process_folder_patch.assert_called_once_with(input_dir, Path("output"))


def test_cli_accepts_short_options(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "filtered"
    input_dir.mkdir()
    runner = CliRunner()

    with patch("process_images.process_folder") as process_folder_patch:
        result = runner.invoke(
            process_images.main, ["-i", str(input_dir), "-o", str(output_dir)]
        )

    assert result.exit_code == 0
    process_folder_patch.assert_called_once_with(input_dir, output_dir)
