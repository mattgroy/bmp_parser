import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

_test_dir = os.path.dirname(os.path.abspath(__file__))

import bmp_parser as bm


def test_wrong_file():
    parser = bm.BMPParser()
    with pytest.raises(bm.BMPException):
        with open('tests/1.jpg', 'rb') as file:
            parser.parse(file)


def test_fileheader():
    parser = bm.BMPParser()
    with open('tests/1.bmp', 'rb') as file:
        parser._extract_file_header(file)
    assert parser.size == 32886 and parser.offbits == 118


def test_fileheader2():
    parser = bm.BMPParser()
    with open('tests/2.bmp', 'rb') as file:
        parser._extract_file_header(file)
    assert parser.size == 787512 and parser.offbits == 1078


def test_infoheader():
    parser = bm.BMPParser()
    with open('tests/1.bmp', 'rb') as file:
        parser._extract_file_header(file)
        parser._extract_info_header(file)
    assert parser.i_width == parser.i_height == 256 and \
           parser.i_bitcount == 4 and parser.i_size == 40


def test_infoheader2():
    parser = bm.BMPParser()
    with open('tests/2.bmp', 'rb') as file:
        parser._extract_file_header(file)
        parser._extract_info_header(file)
    assert parser.i_width == 1024 and parser.i_height == 768 and \
           parser.i_bitcount == 8 and parser.i_size == 40


def test_clrtable():
    parser = bm.BMPParser()
    with open('tests/1.bmp', 'rb') as file:
        parser._extract_file_header(file)
        parser._extract_info_header(file)
        parser._extract_clrtable(file)

    expected = [(0, 0, 0, 0), (0, 0, 128, 0), (0, 128, 0, 0),
                (0, 128, 128, 0), (128, 0, 0, 0), (128, 0, 128, 0),
                (128, 128, 0, 0), (128, 128, 128, 0), (192, 192, 192, 0),
                (0, 0, 255, 0), (0, 255, 0, 0), (0, 255, 255, 0),
                (255, 0, 0, 0), (255, 0, 255, 0), (255, 255, 0, 0),
                (255, 255, 255, 0)]

    assert parser.i_clrtable == expected


def test_v5():
    parser = bm.BMPParser()
    with open('tests/pal8v5.bmp', 'rb') as file:
        parser.parse(file)
    assert parser.size == 9338 and parser.offbits == 1146 and \
           parser.i_width == 127 and parser.i_height == 64 and \
           parser.i_bitcount == 8 and parser.i_size == 124 and \
           parser.i_compression == 0 and parser.i_sizeimage == 8192 and \
           parser.i_xppm == parser.i_yppm == 2835 and \
           parser.i_clrused == len(parser.i_clrtable) == 252 and \
           parser.i_clrtable_cellsize == 4


def test_rgb16():
    parser = bm.BMPParser()
    with open('tests/rgb16-565.bmp', 'rb') as file:
        parser.parse(file)
    assert parser.size == 16450 and parser.offbits == 66 and \
           parser.i_width == 127 and parser.i_height == 64 and \
           parser.i_bitcount == 16 and parser.i_size == 40 and \
           parser.i_compression == 3 and parser.i_sizeimage == 16384
