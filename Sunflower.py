import svgwrite
import numpy as np

drawing = svgwrite.Drawing(filename = "sunflower.svg", size = (500, 500))

seeds = 1000
cst = 3.3
angle = np.pi * 137.5 / 180
center = 250

for n in range(1,seeds+1):
    x = center + cst * np.sqrt(n) * np.cos(n * angle)
    y = center + cst * np.sqrt(n) * np.sin(n * angle)
    drawing.add(drawing.circle(center = (x,y), r =2, fill = 'black'))

drawing.save()