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
# Библиотека для очистки мусора
import os

# -----НАСТРОЙКИ И ПЕРЕМЕННЫЕ-------------------------------------------
# Пути к файлу для обработки
pdf_path = '.\\Data\\test.pdf'
# Временный файл для чтения штрих-кодов
out_path = '.\\Data\\test.png'
# Создание объекта .pdf файла
pdfFileObj = open(pdf_path, 'rb')
# Анализ и сортировка объектов .pdf файла
pdfRead = PyPDF2.PdfReader(pdfFileObj)
# Словарь для записи контента
content_pdf = {}
# Список с общим контентом
page_content = []


# -----ФУНКЦИИ-------------------------------------------
# Функция для получения текста из .pdf
def get_text(element):
    # Получаем текст из объекта в виде строки
    line_text = element.get_text()
    # Возвращаем текст из объекта
    return line_text


# Функция для поиска баркодов на изображениее
def draw_barcode(decoded, image):
    # Ищем штрих-код 
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top),
                          (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                          color=(0, 255, 0),
                          thickness=5)
    # Возвращаем штрих-код
    return image


# Функция для конвертации .pdf в .png
def convert_to_images(input_file, output_file):
    # Открывает файл
    doc = fitz.open(input_file)
    # Считывает данные из файла
    page = doc.load_page(0)
    # Формирует данные в массив картинки
    pix = page.get_pixmap()
    # Сохраняет новый файл в формате .png
    pix.save(output_file)
    # Закрывает файл
    doc.close()


# Функция для чтения данных из штрих-кода
def read_code(out_path):
    # Считывает .png файл как изображение
    image = cv2.imread(out_path)
    # Находим все штрих-кода на картинке
    detectedBarcodes = decode(image)
    # Создан счетчик штрих-кодов
    i = 0
    # Перебирает все штрих-кода на изображении по очереди
    for barcode in detectedBarcodes:
        # Увеличивает счетчик штрих-кодов
        i = i + 1
        # Определяем положение штрих-кодов
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
        # Считываем данные из штрих-кодов в формате utf-8
        barcode_data = str(barcode.data).replace('\'', '').replace('b', '')
        # Обновляем списки и словари
        page_content.append('Barcode_' + str(i) + ' : ' + str(barcode_data) + '\n')

    # Cмотреть что насканировал
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# Функция для чтения текста из файла .pdf
def read_text(pdf_path):
    #получаем layout 
    for page_layout in extract_pages(pdf_path):
        #получаем element 
        for element in page_layout:
            #отбираем текст из элементов LTTextContainer
            if isinstance(element, LTTextContainer):
                line_text = get_text(element)
                #Заполняем список page_content
                page_content.append(str(line_text).replace('#', ''))


# Основная функция 
def scan_pdf(pdf_path, out_path):
    #Ковертируем .pdf в .png
    convert_to_images(pdf_path, out_path)
    #Записываем штрих-кода из .png в список page_content
    read_code(out_path)
    #Записываем текст из .pdf в список page_content
    read_text(pdf_path)
    #Заполняем словарь content_pdf из списка page_content 
    content_pdf['Barcode_1'] = page_content[0].split(':')[1].replace('\n', '')
    content_pdf['Barcode_2'] = page_content[1].split(':')[1].replace('\n', '')
    content_pdf['COMPANY'] = page_content[2].replace('\n', '')
    content_pdf['PN'] = page_content[3].split(':')[1].replace('\n', '')
    content_pdf['DESCRIPTION'] = page_content[4].split(':')[1].replace('\n', '')
    content_pdf['LOCATION'] = page_content[5].split(':')[1].replace('\n', '')
    content_pdf['RECEIVER'] = page_content[6].split(':')[1].replace('\n', '')
    content_pdf['EXP DATE'] = page_content[7].split(':')[1].replace('\n', '')
    content_pdf['CERT SOURCE'] = page_content[8].split(':')[1].replace('\n', '')
    content_pdf['SN'] = page_content[9].split(':')[1].replace('\n', '')
    content_pdf['CONDITION'] = page_content[10].split(':')[1].replace('\n', '')
    content_pdf['UOM'] = page_content[11].split(':')[1].replace('\n', '')
    content_pdf['PO'] = page_content[12].split(':')[1].replace('\n', '')
    content_pdf['REC.DATE'] = page_content[13].split(':')[1].replace('\n', '')
    content_pdf['MFG'] = page_content[14].split(':')[1].replace('\n', '')
    content_pdf['BATCH'] = page_content[15].split(':')[1].replace('\n', '')
    content_pdf['REMARK'] = page_content[16].split(':')[1].replace('\n', '')
    content_pdf['TAGGED BY'] = page_content[17].split(':')[1].replace('\n', '')
    content_pdf['Qty'] = page_content[18].split(':')[1].replace('\n', '')
    content_pdf['DOM'] = page_content[19].split(':')[1].replace('\n', '')
    content_pdf['LOT'] = page_content[20].split(':')[1].replace('\n', '')
    content_pdf['NOTES'] = page_content[22].replace('\n', '')
    # Закрываем объект файла pdf
    pdfFileObj.close()
    # Удаление мусора
    os.remove(out_path)
    #Проверяем штрих-код LOT
    if content_pdf['Barcode_1'] == content_pdf['LOT']:
        pass
    elif content_pdf['Barcode_1'] != content_pdf['LOT']:
        print(f'НЕ ВЕРНЫЙ LOT ШТРИХКОД')
    else:
        pass
    #Проверяем штрих-код PN    
    if content_pdf['Barcode_2'] == content_pdf['PN']:
        pass
    elif content_pdf['Barcode_2'] == content_pdf['PN']:
        print(f'НЕ ВЕРНЫЙ PN ШТРИХКОД')
    else:
        pass

    return content_pdf


# -------ТЕЛО----------------------------------------
if __name__ == '__main__':
    #Выводим словарь на экран
    print(scan_pdf(pdf_path, out_path))
