import os
import pytest
import cv2
import fitz
from unittest.mock import patch, MagicMock
from main import (
    convert_to_images,
    read_code,
    read_text,
    scan_pdf,
    pdf_path,
    out_path
)


# Создадим фикстуры для временного PDF и PNG
@pytest.fixture
def mock_pdf_file(tmp_path):
    # Создаем временный PDF файл
    pdf_file = tmp_path / ".\\Data\\test.pdf"
    with open(pdf_file, "wb") as f:
        f.write(b"%PDF-1.4\n%...")  # Минимальная структура PDF
    return pdf_file


@pytest.fixture
def mock_image_file(tmp_path):
    # Создаем временный PNG файл
    image_file = tmp_path / ".\\Data\\test.png"
    # Создаем пустое изображение и сохраняем его
    img = cv2.imread('.\\Data\\clear.png')
    if img is not None:
        cv2.imwrite(str(image_file), img)
    return image_file


def test_convert_to_images(mock_pdf_file, mock_image_file):
    convert_to_images(mock_pdf_file, mock_image_file)
    assert os.path.exists(mock_image_file)
    # Проверка, что файл не пустой или имеет ожидаемый размер
    assert os.path.getsize(mock_image_file) > 0


@patch('cv2.imread')
@patch('pyzbar.pyzbar.decode')
def test_read_code(mock_decode, mock_imread, mock_image_file):
    # Настраиваем имитацию
    mocked_image = MagicMock()
    mock_imread.return_value = mocked_image
    mock_decode.return_value = [MagicMock(rect=MagicMock(left=10, top=10, width=30, height=30), data=b'test_code')]

    read_code(mock_image_file)

    # Проверяем, что код успешно прочитан
    assert len(page_text) == 1
    assert page_text[0] == 'test_code'


@patch('pdfminer.high_level.extract_pages')
@patch('pdfminer.layout.LTTextContainer')
def test_read_text(mock_LTTextContainer, mock_extract_pages, mock_pdf_file):
    # Настройка имитации
    mock_element = MagicMock()
    mock_element.get_text.return_value = "Sample text"
    mock_LTTextContainer.return_value = mock_element

    mock_extract_pages.return_value = [[mock_element]]

    read_text(mock_pdf_file)

    # Проверяем, что текст успешно извлечен
    assert len(page_text) == 1
    assert page_text[0] == "Sample text"


@patch('your_module.convert_to_images')
@patch('your_module.read_code')
@patch('your_module.read_text')
def test_scan_pdf(mock_read_text, mock_read_code, mock_convert_to_images, mock_pdf_file, mock_image_file):
    mock_convert_to_images.return_value = None
    mock_read_code.return_value = None
    mock_read_text.return_value = None

    result = scan_pdf(mock_pdf_file, mock_image_file)

    mock_convert_to_images.assert_called_once_with(mock_pdf_file, mock_image_file)
    mock_read_code.assert_called_once_with(mock_image_file)
    mock_read_text.assert_called_once_with(mock_pdf_file)
    assert result is None  # Или проверьте результат на основе ваших ожиданий

