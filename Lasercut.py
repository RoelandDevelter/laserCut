import numpy as np
import time

"""
things tried:   np.vectorize(lambda number: format(number, 'b').zfill(n), numbers)
                [bin(number) for number in numbers] -> not zero padded
                [format(number, 'b').zfill(n) for number in numbers] -> zero padded
                [np.binary_repr(number) for number in numbers]
"""


def timer(func):
    """A decorator that prints how long a function took to run."""
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_total = time.time() - t_start
        print('{} took {}s'.format(func.__name__, t_total))
        return result
    return wrapper

@timer
def generate_code(no_bits, type = 'natural'):
    """ Generates binary codes (i.e. counts through different bit representations). Lucal code does not add a different pattern

    Parameters
    ----------
    no_bits : int
        Number of bits the code should be.
    type : str, optional
        The type of code generated. Possible parameters: natural, gray
        Default=natural.

    Returns
    -------
    numpy array of the code
    """
    if type == 'natural':
        code = [list(format(number, 'b').zfill(no_bits)) for number in range(2**no_bits)]
    elif type == 'gray':
        code = [list(format(number ^ (number >> 1), 'b').zfill(no_bits)) for number in range(2**no_bits)]
    return np.array(code).astype(bool)

def detect_edges(code):
    """ Detects edges on given code. 

    Parameters
    ----------
    code: 2D-numpy array
        Code to detect edges on

    Returns
    -------
    edge_r, edge_theta: 2D-numpy arrays, edge_theta same size as code, edge_r 1 column more
        The r- and theta-direction edges.
    """
    no_values, no_bits = np.shape(code)
    # axis 0 == 'theta-direction', axis 1 == 'r-direction'
    edge_theta = np.logical_xor(code, np.roll(code, 1, axis = 0))

    # for r-direction, add zero row in beginning ("inner empty circle") and at the end ("outer empty circle") and xor this
    # this gives an extra column to the edge data 
    code1 = np.zeros((no_values, no_bits+1))
    code1[:,:-1] = code
    code2 = np.zeros((no_values, no_bits+1))
    code2[:,1:] = code

    edge_r = np.logical_xor(code1, code2)
    
    # create coordinate matrix
    mat = np.ones((no_values, no_bits+1,2))
    mat[:,:,1] = np.arange(no_values).reshape(no_values,1)
    mat[:,:,0] = np.arange(no_bits+1)

    edge_r = mat[edge_r] 
    edge_theta = mat[:,:no_bits][edge_theta]

    return edge_r, edge_theta


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
    code = generate_code(5, type = 'natural')
    edge_r, edge_theta = detect_edges(code)
    print('breakpoint')


if __name__ == "__main__":
    main()