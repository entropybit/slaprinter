__author__ = 'mithrawnuruodo'

from abc import ABCMeta,abstractmethod
from StlModels import Model


class Slicer(object):
    '''
        Abstract slicer Object this is the standard layout of every slicer object.
        Specific slicers should be derived from this.
    '''

    def __init__(self, stl_model):

        self._model = None
        self_slices = []
        if isinstance(stl_model, Model):
            self._model = stl_model


    @abstractmethod
    def slice(self):
        pass


class Slice(object):
    '''
     A simple wrapper class for a set of points defining a slice
    '''

    # static slice id array holds the slice ids over all objects of this class
    slice_id = []

    def __init__(self, points):

        self.__points = points

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
    def points(self):
        return self.__points

    @property
    def xlims(self):
        return [self.x_min, self.x_max]


    @property
    def ylims(self):

        return [self.y_min, self.y_max]




class EquiSlicer(Slicer):
    '''
    A simple slicer implementation which works by defining a set of equal height boxes.
    The slices are then defined by the vertices lying within the respective box.
    '''

    def __init__(self, stl_model, partitions=100):

        Slicer.__init__(self, stl_model)
        self.__partitions = partitions


    def slice(self):

        zmin, zmax = self._model.zlims
        z_inc = (zmax - zmin)*(1.0/self.__partitions)

        print(" slicing with data: z_inc = " + str(z_inc) + " [z_min, z_max] = [" + str(zmin) + ", " + str(zmax) + "] " )

        points = self.getPointsByZincrement(z_inc, self.__partitions)


        slices = []
        for p in points:
            s = Slice(p)
            #print("#################################")
            #print("")
            #print(s)
            #print("")
            #print("---------------------------------")
            slices.append(s)

        return slices


    def getPointsByZincrement(self, z_inc, n):
        '''
        This function sorts all vertices into slices acording to the z-increment and the given target number of
        partitions.
        So all vertices will be grouped by theire z-value so that n slices of height z are build.

        :param z_inc:   z-increment (slice heights)
        :param n:       number of partitions / slices
        :return:        array of array of normalized points, where each line corresponds to the points in a slice
        '''

        points = []

        for i in range(0,n):
            points.append([])

        N = len(self._model.mesh)

        v0s = self._model.mesh.v0
        v1s = self._model.mesh.v1
        v2s = self._model.mesh.v2

        for i in range(0,N):

            v0 = v0s[i]
            v1 = v1s[i]
            v2 = v2s[i]


            indx0 = self.getIndex(z_inc,n,v0)
            indx1 = self.getIndex(z_inc,n,v1)
            indx2 = self.getIndex(z_inc,n,v2)


            v0 = self.normalize(v0s[i], self._model.xlims, self._model.ylims)
            v1 = self.normalize(v1s[i], self._model.xlims, self._model.ylims)
            v2 = self.normalize(v2s[i], self._model.xlims, self._model.ylims)


            #print("reveiced indices (i0,i1,i2) = (" + str(indx0) + ", " + str(indx1) + ", " + str(indx2) + ") ")

            if indx0 > -1:
                points[indx0].append(v0)

            if indx1 > -1:
                points[indx1].append(v1)

            if indx2 > -1:
                points[indx2].append(v2)

        return points


    def getIndex(self, z_inc, n, v):
        '''
        :param z_inc: z - increment used to build slices (essentially layer height)
        :param n:   number of layers
        :param v:   a vertix which is to be sorted wihtin a specific slice
        :return:    a index specifying the vertices layer index i stands for (i-1)th slice
        '''

        z = v[2]
        print(v)

        for i in range(0,n):

            z0 = i*z_inc
            z1 = (i+1)*z_inc
            print("i: " + str(i) + " (z, z0, z1) = (" + str(z) + ", " + str(z0) + ", " + str(z1) + ") | n = " + str(n))

            if z0 <= z and z < z1:
                return i

        return -1



    def normalize(self, v, xlims, ylims):

        '''

        This function is used to normalize the points to x/y-ranges [0,1]

        :param v:
        :param xlims:
        :param ylims:
        :return:
        '''


        def normalizer(t, tmin, tmax):
            #if tmin >= 0 or t >= 0:
            #    t = t/(1.0*tmax)
            #else:
            #    if t < 0:
            #        t = t/(1.0*tmin)

            t_scale = max(abs(tmin),abs(tmax))

            return t*1.0/t_scale

        xmin, xmax = xlims
        ymin, ymax = ylims


        x = v[0]
        y = v[1]
        z = v[2]

        x = normalizer(x,xmin,xmax)
        y = normalizer(y,ymin,ymax)



        return [x,y,0]