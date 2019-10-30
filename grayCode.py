# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:40:50 2019

@author: roelandd
"""

#%% imports
import numpy as np
from PIL import Image, ImageDraw

#%% function definitions
def generate_binary(n):
    binary = [format(i, "0{}b".format(n)) for i in range(2**n)] # creates binary numbers
    binary = [[int(i)*255 for i in l] for l in binary]
    return np.uint8(binary)


def generate_gray(n):
    gray = [format(i^(i>>1),"0{}b".format(n)) for i in range(2**n)]
    gray = [[int(i)*255 for i in l] for l in gray]
    return np.uint8(gray)    
    
    
def build_grid(seq):
    aspect_ratio = 3 # height / width of 1 bit
    image_width = 100 # in pixels
    W = len(seq[0])
    H = len(seq)
    img = Image.new('L',(W, H), color = color1)
    m = Image.fromarray(seq, mode = 'L')
    img.paste(color2, box = (0,0), mask = m)
    img_large = img.resize((image_width, int(image_width*aspect_ratio)))
    return img_large


def build_wheel(seq):
    inner_diam = 1000
    annulus_radius = 300
    no_bits = len(seq[0])
    angle_inc = 360/(2**no_bits)
    image_size = inner_diam + 2*annulus_radius*no_bits
    img = Image.new('L', (image_size, image_size), color = color1)
    d = ImageDraw.Draw(img)
    for i in range(no_bits-1,-1,-1):
        print(i)
        bounding_box = ((no_bits-i-1)*annulus_radius, (no_bits-i-1)*annulus_radius, inner_diam+(no_bits+i+1)*annulus_radius, inner_diam+(no_bits+i+1)*annulus_radius)
        for j in range(2**no_bits):
            if seq[j][i] == 255:
                d.pieslice(bounding_box, j*angle_inc, (j+1)*angle_inc, fill = color2)
            else:
                d.pieslice(bounding_box,  j*angle_inc, (j+1)*angle_inc, fill = color1)
    d.ellipse((image_size/2-inner_diam/2, image_size/2-inner_diam/2, image_size/2+inner_diam/2, image_size/2+inner_diam/2), fill = color1)
    return img


#%%
color1 = "white"
color2 = "black"
seq_gray = generate_gray(4)
seq_bin = generate_binary(4)
build_grid(seq_gray).save("Gray_grid.png", "PNG")
build_grid(seq_bin).save("Binary_grid.png", "PNG")
build_wheel(seq_bin).save("Binary_wheel.png", "PNG")
build_wheel(seq_gray).save("Gray_wheel.png", "PNG")
