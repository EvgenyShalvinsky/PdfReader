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
# Словарь для записи контента
#content_pdf = {}
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
    #Ищем штрих-код и рисуем поля
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    #Возвращаем штрих-код
    return image

# Функция для конвертации .pdf в .png
def convert_to_images(input_file, output_file):
    #Открывает файл
    doc = fitz.open(input_file)
    #Считывает данные из файла
    page = doc.load_page(0)
    #Формирует данные в массив картинки
    pix = page.get_pixmap()
    #Сохраняет новый файл в формате .png
    pix.save(output_file)
    #Закрывает файл
    doc.close()

#Функция для чтения данных из штрих-кода
def read_code(out_path):
    #Считывает .png файл как изображение
    image = cv2.imread(out_path)
    #Находим все штрих-кода на картинке
    detectedBarcodes = decode(image)
    #Создан счетчик штрих-кодов
    i = 0
    #Перебирает все штрих-кода на изображении по очереди
    for barcode in detectedBarcodes:
        #Увеличивает счетчик штрих-кодов
        i = i + 1
        #Определяем положение штрих-кодов
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
        #Считываем данные из штрих-кодов в формате utf-8
        barcode_data = str(barcode.data).replace('\'', '').replace('b', '')
        #Обновляем списки и словари
        text_from_images.append(barcode_data)
        page_content.append('Barcode_'+str(i)+' : '+str(barcode_data)+'\n')



    # Cмотреть что насканировал
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

#Функция для чтения текста из файла .pdf
def read_text(pdf_path):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                line_text = get_text(element)
                page_text.append(str(line_text).replace('#', ''))
                page_content.append(str(line_text).replace('#', ''))





#Основная функция
def scan_pdf(pdf_path, out_path):
    convert_to_images(pdf_path, out_path)
    read_code(out_path)
    read_text(pdf_path)

    dictionary_key = 'Page'
    text_per_page[dictionary_key] = [page_content]
    # Закрываем объект файла pdf
    pdfFileObj.close()
    # Отображение контента
    result = ''.join(text_per_page['Page'][0])
    # Отображение контента

    return result

#-------ТЕЛО----------------------------------------
if __name__ == '__main__':
    data_from_pdf = scan_pdf(pdf_path, out_path)
    print(data_from_pdf)





