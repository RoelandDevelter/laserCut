import numpy as np

# things tried: np.vectorize(lambda number: format(number, 'b').zfill(n), numbers)
# [bin(number) for number in numbers] -> not zero padded
# [format(number, 'b').zfill(n) for number in numbers] -> zero padded
# [np.binary_repr(number) for number in numbers]


def generate_code(no_bits, type = 'natural'):
    # generates codes. Lucal code does not add a different pattern
    if type == 'natural':
        code = [list(format(number, 'b').zfill(no_bits)) for number in range(2**no_bits)]
    elif type == 'gray':
        code = [list(format(number ^ (number >> 1), 'b').zfill(no_bits)) for number in range(2**no_bits)]
    return np.array(code) == '1'   # convert to boolean array


def detect_edges(code):
    # axis 0 == 'vertical', axis 1 == 'horizontal'
    # returns edge_x, edge_y
    edge_x = np.logical_xor(code, np.roll(code, 1, axis = 1))
    edge_y = np.logical_xor(code, np.roll(code, 1, axis = 0))
    # return coordinates
    return edge_x, edge_y


def main():
    # print(timeit.timeit("generate_gray_np(8)", setup="from __main__ import generate_gray_np", number = 20))
    # print(timeit.timeit("generate_gray(8)", setup = "from __main__ import generate_gray", number = 20))
    code = generate_code(5)
    edge_x, edge_y = detect_edges(code)


if __name__ == "__main__":
    main()
