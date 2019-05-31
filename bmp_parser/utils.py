def hexint(value, signed=False):
    return int.from_bytes(value, byteorder='little', signed=signed)
