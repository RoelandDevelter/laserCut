import numpy as np
import timeit


# things tried: np.vectorize(lambda number: format(number, 'b').zfill(n), numbers)
# [bin(number) for number in numbers] -> not zero padded
# [format(number, 'b').zfill(n) for number in numbers] -> zero padded
# [np.binary_repr(number) for number in numbers]


def generate_binary(n):
    # creates standard binary numbers
    return [format(number, 'b').zfill(n) for number in range(0, 2**n, 1)]


def generate_gray(n):
    # creates gray binary numbers
    return [format(number ^ (number >> 1), 'b').zfill(n) for number in range(0, 2**n, 1)]


def main():
    # print(timeit.timeit("generate_gray_np(8)", setup="from __main__ import generate_gray_np", number = 20))
    # print(timeit.timeit("generate_gray(8)", setup = "from __main__ import generate_gray", number = 20))
    code = np.array(generate_gray(3))
    print(*code)
    edge_x = np.logical_xor(code, np.roll(code, 1, axis = 0)) # axis 0 == 'vertical'
    edge_y = np.logical_xor(code, np.roll(code, 1, axis = 1)) # axis 1 == 'horizontal'
    print(edge_x)

if __name__ == "__main__":
    main()
