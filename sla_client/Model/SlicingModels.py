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

    def __init__(self,points=[]):

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

    @property
    def points(self):
        return self.__points



class equiSlicer(Slicer):
    '''
    A simple slicer implementation which works by defining a set of equal height boxes.
    The slices are then defined by the vertices lying within the respective box.
    '''

    def __init__(self, stl_model, partitions=100):

        Slicer.__init__(self, stl_model)
        self.__partitions = partitions


    def slice(self):

        zmin, zmax = self._model.zlims
        z_inc = (zmax - zmin)*1.0/self.__partitions


    


