# Recebe um binário e retorna um vetor com valores em [-1, 0, 1]
def mlt3_encode(bin):
    mlt3 = []
    last = 0
    adder = 1
    for bit in bin:
        if bit == 0:
            mlt3.append(last)
        else:
            if (last == 1 or last == -1):
                adder = -adder
            mlt3.append(last + adder)
            last = last + adder
    return mlt3


def mlt3_decode(mlt3):
    bin = []
    last = 0
    for value in mlt3:
        if value == last:
            bin.append(0)
        else:
            bin.append(1)
        last = value
    return bin

mlt3 = mlt3_encode([1,1,0,1,0,0,1,1])
bin = mlt3_decode(mlt3)

print(mlt3)
print(bin)