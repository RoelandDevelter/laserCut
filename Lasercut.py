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
    x, y = np.shape(code)
    edge_x = np.logical_xor(code, np.roll(code, 1, axis = 1))
    edge_x = (np.ones((x,y)) * np.arange(y))[edge_x]
    print(edge_x)
    edge_y = np.logical_xor(code, np.roll(code, 1, axis = 0))
    edge_y = (np.ones((x,y)) * np.arange(y))[edge_y]
    # return coordinates
    return edge_x, edge_y


def find_boundaries(seq, color_val = 1):
    vals = []
    no_values = len(seq)
    no_bits = len(seq[0])
    for i in range(no_bits):
        begin = 0
        end = 0
        for j in range(no_values):
            if seq[j,i] == color_val:
                # if color switch has happened -> beginning
                if seq[(j-1)%(no_values), i] != color_val:
                    begin = j               
                # if color switch will happen -> ending
                if (seq[(j+1)%(no_values), i] != color_val) or (seq[(j+1)%(no_values), i] == 0):
                    end = j+1
                    vals.append((i, begin, end))
    return vals


def make_path(edge_x, edge_y):
    pass


def write_img(svg_path):
    preamble = '<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="{}px" version="1.1" width="{}px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><path d='
    preamble = preamble.format("1100", "1100")
    postamble = ' fill="black" stroke="red" stroke-width="1 /></svg>'
    svg_path_flat = '"' + "".join(svg_path) + '"'
    with open('test.svg', 'w') as file:
        file.write(preamble)
        file.write(svg_path_flat)
        file.write(postamble)



def main():
    # print(timeit.timeit("generate_gray_np(8)", setup="from __main__ import generate_gray_np", number = 20))
    # print(timeit.timeit("generate_gray(8)", setup = "from __main__ import generate_gray", number = 20))
    code = generate_code(2, type = 'natural')
    code_manual = np.array([[False, False, False, False, False], [True, True,True,True,True], [False, False, False, False, False]])
    edge_x, edge_y = detect_edges(code_manual)
    vals = find_boundaries(code_manual)
    print(code_manual)
    print(vals)
    print(edge_x)
    print(edge_y)


if __name__ == "__main__":
    main()
