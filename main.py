# Библиотека для чтения данных из .png
import cv2
# Библиотека для конвертирования .pdf в .png
import fitz
# Библиотека для записи .pdf в массив данных для чтения
import PyPDF2
# Библиотеки для анализа и чтения данных из массива
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer
# Библиотека для чтения штрих-кодов
from pyzbar.pyzbar import decode, ZBarSymbol
#-----НАСТРОЙКИ И ПЕРЕМЕННЫЕ-------------------------------------------
# Пути к файлу для обработки
pdf_path = '.\\Data\\test.pdf'
# Временный файл для чтения штрих-кодов
out_path = '.\\Data\\test.png'
# Создание объекта .pdf файла
pdfFileObj = open(pdf_path, 'rb')
# Анализ и сортировка объектов .pdf файла
pdfRead = PyPDF2.PdfReader(pdfFileObj)
# Словарь для записи в него данных
text_per_page = {}
# Списки с данными
#Список с текстовыми данными
page_text = []
#Список с данными штрих-кодов
text_from_images = []
#Список с общим контентом
page_content = []

#-----ФУНКЦИИ-------------------------------------------
# Функция для получения текста из .pdf
def get_text(element):
    #Получаем текст из объекта в виде строки
    line_text = element.get_text()
    #Возвращаем текст из объекта
    return line_text

# Функция для поиска баркодов на изображениее
def draw_barcode(decoded, image):

    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image

# Функция для конвертации .pdf в .png
def convert_to_images(input_file, output_file):
    doc = fitz.open(input_file)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    output = output_file
    pix.save(output)
    doc.close()

#Функция для чтения данных из штрих-кода
def read_code(out_path):
    image = cv2.imread(out_path)
    detectedBarcodes = decode(image)
    for barcode in detectedBarcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
        barcode_data = str(barcode.data).replace('\'', '').replace('b', '')
        text_from_images.append(barcode_data)
        page_content.append(f'{barcode_data}\n')

#Функция для чтения текста из файла .pdf
def read_text(pdf_path):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                line_text = get_text(element)
                page_text.append(line_text)
                page_content.append(line_text)

#Основная функция
def scan_pdf(pdf_path, out_path):
    convert_to_images(pdf_path, out_path)
    read_code(out_path)
    read_text(pdf_path)
    # Cмотреть что насканировал
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    dictionary_key = 'Page'
    text_per_page[dictionary_key] = [page_text, text_from_images, page_content]
    # Закрываем объект файла pdf
    pdfFileObj.close()
    # Отображение контента
    result = ''.join(text_per_page['Page'][2])
    # Отображение контента
    print(result)
    return result

#-------ТЕЛО----------------------------------------
if __name__ == '__main__':
    data_from_pdf = scan_pdf(pdf_path, out_path)




