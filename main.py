from ray import *
from scene import *
from shapes import *
import numpy as np

color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)

scene = Scene(ambient=0.05)
scene.add_object(Sphere(centre=[.75, .1, 1.],
                        radius=.6,
                        colour=[0., 0., 1.],
                        diffuse_c=1.0,
                        specular_c=1.0,
                        specular_k=50,
                        reflection=0.5))

scene.add_object(Sphere(centre=[-.75, .1, 2.25],
                        radius=.6,
                        colour=[0.5, 0.223, 0.5],
                        diffuse_c=1.0,
                        specular_c=1.0,
                        specular_k=50,
                        reflection=0.5))


scene.add_object(Sphere(centre=[.75, .1, 1.],
                        radius=.6,
                        colour=[0., 0., 1.],
                        diffuse_c=1.0,
                        specular_c=1.0,
                        specular_k=50,
                        reflection=0.5))

scene.add_object(Sphere(centre=[-2.75, 0.1, 3.5],
                        radius=0.6,
                        colour=[1.0, 0.572, 0.184],
                        diffuse_c=1.0,
                        specular_c=1.0,
                        specular_k=50,
                        reflection=0.5))


scene.add_object(Plane(p = [0.0, -0.5, 0.0],
                       n = [0.0, 1.0, 0.0],
                       colour_plane_0 = [1.0, 1.0, 1.0],
                       colour_plane_1= [0.0, 0.0, 0.0],
                       diffuse_c=0.75,
                       specular_c=0.5,
                       specular_k=50,
                       reflection=0.25))


scene.add_light_source(Light_Source(position=[5.0, 5.0, -10.0], colour=[1.0,1.0,1.0]))

h, w = 300, 400
depth_max = 5

O = np.array([0., 0.35, -1.])  # Camera.


img = np.zeros(shape=(h, w, 3))

r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)

for i, x in enumerate(np.linspace(S[0], S[2], w)):

    for j, y in enumerate(np.linspace(S[1], S[3], h)):

        ray = Ray(O, D = np.array([x,y,0]) - O)

        col = np.zeros(3)
        depth = 0
        reflection = 1.0

        while depth < depth_max:
            traced = ray.trace(scene)
            if not traced:
                break

            obj, M, N, col_ray = traced
            ray = Ray(O = M + N * .0001, D = ray.D - 2 * np.dot(ray.D, N) * N )
            depth += 1
            col += reflection * col_ray
            reflection *= obj.reflection


        img[h - j - 1, i, : ] = np.clip(col, 0, 1)

from PIL import Image
rendered_image = (img * 255.0).astype(np.uint8)
rendered_image = Image.fromarray(rendered_image)
rendered_image.show()




