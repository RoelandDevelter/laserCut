# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:40:50 2019

@author: roelandd
"""

import numpy as np
from PIL import Image, ImageDraw
import svgwrite
import time


def generate_binary(n):
     # creates binary numbers with 0 and 255 as values
    binary = [format(i, "0{}b".format(n)) for i in range(2**n)]
    binary = [[int(i) for i in l] for l in binary]
    return np.uint8(binary)

def generate_gray(n):
    # creates binary Gray codes with 0 and 255 as values
    gray = [format(i^(i>>1),"0{}b".format(n)) for i in range(2**n)]
    gray = [[int(i) for i in l] for l in gray]
    return np.uint8(gray)    


def grid_png(seq, name = "test"):
    color0 = "white"
    color1 = "black"

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

def wheel_png(seq, name = "test"):
    color0 = "white"
    color1 = "black"

    inner_diam = 1000
    annulus_radius = 300
    no_bits = len(seq[0])
    angle_inc = 360/(2**no_bits)
    image_size = inner_diam + 2*annulus_radius*no_bits
    img = Image.new('RGB', (image_size, image_size), color = color0)
    d = ImageDraw.Draw(img)
    for i in range(no_bits-1,-1,-1):
        bounding_box = ((no_bits-i-1)*annulus_radius, 
                        (no_bits-i-1)*annulus_radius, 
                        inner_diam+(no_bits+i+1)*annulus_radius, 
                        inner_diam+(no_bits+i+1)*annulus_radius)
        for j in range(2**no_bits):
            if seq[j][i] == 255:
                d.pieslice(bounding_box, j*angle_inc, (j+1)*angle_inc, fill = color1)
            else:
                d.pieslice(bounding_box,  j*angle_inc, (j+1)*angle_inc, fill = color0)
    d.ellipse((image_size/2-inner_diam/2, image_size/2-inner_diam/2,
                image_size/2+inner_diam/2, image_size/2+inner_diam/2), fill = color1)
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
                # if color switch has happened -> beginning
                if seq[(j-1)%(no_values), i] != color_val:
                    begin = j               
                # if color switch will happen -> ending
                if (seq[(j+1)%(no_values), i] != color_val) or (seq[(j+1)%(no_values), i] == 0):
                    end = j+1
                    vals.append((i, begin, end))
    return vals

def path_annular_sector(angle_begin, angle_end, 
                        radius_small, radius_large, 
                        center_x, center_y):
    # Draws annular sector with specified dimensions around center
    # Shape is drawn clockwise, with the 4 points being (x_i,y_i), i from 0-3
    # Straight line from p0 to p1, arc to p2, straight line to p3, arc to p0
    # SVG arc: rx ry x-axis-rotation large-arc-flag sweep-flag x y
    (x_0, y_0) = (center_x+np.cos(angle_begin)*radius_small,
                 center_y+np.sin(angle_begin)*radius_small)
    (x_1, y_1) = (center_x+np.cos(angle_begin)*radius_large,
                 center_y+np.sin(angle_begin)*radius_large)
    (x_2, y_2) = (center_x+np.cos(angle_end)*radius_large, 
                center_y+np.sin(angle_end)*radius_large)
    (x_3, y_3) = (center_x+np.cos(angle_end)*radius_small, 
                center_y+np.sin(angle_end)*radius_small)

    # straight line
    path = "M {} {} {} {}".format(x_0, y_0, x_1, y_1)
    # outer arc
    path += "A {},{} 0 0,1 {},{}".format(radius_large, radius_large, x_2, y_2)
    # straight line
    path += "L {} {}".format(x_3, y_3)
    # outer arc
    path += "A {},{} 0 0,0 {},{} z".format(radius_small, radius_small, x_0, y_0)
    return(path)


def create_svg(svg_path, name):
    preamble = '<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="{}px" version="1.1" width="{}px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><path d='
    preamble = preamble.format("1100", "1100")
    postamble = ' fill="black" stroke="red" stroke-width="0" /></svg>'
    svg_path_flat = '"' + "".join(svg_path) + '"'
    with open(name, 'w') as file:
        file.write(preamble)
        file.write(svg_path_flat)
        file.write(postamble)


def path_wheel(seq):
    colors = np.unique(seq)
    no_bits = len(seq[0])
    no_values = len(seq)
    radius_inner = 1000
    radius_sector = 6

    image_size = 2*(no_bits*radius_sector+radius_inner)

    boundaries = []
    for color_val in colors:
        boundaries.append(find_boundaries(seq, color_val))
    
    # sectors per digit
    for i in range(len(colors)):
        color_val = colors[i]
        boundaries_color = boundaries[i]
        color = map_color(color_val) #TODO
        if (color != 'white'):
            paths = []
            # inner circle
            #paths.append("M {} {} A {},{} 0 1,1 {},{} z".format(image_size/2 + radius_inner, image_size/2, radius_inner, radius_inner, image_size/2 - radius_inner, image_size/2))
            #paths.append("M {} {} A {},{} 0 1,1 {},{} z".format(image_size/2 - radius_inner, image_size/2, radius_inner, radius_inner, image_size/2 + radius_inner, image_size/2))
            for sector in boundaries_color:
                radius_small = sector[0]*radius_sector+radius_inner
                radius_large = radius_small + radius_sector
                angle_begin = 2*np.pi*sector[1]/(no_values)
                angle_end = 2*np.pi*(sector[2])/(no_values)
                paths.append(path_annular_sector(angle_begin, angle_end, radius_small, radius_large, image_size/2, image_size/2))
    return paths

def map_color(value):
    if value == 1:
        return "black"
    else:
        return "yellow"



no_bits = 10
seq_bin = generate_binary(no_bits)
seq_gray = generate_gray(no_bits)
p = path_wheel(seq_gray)
create_svg(p, "test.svg")