from shapes import Shape
import numpy as np

class Light_Source:

    def __init__(self, position, colour):
        self.position = np.array(position)
        self.colour = np.array(colour)



class Scene:

    def __init__(self, ambient):

        self.objects = []
        self.lights = []
        self.ambient = ambient

    def add_object(self, object : Shape):
        self.objects.append(object)

    def add_light_source(self, l : Light_Source):
        self.lights.append(l)



