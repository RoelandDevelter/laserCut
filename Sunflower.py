import svgwrite
import numpy as np

for n in range(10):
    cst = 4 + n
    drawing = svgwrite.Drawing(filename = "images/sunflower_{}.svg".format(cst), size = (800, 800))

    seeds = 2000
    angle = np.pi * 137.5 / 180
    center = 500

    for n in range(1,seeds+1):
        x = center + cst * np.sqrt(n) * np.cos(n * angle)
        y = center + cst * np.sqrt(n) * np.sin(n * angle)
        drawing.add(drawing.circle(center = (x,y), r =5, fill = 'black'))

    drawing.save()