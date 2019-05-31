from .bmp_constants import BM_FILE_HEADER, BM_INFO, COMPRESSION
from .bmp_exceptions import *
from .utils import hexint


class BMPParser:
    def __init__(self):
        self.size = 0
        self.offbits = 0
        self.i_size = 0
        self.i_ver = ''
        self.core = 0
        self.i_width = 0
        self.i_height = 0
        self.i_planes = 0
        self.i_bitcount = 0
        self.i_sizeimage = 0
        self.i_clrtable = []
        self.i_clrtable_cellsize = 0
        self.i_redmask = 0
        self.i_greenmask = 0
        self.i_bluemask = 0
        self.i_alphamask = 0

    def parse(self, file):
        self._extract_file_header(file)
        self._extract_info_header(file)
        self._extract_clrtable(file)
        self._extract_gap(file)

        # pixeldata
        if self.i_sizeimage == 0:
            if not self.core and self.i_compression not in {0, 3, 6}:
                raise BMPException(
                    "Pixel data size should be explicitly stated")
            else:
                self.i_sizeimage = int(
                    self.i_width * self.i_height / 8 * self.i_bitcount)
        self.pixeldata = file.read(self.i_sizeimage)

    def _extract_file_header(self, file):
        if file.read(BM_FILE_HEADER['type']) != b'BM':
            raise BMPException("File type is not BMP")
        self.size = hexint(file.read(BM_FILE_HEADER['size']))
        file.read(BM_FILE_HEADER['reserved'])
        self.offbits = hexint(file.read(BM_FILE_HEADER['offbits']))

    def _extract_info_header(self, file):
        ver = hexint(file.read(4))
        if ver not in BM_INFO:
            raise BMPException("Unsupported BITMAPINFO version")
        bmi = BM_INFO[ver]
        self.i_size = ver
        self.i_ver = bmi['name']
        self.core = ver == 12
        self.i_width = hexint(file.read(bmi['width']), signed=not self.core)
        self.i_height = hexint(file.read(bmi['height']), signed=not self.core)
        self.i_planes = hexint(file.read(bmi['planes']))
        self.i_bitcount = hexint(file.read(bmi['bitcount']))
        if not self.core:
            self.i_compression = hexint(file.read(bmi['compression']))
            self.i_sizeimage = hexint(file.read(bmi['sizeimage']))
            self.i_xppm = hexint(file.read(bmi['xppm']), signed=True)
            self.i_yppm = hexint(file.read(bmi['yppm']), signed=True)
            self.i_clrused = hexint(file.read(bmi['clrused']))
            self.i_clrimportant = hexint(file.read(bmi['clrimportant']))

            if ver != 40:
                self.i_redmask = hexint(file.read(bmi['redmask']))
                self.i_greenmask = hexint(file.read(bmi['greenmask']))
                self.i_bluemask = hexint(file.read(bmi['bluemask']))
                self.i_alphamask = hexint(file.read(bmi['alphamask']))
                self.i_cstype = hexint(file.read(bmi['cstype']))
                self.i_endpoints = hexint(file.read(bmi['endpoints']))
                self.i_gammared = hexint(file.read(bmi['gammared']))
                self.i_gammagreen = hexint(file.read(bmi['gammagreen']))
                self.i_gammablue = hexint(file.read(bmi['gammablue']))

                if ver != 108:
                    self.i_intent = hexint(file.read(bmi['intent']))
                    self.i_profiledata = hexint(file.read(bmi['profiledata']))
                    self.i_profilesize = hexint(file.read(bmi['profilesize']))
                    file.read(bmi['reserved'])
            else:
                if self.i_bitcount in {16, 32}:
                    if self.i_compression in {3, 6}:
                        self.i_redmask = hexint(file.read(4))
                        self.i_greenmask = hexint(file.read(4))
                        self.i_bluemask = hexint(file.read(4))
                        if self.i_compression == 6:
                            self.i_alphamask = hexint(file.read(4))

    def _extract_clrtable(self, file):
        if self.i_bitcount <= 8:
            if self.core or self.i_clrused == 0:
                clrtable_len = 2 ** self.i_bitcount
            else:
                clrtable_len = self.i_clrused
        else:
            clrtable_len = self.i_clrused
        if clrtable_len:
            self.i_clrtable_cellsize = 3 if self.core else 4
            for i in range(clrtable_len):
                self.i_clrtable.append(
                    tuple(file.read(self.i_clrtable_cellsize)))

    def _extract_gap(self, file):
        gap = self.offbits - 14 - self.i_size - \
              len(self.i_clrtable) * self.i_clrtable_cellsize
        file.read(gap)

    def __iter__(self):
        yield 'File size: ', '{} bytes'.format(self.size)
        yield 'Info header version: ', self.i_ver
        yield 'Width: ', '{} bytes'.format(self.i_width)
        yield 'Height: ', '{} bytes'.format(self.i_height)
        yield 'Bitcount: ', self.i_bitcount
        yield 'Image size: ', '{} bytes'.format(self.i_sizeimage)

        if not self.core:
            yield 'Compression type: ', '{} ({})'.format(
                COMPRESSION[self.i_compression], self.i_compression)
            yield 'Pixels per meter (X): ', self.i_xppm
            yield 'Pixels per meter (Y): ', self.i_yppm
            yield 'Colour table size: ', len(self.i_clrtable)
            yield 'Important colours in colour table', self.i_clrimportant
            if self.i_redmask:
                yield 'Red mask: ', '0x{:08x}'.format(self.i_redmask)
            if self.i_greenmask:
                yield 'Green mask: ', '0x{:08x}'.format(self.i_greenmask)
            if self.i_bluemask:
                yield 'Blue mask: ', '0x{:08x}'.format(self.i_bluemask)
            if self.i_alphamask:
                yield 'Alpha mask: ', '0x{:08x}'.format(self.i_alphamask)

            if self.i_size != 40:
                yield 'Colour space type: ', self.i_cstype

                if self.i_size != 108:
                    yield 'Intent: ', self.i_intent
                    yield 'Profile data: ', self.i_profiledata
                    yield 'Profile size: ', self.i_profilesize

        if self.i_clrtable:
            yield 'Colour table: ', self.i_clrtable
