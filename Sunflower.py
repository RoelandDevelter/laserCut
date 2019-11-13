import svgwrite
import numpy as np

drawing = svgwrite.Drawing(filename = "sunflower.svg", size = (1000, 1000))

seeds = 2000
cst = 7
angle = np.pi * 137.5 / 180
center = 500

for n in range(1,seeds+1):
    x = center + cst * np.sqrt(n) * np.cos(n * angle)
    y = center + cst * np.sqrt(n) * np.sin(n * angle)
    drawing.add(drawing.circle(center = (x,y), r =5, fill = 'black'))

drawing.save()