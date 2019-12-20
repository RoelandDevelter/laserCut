import svgwrite
import numpy as np

angle = np.pi * 137.5 / 180

drawing = svgwrite.Drawing(filename = "images/sunflower_laser.svg", size = (305, 508))

cst = 3.5
center = 125
dot_radius = 2
seeds = 1000

for n in range(4,seeds+1):
    x = center + cst * np.sqrt(n) * np.cos(n * angle)
    y = center + cst * np.sqrt(n) * np.sin(n * angle)
    drawing.add(drawing.circle(center = (x,y), r =dot_radius, fill = 'black'))

max_radius = np.sqrt((x-center)**2 + (y-center)**2) + 1.5 * dot_radius
min_radius = 5
drawing.add(drawing.circle(center = (center, center), r = max_radius, stroke = 'red', fill = 'none'))
drawing.add(drawing.circle(center = (center, center), r = min_radius, stroke = 'red', fill = 'none'))
drawing.save()