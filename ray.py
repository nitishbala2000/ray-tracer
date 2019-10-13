import numpy as np

def normalize(v):
    return v / np.linalg.norm(v)

class Ray(object):

    def __init__(self, O : np.ndarray, D : np.ndarray):
        self.O = O
        self.D = D / np.linalg.norm(D)

    def _find_closest_object_and_distance(self, scene):
        closest_object = None
        closest_object_distance = np.inf

        for object in scene.objects:
            distance = object.intersects_with(self)
            if distance < closest_object_distance:
                closest_object_distance = distance
                closest_object = object

        return closest_object, closest_object_distance


    def trace(self, scene):

        closest_object, closest_object_distance = self._find_closest_object_and_distance(scene)
        if closest_object is None:
            return

        #Position of closest object that ray hits
        M = self.O + closest_object_distance * self.D
        N = closest_object.get_normal_at(M)
        colour = closest_object.get_colour_at(M)

        col_ray = scene.ambient
        toO = normalize(self.O - M)
        for light in scene.lights:

            
            #If the ray from the light source to closest_object hit another object before, then ignore light source contribution
            shadow_ray = Ray(O = light.position, D = M - light.position)
            shadow_ray_closest_obj, _ = shadow_ray._find_closest_object_and_distance(scene)
            if shadow_ray_closest_obj is not closest_object:
                continue


            toL = normalize(light.position - M)

            #Diffuse reflection
            col_ray += closest_object.diffuse_c * max(np.dot(N, toL), 0) * colour
            col_ray += closest_object.specular_c * max(np.dot(N, normalize(toL + toO)),0) ** closest_object.specular_k * light.colour

        return closest_object, M, N, col_ray
