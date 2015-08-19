__author__ = 'mithrawnuruodo'

from abc import ABCMeta,abstractmethod
from StlModels import Model
import numpy as np
import math
import traceback


def drange(start,stop,inc):

    r = start
    while r < stop:
        yield r
        r += inc

class Slicer(object):
    '''
        Abstract slicer Object this is the standard layout of every slicer object.
        Specific slicers should be derived from this.
    '''

    def __init__(self, stl_model):

        self._model = None
        self._scale = 1.0
        self_slices = []
        if isinstance(stl_model, Model):
            self._model = stl_model


    @abstractmethod
    def slice(self):
        pass

    @property
    def scale(self):
        return self._scale


class Slice(object):
    '''
     A simple wrapper class for a set of points defining a slice
    '''

    # static slice id array holds the slice ids over all objects of this class
    slice_id = []

    def __init__(self, points):
        #print(points)
        self.__points = np.array(points)

        if len(self.slice_id) == 0:
            self.__id = 1
            self.slice_id.append(self.__id)
        else:
            self.__id = self.slice_id[-1] + 1
            self.slice_id.append(self.__id)


    def __del__(self):
        '''
            upon deletion remove id of this slice object from
            static slice_id array
        '''
        self.slice_id.remove(self.__id)

    def __hash__(self):
        '''
             :return    the hash of this object is its slice id
        '''
        return self.__id

    def __str__(self):

        s =  " This is slice id [" + str(self.__hash__()) + "] it contains " + str(len(self.__points)) + " points \n"
        s = s + " \n"
        s = s + " \n"
        s = s + " printing points now \n\n"
        s = s + str(self.__points)

        return s

    @property
    def xlims(self):
        if len(self.__points) > 0:
            xmin = np.min(self.__points[:,0])
            xmax = np.max(self.__points[:,0])
        else:
            xmin = 0
            xmax = 0

        return [xmin, xmax]

    @property
    def ylims(self):

        if len(self.__points) > 0:
            ymin = np.min(self.__points[:,1])
            ymax = np.max(self.__points[:,1])
        else:
            ymin = 0
            ymax = 0

        return [ymin, ymax]


    @property
    def points(self):
        return self.__points



#
# class EquiSlicer(Slicer):
#     '''
#     A simple slicer implementation which works by defining a set of equal height boxes.
#     The slices are then defined by the vertices lying within the respective box.
#     '''
#
#     def __init__(self, stl_model, partitions=100):
#
#         Slicer.__init__(self, stl_model)
#         self.__partitions = partitions
#
#
#     def slice(self):
#
#         zmin, zmax = self._model.zlims
#         z_inc = (zmax - zmin)*(1.0/self.__partitions)
#
#         print(" slicing with data: z_inc = " + str(z_inc) + " [z_min, z_max] = [" + str(zmin) + ", " + str(zmax) + "] " )
#
#         points = self.getPointsByZincrement(z_inc, self.__partitions)
#
#
#         slices = []
#         for p in points:
#             s = Slice(p)
#             #print("#################################")
#             #print("")
#             #print(s)
#             #print("")
#             #print("---------------------------------")
#             slices.append(s)
#
#         return slices
#
#
#     def getPointsByZincrement(self, z_inc, n):
#         '''
#         This function sorts all vertices into slices acording to the z-increment and the given target number of
#         partitions.
#         So all vertices will be grouped by theire z-value so that n slices of height z are build.
#
#         :param z_inc:   z-increment (slice heights)
#         :param n:       number of partitions / slices
#         :return:        array of array of normalized points, where each line corresponds to the points in a slice
#         '''
#
#         points = []
#
#         for i in range(0,n):
#             points.append([])
#
#         N = len(self._model.mesh)
#
#         v0s = self._model.mesh.v0
#         v1s = self._model.mesh.v1
#         v2s = self._model.mesh.v2
#
#         for i in range(0,N):
#
#             v0 = v0s[i]
#             v1 = v1s[i]
#             v2 = v2s[i]
#
#
#             indx0 = self.getIndex(z_inc,n,v0)
#             indx1 = self.getIndex(z_inc,n,v1)
#             indx2 = self.getIndex(z_inc,n,v2)
#
#
#             v0 = self.normalize(v0s[i], self._model.xlims, self._model.ylims)
#             v1 = self.normalize(v1s[i], self._model.xlims, self._model.ylims)
#             v2 = self.normalize(v2s[i], self._model.xlims, self._model.ylims)
#
#
#             #print("reveiced indices (i0,i1,i2) = (" + str(indx0) + ", " + str(indx1) + ", " + str(indx2) + ") ")
#
#             if indx0 > -1:
#                 points[indx0].append(v0)
#
#             if indx1 > -1:
#                 points[indx1].append(v1)
#
#             if indx2 > -1:
#                 points[indx2].append(v2)
#
#         return points
#
#
#     def getIndex(self, z_inc, n, v):
#         '''
#         :param z_inc: z - increment used to build slices (essentially layer height)
#         :param n:   number of layers
#         :param v:   a vertix which is to be sorted wihtin a specific slice
#         :return:    a index specifying the vertices layer index i stands for (i-1)th slice
#         '''
#
#         z = v[2]
#         print(v)
#
#         for i in range(0,n):
#
#             z0 = i*z_inc
#             z1 = (i+1)*z_inc
#             print("i: " + str(i) + " (z, z0, z1) = (" + str(z) + ", " + str(z0) + ", " + str(z1) + ") | n = " + str(n))
#
#             if z0 <= z and z < z1:
#                 return i
#
#         return -1
#
#
#
#     def normalize(self, v, xlims, ylims):
#
#         '''
#
#         This function is used to normalize the points to x/y-ranges [0,1]
#
#         :param v:
#         :param xlims:
#         :param ylims:
#         :return:
#         '''
#
#
#         def normalizer(t, tmin, tmax):
#             #if tmin >= 0 or t >= 0:
#             #    t = t/(1.0*tmax)
#             #else:
#             #    if t < 0:
#             #        t = t/(1.0*tmin)
#
#             t_scale = max(abs(tmin),abs(tmax))
#
#             return t*1.0/t_scale
#
#         xmin, xmax = xlims
#         ymin, ymax = ylims
#
#
#         x = v[0]
#         y = v[1]
#         z = v[2]
#
#         x = normalizer(x,xmin,xmax)
#         y = normalizer(y,ymin,ymax)
#
#
#
#         return [x,y,0]



class EquiSlicer(Slicer):


    def __init__(self, stl_model, partitions=100):
        Slicer.__init__(self, stl_model)
        self.__slices = []
        self.__partitions = partitions


    def getSlicingThickness(self):

        zmin, zmax = self._model.zlims

        thickness = (zmax - zmin)*(1.0/(1.0*self.__partitions))

        return thickness


    def slice(self):

        sliceThickness = self.getSlicingThickness()




        if len(self.__slices) > 0:
            self.__slices = []

        def decide_relevant_triangles_z(triangle, slicingLevel):
            if ((triangle[2] >= slicingLevel and (triangle[5] < slicingLevel or triangle[8] < slicingLevel)) or (triangle[2] < slicingLevel and (triangle[5] >= slicingLevel or triangle[8] >= slicingLevel))):
                return True

        def select_triangles(triangle, slicingLevel):
            if (triangle[2] <= slicingLevel and triangle[5] <= slicingLevel) or (triangle[2] >= slicingLevel and triangle[5] >= slicingLevel):
                a = triangle[6:9]
                b = triangle[0:3]
                c = triangle[3:6]
            elif (triangle[8] <= slicingLevel and triangle[5] <= slicingLevel) or (triangle[8] >= slicingLevel and triangle[5] >= slicingLevel):
                a = triangle[0:3]
                b = triangle[6:9]
                c = triangle[3:6]
            elif (triangle[8] <= slicingLevel and triangle[2] <= slicingLevel) or (triangle[8] >= slicingLevel and triangle[2] >= slicingLevel):
                a = triangle[3:6]
                b = triangle[6:9]
                c = triangle[0:3]
            else:
                print "Error! Aslan dun fuckd up!"
                quit()

            return [a,b,c]

        self.allresults = []

        #slicingLevelsList = range(min(self._model.z.flatten()), max(self._model.z.flatten()), sliceThickness)
        zmin, zmax = self._model.zlims
        slicingLevelsList = drange(zmin, zmax, sliceThickness)

        x_dims = [0,0]
        y_dims = [0,0]

        for slicingLevel in slicingLevelsList:
            #self.slicingLevel = 97.70
            # this a specific filter for the current slicingLevel
            iteration_filter = lambda tri: decide_relevant_triangles_z(tri, slicingLevel)

            save_z = np.array(filter(iteration_filter, self._model.mesh.points)) #todo: optimise this step - it needs 2.3s per slice (@130k triangles), about 99% of total CPU time
            results = []
            #results.append([["sliceLevel", slicingLevel], [0, 0]]) #basically the file output header.
            #decide which corner point is a (=the single point on the other side of the slicing level). b&c are on the same side of the slicing level
            for triangle in save_z:
                a,b,c = select_triangles(triangle, slicingLevel)


                #calculating the cutpoints via intersecting the two c-a and b-a lines with the slicinglevel-plane. results are points. drawing a line between those gives me a pice of the slicing edge
                #c-a
                if c[2] - a[2] == 0:
                    print("(slicingLevel-a[2])/(c[2]-a[2]) = (" + str(slicingLevel) + "-" + str(a[2]) + ")/(" + str(c[2]) + "-" + str(a[2]) + ")")

                t1 = (slicingLevel-a[2])/(c[2]-a[2]) #2 means: the first calculation of this Linear Equation System is in the z-plane
                x1 = a[0]+t1*(c[0]-a[0]) #0 means: in the x-plane
                y1 = a[1]+t1*(c[1]-a[1]) #1 means: in the y-plane
                #b-a

                if b[2] - a[2] == 0:
                    print("(slicingLevel-a[2])/(b[2]-a[2]) = (" + str(slicingLevel) + "-" + str(a[2]) + ")/(" + str(b[2]) + "-" + str(a[2]) + ")")

                t2 = (slicingLevel-a[2])/(b[2]-a[2]) #2 means: the first calculation of this Linear Equation System is in the z-plane
                x2 = a[0]+t2*(b[0]-a[0]) #0 means: in the x-plane
                y2 = a[1]+t2*(b[1]-a[1]) #1 means: in the y-plane


                results.append([x1, y1, 0])
                results.append([x2, y2, 0])

                x_dims = self.update_dims(x_dims, x1) #used to define bounding boxes in OpenGL
                x_dims = self.update_dims(x_dims, x2)

                y_dims = self.update_dims(y_dims, y1)
                y_dims = self.update_dims(y_dims, y2)


            results = np.array(results)
            self.allresults.append(Slice(results))


        # compute scale from extremal x and y values
        self._scale = self.compute_scale(x_dims, y_dims)

        return self.allresults


    def update_dims(self,dims,cmpr):

        if cmpr > dims[1]:
            dims[1] = cmpr
        elif cmpr <= dims[0]:
            dims[0] = cmpr

        return dims

    def compute_scale(self, x_dims, y_dims):

        xmin, xmax = x_dims
        ymin, ymax = y_dims

        sx = xmax - xmin
        sy = ymax - ymin

        s = max(sx,sy)

        return 1.0/s


if __name__ == "__main__":
    partitions = 4
    eiffel = EquiSlicer('../Data/EiffelTowerTALL.stl',partitions)
    eiffel.slice(100)