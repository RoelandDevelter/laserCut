# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:40:50 2019

@author: roelandd
"""

#%% imports
import numpy as np
from PIL import Image, ImageDraw
import svgwrite

#%% function definitions
def generate_binary(n):
     # creates binary numbers with 0 and 255 as values
    binary = [format(i, "0{}b".format(n)) for i in range(2**n)]
    binary = [[int(i)*255 for i in l] for l in binary]
    return np.uint8(binary)


def generate_gray(n):
    # creates binary Gray codes with 0 and 255 as values
    gray = [format(i^(i>>1),"0{}b".format(n)) for i in range(2**n)]
    gray = [[int(i)*255 for i in l] for l in gray]
    return np.uint8(gray)    
    
    
def build_grid(seq, name = "test"):
    image_height = 800   
    image_width = 200 # in pixels
    W = len(seq[0])
    H = len(seq)
    img = Image.new('L',(W, H), color = color0)
    m = Image.fromarray(seq, mode = 'L')
    img.paste(color1, box = (0,0), mask = m)
    img_large = img.resize((image_width, image_height))
    img_large.save("{}_grid_{}.png".format(name, len(seq[0])), "PNG")
    return img_large


def build_wheel(seq, name = "test"):
    inner_diam = 1000
    annulus_radius = 300
    no_bits = len(seq[0])
    angle_inc = 360/(2**no_bits)
    image_size = inner_diam + 2*annulus_radius*no_bits
    img = Image.new('RGB', (image_size, image_size), color = color0)
    d = ImageDraw.Draw(img)
    for i in range(no_bits-1,-1,-1):
        bounding_box = ((no_bits-i-1)*annulus_radius, (no_bits-i-1)*annulus_radius, inner_diam+(no_bits+i+1)*annulus_radius, inner_diam+(no_bits+i+1)*annulus_radius)
        for j in range(2**no_bits):
            if seq[j][i] == 255:
                d.pieslice(bounding_box, j*angle_inc, (j+1)*angle_inc, fill = color1)
            else:
                d.pieslice(bounding_box,  j*angle_inc, (j+1)*angle_inc, fill = color0)
    d.ellipse((image_size/2-inner_diam/2, image_size/2-inner_diam/2, image_size/2+inner_diam/2, image_size/2+inner_diam/2), fill = color1)
    img.save("{}_wheel_{}.png".format(name,no_bits), "PNG")
    return img


def find_boundaries(seq, color_val):
    vals = []
    no_values = len(seq)
    no_bits = len(seq[0])
    for i in range(no_bits):
        begin = 0
        end = 0
        for j in range(no_values):
            if seq[j,i] == color_val:
                if seq[(j-1)%(no_values), i] != color_val:
                    begin = j
                if seq[(j+1)%(no_values), i] != 255:
                    end = j+1
                    vals.append((i, begin, end))
    return vals


def remap(img, cmap):
    # converts single values to color values
    return


#%%
no_bits = 8
color0 = "white"
color1 = "black"
seq_gray = generate_gray(no_bits)
seq_bin = generate_binary(no_bits)

build_wheel(seq_bin, "8bitBW.png")
