# Импорты для работы с путями и файловой системой
from pathlib import Path

# Импорты для создания mock'ов (имитаций объектов) в тестах
from unittest.mock import MagicMock, patch

# Фреймворк для написания и запуска тестов
import pytest

# Импорты для тестирования CLI
from click.testing import CliRunner

# Импортируем модуль который тестируем
import process_images


# pytest fixture - вспомогательная функция для подготовки тестовых данных
@pytest.fixture
def mock_image() -> MagicMock:
    """Создает mock объект изображения для изоляции тестов от реальной PIL библиотеки"""
    image = MagicMock()  # Создаем имитацию объекта изображения
    filtered_image = MagicMock()  # Создаем имитацию обработанного изображения
    # Настраиваем, что вызов convert() возвращает то же изображение
    image.convert.return_value = image
    # Настраиваем, что вызов filter() возвращает обработанное изображение
    image.filter.return_value = filtered_image
    # Подготавливаем mock для метода save()
    filtered_image.save = MagicMock()
    return image


def test_process_image_applies_filters_and_saves(
    mock_image: MagicMock, tmp_path: Path
) -> None:
    """Тест проверяет что процесс обработки применяет фильтры и сохраняет файлы"""
    # Подготавливаем пути для теста
    image_path = tmp_path / "sample.jpg"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Создаем mock для контекстного менеджера (with statement)
    image_context = MagicMock()
    image_context.__enter__.return_value = mock_image

    # Заменяем реальную функцию Image.open на нашу имитацию
    with patch("process_images.Image.open", return_value=image_context) as open_patch:
        # Вызываем тестируемую функцию
        process_images.process_image(image_path, output_dir)

    # Проверяем что Image.open был вызван с правильным путем
    open_patch.assert_called_once_with(image_path)
    # Проверяем что контекстный менеджер был правильно закрыт
    image_context.__exit__.assert_called_once()
    # Проверяем что convert был вызван с RGB параметром
    mock_image.convert.assert_called_once_with("RGB")
    # Проверяем что фильтры были применены для каждого фильтра в словаре
    assert mock_image.filter.call_count == len(process_images.FILTERS)

    # Проверяем что сохраняются файлы с правильными именами
    expected_paths = [
        output_dir / f"sample_{name}.jpg" for name in process_images.FILTERS
    ]
    actual_save_calls = [
        call.args[0] for call in mock_image.filter.return_value.save.call_args_list
    ]
    assert actual_save_calls == expected_paths


def test_process_folder_creates_output_and_processes_files(tmp_path: Path) -> None:
    """Тест проверяет что process_folder создает выходную папку и обрабатывает файлы"""
    # Подготавливаем структуру папок для теста
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    # Создаем тестовые файлы
    (input_dir / "one.jpg").write_text("fake")
    (input_dir / "two.png").write_text("fake")
    (input_dir / "ignore.txt").write_text("ignore")  # Этот файл должен быть пропущен

    # Заменяем process_image на mock для изоляции теста
    with patch("process_images.process_image") as process_image_patch:
        process_images.process_folder(input_dir, output_dir)

    # Проверяем что выходная папка была создана
    assert output_dir.exists()
    # Проверяем что process_image был вызван только для 2 изображений (не для txt)
    assert process_image_patch.call_count == 2
    # Проверяем что файлы обрабатываются в алфавитном порядке
    assert process_image_patch.call_args_list[0].args[0].name == "one.jpg"
    assert process_image_patch.call_args_list[1].args[0].name == "two.png"


def test_process_folder_skips_non_supported_files_and_logs_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Тест проверяет сообщение при отсутствии поддерживаемых изображений."""
    # Подготавливаем структуру папок
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    # Создаем файл который не поддерживается
    (input_dir / "readme.md").write_text("ignore")

    # Заменяем iterdir на mock который возвращает пустой список
    with patch("pathlib.Path.iterdir", return_value=[]):
        process_images.process_folder(input_dir, output_dir)

    # Захватываем вывод программы
    captured = capsys.readouterr()
    # Проверяем что выведено правильное сообщение
    assert "No supported images found" in captured.out
    # Проверяем что выходная папка была создана даже без файлов
    assert output_dir.exists()


def test_process_folder_raises_for_missing_directory(tmp_path: Path) -> None:
    """Тест проверяет, что при отсутствующей папке выбрасывается ошибка."""
    missing_dir = tmp_path / "missing"
    output_dir = tmp_path / "output"

    with pytest.raises(NotADirectoryError, match="Input folder does not exist"):
        process_images.process_folder(missing_dir, output_dir)


def test_module_entrypoint_shows_help(capsys, monkeypatch) -> None:
    """Тест проверяет работу точки входа при запуске как модуля."""
    monkeypatch.setattr("sys.argv", ["python", "--help"])

    with pytest.raises(SystemExit) as excinfo:
        __import__("runpy").run_module("process_images", run_name="__main__")

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "Apply blur and sharpen filters" in captured.out


def test_cli_uses_default_output_folder(tmp_path: Path) -> None:
    """Тест проверяет что CLI использует папку 'output' по умолчанию"""
    # Подготавливаем папку с входными файлами
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    # Создаем runner для тестирования CLI
    runner = CliRunner()

    # Заменяем process_folder на mock для изоляции CLI от реальной обработки
    with patch("process_images.process_folder") as process_folder_patch:
        # Вызываем CLI команду без указания выходной папки
        result = runner.invoke(process_images.main, ["--input-folder", str(input_dir)])

    # Проверяем что команда выполнилась успешно
    assert result.exit_code == 0
    # Проверяем что была использована папка output по умолчанию
    process_folder_patch.assert_called_once_with(input_dir, Path("output"))


def test_cli_accepts_short_options(tmp_path: Path) -> None:
    """Тест проверяет что CLI принимает сокращенные опции (-i и -o)"""
    # Подготавливаем папки для теста
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "filtered"
    input_dir.mkdir()
    # Создаем runner для тестирования CLI
    runner = CliRunner()

    # Заменяем process_folder на mock
    with patch("process_images.process_folder") as process_folder_patch:
        # Вызываем CLI с сокращенными опциями
        result = runner.invoke(
            process_images.main, ["-i", str(input_dir), "-o", str(output_dir)]
        )

    # Проверяем что команда выполнилась успешно
    assert result.exit_code == 0
    # Проверяем что функция была вызвана с правильными параметрами
    process_folder_patch.assert_called_once_with(input_dir, output_dir)
