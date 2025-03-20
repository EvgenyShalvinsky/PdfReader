import pytest
from main import convert_to_images, scan_pdf, read_text, read_code, pdf_path, out_path
import os

def test_img_null():
    convert_to_images(pdf_path, out_path)
    assert os.path.getsize(out_path) > 0

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
                 'NOTES': 'inspection notes'}
    real_dict = scan_pdf(pdf_path, out_path)
    assert real_dict == test_dict

