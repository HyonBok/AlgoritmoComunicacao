# Recebe um binário e retorna um vetor com valores em [0, 1, 2]
def mlt3_encode(bin):
    mlt3 = []
    last = 1
    adder = 1
    for bit in bin:
        if bit == '0':
            mlt3.append(last)
        elif bit == '1':
            if (last == 2 or last == 0):
                adder = -adder
            mlt3.append(last + adder)
            last = last + adder
    return mlt3


def mlt3_decode(mlt3):
    bin = []
    last = 1
    for value in mlt3:
        if value == last:
            bin.append(0)
        else:
            bin.append(1)
        last = value

    return ''.join(str(num) for num in bin)
