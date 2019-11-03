import svgwrite
import numpy as np
import GrayCode


x_max = 800
y_max = 600
x_mid = x_max/2
y_mid = y_max/2


def pathAnnularSector(angle_begin, angle_end, radius_small, radius_large, center_x, center_y):
    # Draws annular sector with specified dimensions around center
    # Shape is drawn clockwise, with the 4 points being (x_i,y_i), i from 0-3
    # Straight line from p0 to p1, arc to p2, straight line to p3, arc to p0
    # SVG arc: rx ry x-axis-rotation large-arc-flag sweep-flag x y
    (x_0, y_0) = (center_x+np.cos(angle_begin)*radius_small, center_y+np.sin(angle_begin)*radius_small)
    (x_1, y_1) = (center_x+np.cos(angle_begin)*radius_large, center_y+np.sin(angle_begin)*radius_large)
    (x_2, y_2) = (center_x+np.cos(angle_end)*radius_large, center_y+np.sin(angle_end)*radius_large)
    (x_3, y_3) = (center_x+np.cos(angle_end)*radius_small, center_y+np.sin(angle_end)*radius_small)

    path = "M {} {} {} {}".format(x_0, y_0, x_1, y_1) # straight line
    path += "A {},{} 0 0,1 {},{}".format(radius_large, radius_large, x_2, y_2) # outer arc
    path += "L {} {}".format(x_3, y_3) # straight line
    path += "A {},{} 0 0,0 {},{} z".format(radius_small, radius_small, x_0, y_0) # outer arc
    return(path)


def createSVG(base, no_bits, name):
    seq = GrayCode.generate_binary(no_bits)
    boundaries = GrayCode.find_boundaries(seq, 255)

    radius_inner = 100
    radius_sector = 30
    image_size = 2*(no_bits*radius_sector+radius_inner)
    no_values = base**no_bits
    paths = []

    for sector in boundaries:
        radius_small = sector[0]*radius_sector+radius_inner
        radius_large = radius_small + radius_sector
        angle_begin = 2*np.pi*sector[1]/(no_values)
        angle_end = 2*np.pi*(sector[2])/(no_values)
        paths.append(pathAnnularSector(angle_begin, angle_end, radius_small, radius_large, image_size/2, image_size/2))
    
    svg_document = svgwrite.Drawing(filename = name,size = (image_size, image_size))
    svg_document.add(svg_document.path(paths, fill=color, stroke="red", stroke_width="0"))
    svg_document.add(svg_document.circle(center = (image_size/2, image_size/2), r = radius_inner, fill = color, stroke = color, stroke_width="0.1"))
    
    svg_document.save()


no_bits = 8
color = "green"
createSVG(2, no_bits, "testSVG2.svg")