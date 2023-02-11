from enum import IntEnum

class A(IntEnum):
    EVEN = 0,
    ODD  = 1,
    NEGATIV  = 2

def get_even():
    n = int(input())
    if n < 0:
        return A.NEGATIV
    elif n % 2 == 1:
        return A.ODD
    elif n % 2 == 0:
        print(f'yes, {n} is even')
        return A.EVEN

while get_even():
    pass