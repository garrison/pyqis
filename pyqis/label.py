def binary_str(i, nbits):
    # NOTE: bin() was introduced with python 2.6
    return bin(i)[2:].rjust(nbits, '0')

def create_label(i, nqubits, format_string=None):
    if format_string is None:
        format_string = "{i} ({b})"
    return format_string.format(i=i, b=binary_str(i, nqubits))
