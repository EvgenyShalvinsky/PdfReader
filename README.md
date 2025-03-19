# PdfReader
Метод "scan_pdf(pdf_path, out_path)" создан для чтения текста и данных штрих-кодов из файла .pdf и записи в словарь text_per_page[dictionary_key] . 
В качестве переменные pdf_path и out_path, по-этому для корректной работы метода в установленом окружении должна быть папка ".\Data" или изменен путь.
Так же обязательно нужно установить библиотеки : 
$pip3 install opencv-python
$pip3 install fitz
$pip3 install PyPDF2
$pip3 install pdfminer
$pip3 install pyzbar


