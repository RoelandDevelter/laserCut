import numpy as np
import timeit


def generate_binary(n):
    # creates standard binary numbers
    return [np.binary_repr(num).zfill(n) for num in  np.arange(2**n)]


def generate_gray(n):
    # creates gray binary numbers
    numbers = np.arange(2**n)
    return [np.binary_repr(num).zfill(n) for num in numbers ^ (numbers >> 1)]


def main():
    # print(timeit.timeit("generate_gray_np(8)", setup="from __main__ import generate_gray_np", number = 20))
    # print(timeit.timeit("generate_gray(8)", setup = "from __main__ import generate_gray", number = 20))
    code = np.array(generate_gray_np(3))
    print(*code)
    edge_x = np.logical_xor(code, np.roll(code, 1, axis = 0)) # axis 0 == 'vertical'
    edge_y = np.logical_xor(code, np.roll(code, 1, axis = 1)) # axis 1 == 'horizontal'
    print(edge_x)

if __name__ == "__main__":
    main()
