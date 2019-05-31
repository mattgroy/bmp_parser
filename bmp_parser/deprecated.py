# BM_FILE_HEADER = {
#     'type': {
#         'start': 0,
#         'length': 2
#     },
#     'size': {
#         'start': 2,
#         'length': 4
#     },
#     'offbits': {
#         'start': 10,
#         'length': 4
#     },
# }
#
# BM_INFO_HEADER = {
#     'width': {
#         'start': 4,
#         'length': 4
#     },
#     'height': {
#         'start': 8,
#         'length': 4
#     },
#     # not important, always 1
#     'planes': {
#         'start': 12,
#         'length': 2
#     },
#     'bitcount': {
#         'start': 14,
#         'length': 2
#     },
#     'compression': {
#         'start': 16,
#         'length': 4
#     },
#     'sizeimage': {
#         'start': 20,
#         'length': 4
#     },
#     'xppm': {
#         'start': 24,
#         'length': 4
#     },
#     'yppm': {
#         'start': 28,
#         'length': 4
#     },
#     'clrused': {
#         'start': 32,
#         'length': 4
#     },
#     'clrimportant': {
#         'start': 36,
#         'length': 4
#     }
# }
#
# BM_V4_HEADER = {
#     **BM_INFO_HEADER,
#     'redmask': {
#         'start': 40,
#         'length': 4
#     },
#     'greenmask': {
#         'start': 44,
#         'length': 4
#     },
#     'bluemask': {
#         'start': 48,
#         'length': 4
#     },
#     'alphamask': {
#         'start': 52,
#         'length': 4
#     },
#     'cstype': {
#         'start': 56,
#         'length': 4
#     },
#     'endpoints': {
#         'start': 60,
#         'length': 36
#     },
#     'gammared': {
#         'start': 96,
#         'length': 4
#     },
#     'gammagreen': {
#         'start': 100,
#         'length': 4
#     },
#     'gammablue': {
#         'start': 104,
#         'length': 4
#     }
# }
#
# BM_V5_HEADER = {
#     **BM_V4_HEADER,
#     'intent': {
#         'start': 108,
#         'length': 4
#     },
#     'profiledata': {
#         'start': 112,
#         'length': 4
#     },
#     'profilesize': {
#         'start': 116,
#         'length': 4
#     },
#     'reserved': {
#         'start': 120,
#         'length': 4
#     }
# }
#
# BM_INFO = {
#     12: {
#         'name': 'BITMAPCOREHEADER',
#         'width': {
#             'start': 4,
#             'length': 2
#         },
#         'height': {
#             'start': 6,
#             'length': 2
#         },
#         # not important, always 1
#         'planes': {
#             'start': 8,
#             'length': 2
#         },
#         'bitcount': {
#             'start': 10,
#             'length': 2
#         }
#     },
#     40: {
#         **BM_INFO_HEADER,
#         'name': 'BITMAPINFOHEADER'
#     },
#     108: {
#         **BM_V4_HEADER,
#         'name': 'BITMAPV4HEADER'
#     },
#     124: {
#         **BM_V5_HEADER,
#         'name': 'BITMAPV5HEADER'
#     }
# }
#
#
#
# file_header = file.read(14)
#         if file_header[:BM_FILE_HEADER['type']['length']] != b'BM':
#             raise BMPException("File type is not BMP")
#         self.size = hexint(file_header[
#                            BM_FILE_HEADER['size']['start']:
#                            BM_FILE_HEADER['size']['length']])
#         a = file_header[BM_FILE_HEADER['offbits']['start']:BM_FILE_HEADER['offbits']['start']+4]
#         b = BM_FILE_HEADER['offbits']['length']
#         self.offbits = hexint(file_header[
#                               BM_FILE_HEADER['offbits']['start']:
#                               BM_FILE_HEADER['offbits']['length']])
#
#         p = file.tell()
#         ver = hexint(file.read(4))
#         if ver not in BM_INFO:
#             raise BMPException("Unsupported BITMAPINFO version")
#         bmi = BM_INFO[ver]
#         file.seek(p-1)
#         info = file.read(ver)
#         self.i_size = ver
#         self.i_ver = bmi['name']
#         core = ver == 12
#
#         self.i_width = hexint(
#             info[bmi['width']['start']:bmi['width']['length']],
#             signed=not core)
#
#         self.i_height = hexint(
#             info[bmi['height']['start']:bmi['height']['length']],
#             signed=not core)
#
#         self.i_bitcount = hexint(
#             info[bmi['bitcount']['start']:bmi['bitcount']['length']])
#
#         if not core:
#             self.i_compression = hexint(
#                 info[bmi['compression']['start']:bmi['compression']['length']])
#
#             self.i_sizeimage = hexint(
#                 info[bmi['sizeimage']['start']:bmi['sizeimage']['length']])
#
#             self.i_xppm = hexint(
#                 info[bmi['xppm']['start']:bmi['xppm']['length']],
#                 signed=True)
#
#             self.i_yppm = hexint(
#                 info[bmi['yppm']['start']:bmi['yppm']['length']],
#                 signed=True)
#
#             self.i_clrused = hexint(
#                 info[bmi['clrused']['start']:bmi['clrused']['length']])
#
#             self.i_clrimportant = hexint(
#                 info[bmi['clrimportant']['start']:
#                      bmi['clrimportant']['length']])
#
#             if ver != 40:
#                 self.i_redmask = hexint(
#                     info[bmi['redmask']['start']:bmi['redmask']['length']])
#
#                 self.i_greenmask = hexint(
#                     info[bmi['greenmask']['start']:bmi['greenmask']['length']])
#
#                 self.i_bluemask = hexint(
#                     info[bmi['bluemask']['start']:bmi['bluemask']['length']])
#
#                 self.i_alphamask = hexint(
#                     info[bmi['alphamask']['start']:bmi['alphamask']['length']])
#
#                 self.i_cstype = hexint(
#                     info[bmi['cstype']['start']:bmi['cstype']['length']])
#
#                 self.i_endpoints = hexint(
#                     info[bmi['endpoints']['start']:bmi['endpoints']['length']])
#
#                 self.i_gammared = hexint(
#                     info[bmi['gammared']['start']:bmi['gammared']['length']])
#
#                 self.i_gammagreen = hexint(
#                     info[bmi['gammagreen']['start']:
#                          bmi['gammagreen']['length']])
#
#                 self.i_gammablue = hexint(
#                     info[bmi['gammablue']['start']:bmi['gammablue']['length']])
#
#                 if ver != 108:
#                     self.i_intent = hexint(
#                         info[bmi['intent']['start']:bmi['intent']['length']])
#
#                     self.i_profiledata = hexint(
#                         info[bmi['profiledata']['start']:
#                              bmi['profiledata']['length']])
#
#                     self.i_profilesize = hexint(
#                         info[bmi['profilesize']['start']:
#                              bmi['profilesize']['length']])
