# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from matplotlib.pyplot import imshow

def generateBinary(n):
    binary = [format(i, "0{}b".format(n)) for i in range(2**n)] # creates binary numbers
    binary = [[int(i)*255 for i in l] for l in binary]
    return np.uint8(binary)


def generateGray(n):
    gray = [format(i^(i>>1),"0{}b".format(n)) for i in range(2**n)]
    gray = [[int(i)*255 for i in l] for l in gray]
    return np.uint8(gray)    
    
    
def buildGrid(seq):
    boxH = 10 # height in pixels
    boxW = 20 # width in pixels
    W = len(seq[0])
    H = len(seq)
    img = Image.new('L',(W, H), color = "black")
    m = Image.fromarray(seq, mode = 'L')
    img.paste(255, box = (0,0), mask = m)
    img_large = img.resize((W*boxW, H*boxH))
    return img_large

seq = generateGray(5)
seq2 = generateBinary(5)
img = buildGrid(seq2)
imshow(np.asarray(img))
