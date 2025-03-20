import os.path
from main import scan_pdf, pdf_path, out_path


def test_scan():
    test_dict = {'Barcode_1': ' 1',
                 'Barcode_2': ' tst',
                 'COMPANY': 'GRIFFON AVIATION SERVICES LLC',
                 'PN': ' tst',
                 'DESCRIPTION': ' PART',
                 'LOCATION': ' 111',
                 'RECEIVER': ' 9',
                 'EXP DATE': ' 13.04.2022',
                 'CERT SOURCE': ' wef',
                 'SN': ' 123123',
                 'CONDITION': ' FN',
                 'UOM': ' EA',
                 'PO': ' P101',
                 'REC.DATE': ' 18.04.2022',
                 'MFG': ' efwfe',
                 'BATCH': ' 1',
                 'REMARK': '',
                 'TAGGED BY': ' ',
                 'Qty': ' 1',
                 'DOM': ' 13.04.2022',
                 'LOT': ' 1',
                 'NOTES': 'inspection notes'} \
    # Сверяем тестовые данные полученные из test.pdf c эталонным словарем
    assert scan_pdf(pdf_path, out_path) == test_dict
    # проверяем  удаление мусорного файла .png
    assert os.path.exists(out_path) == False

