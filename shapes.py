from abc import ABC, abstractmethod
import numpy as np
import math

def normalise(v):
    return v / np.linalg.norm(v)

class Shape(object):

    def __init__(self, diffuse_c, specular_c, specular_k, reflection):
        self.diffuse_c = diffuse_c
        self.specular_c = specular_c
        self.specular_k = specular_k
        self.reflection = reflection

    @abstractmethod
    def intersects_with(self, ray):
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_normal_at(self, M):
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_colour_at(self, M):
        raise NotImplementedError("Not implemented")


class Sphere(Shape):

    def __init__(self, centre, radius, colour, diffuse_c, specular_c, specular_k, reflection):
        super().__init__(diffuse_c, specular_c, specular_k, reflection)
        self.colour = np.array(colour)
        self.centre = np.array(centre)
        self.radius = radius

    def intersects_with(self, ray):
        O = ray.O
        D = ray.D

        a = np.dot(D, D)
        b = 2 * np.dot(D, O - self.centre)
        c = np.dot(O - self.centre, O - self.centre) - self.radius ** 2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return math.inf
        else:
            s1 = (-b - math.sqrt(discriminant))/ (2 * a)
            s2 = (-b + math.sqrt(discriminant))/ (2 * a)
            if s1 < 0:
                return s2
            else:
                return s1

    def get_normal_at(self, M):
        return normalise(M - self.centre)

    def get_colour_at(self,M):
        return self.colour

class Plane(Shape):

    def __init__(self, p, n, colour_plane_0, colour_plane_1, diffuse_c, specular_c, specular_k, reflection):
        super().__init__(diffuse_c, specular_c, specular_k, reflection)
        self.p = np.array(p)
        self.n = normalise(np.array(n))
        self.colour_plane_0 = np.array(colour_plane_0)
        self.colour_plane_1 = np.array(colour_plane_1)


    def intersects_with(self, ray):
        denom = np.dot(ray.D, self.n)
        if abs(denom) < 1e-6:
            return math.inf

        d = np.dot(self.p - ray.O, self.n) / denom
        if d < 0:
            return math.inf

        return d

    def get_normal_at(self, M):
        return self.n

    def get_colour_at(self, M):
        if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2):
            return self.colour_plane_0
        else:
            return self.colour_plane_1







