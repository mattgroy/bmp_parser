BM_FILE_HEADER = {
    'type': 2,
    'size': 4,
    'reserved': 4,
    'offbits': 4
}

BM_INFO_HEADER = {
    'width': 4,
    'height': 4,
    # not important, always 1
    'planes': 2,
    'bitcount': 2,
    'compression': 4,
    'sizeimage': 4,
    'xppm': 4,
    'yppm': 4,
    'clrused': 4,
    'clrimportant': 4
}

BM_V4_HEADER = {
    **BM_INFO_HEADER,
    'redmask': 4,
    'greenmask': 4,
    'bluemask': 4,
    'alphamask': 4,
    'cstype': 4,
    'endpoints': 36,
    'gammared': 4,
    'gammagreen': 4,
    'gammablue': 4
}

BM_V5_HEADER = {
    **BM_V4_HEADER,
    'intent': 4,
    'profiledata': 4,
    'profilesize': 4,
    'reserved': 4
}

BM_INFO = {
    12: {
        'name': 'BITMAPCOREHEADER',
        'width': 2,
        'height': 2,
        # not important, always 1
        'planes': 2,
        'bitcount': 2
    },
    40: {
        **BM_INFO_HEADER,
        'name': 'BITMAPINFOHEADER'
    },
    108: {
        **BM_V4_HEADER,
        'name': 'BITMAPV4HEADER'
    },
    124: {
        **BM_V5_HEADER,
        'name': 'BITMAPV5HEADER'
    }
}

COMPRESSION = {
    0: 'BI_RGB',
    1: 'BI_RLE8',
    2: 'BI_RLE4',
    3: 'BI_BITFIELDS',
    4: 'BI_JPEG',
    5: 'BI_PNG',
    6: 'BI_ALPHABITFIELDS'
}
