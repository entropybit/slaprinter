__author__ = 'mithrawnuruodo'

from abc import ABCMeta,abstractmethod
from StlModels import Model, StlModel
import numpy as np
import matplotlib.pyplot as plt


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


class EquiSlicer(Slicer):

    def __init__(self, stl_model):
        Slicer.__init__(self, stl_model)
        self.__slices = []

    def slice(self, sliceThickness):

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
        slicingLevelsList = np.arange(zmin+0.1, zmax-0.1, sliceThickness) #todo: should not be 0.1 but adaptive, but this simply works.
        print("Number of Slices: " + str(len(slicingLevelsList)))

        x_dims = [0, 0]
        y_dims = [0, 0]

        for slicingLevel in slicingLevelsList:
            #self.slicingLevel = 97.70
            # this a specific filter for the current slicingLevel
            iteration_filter = lambda tri: decide_relevant_triangles_z(tri, slicingLevel)

            save_z = np.array(filter(iteration_filter, self._model.mesh.points)) #todo: optimise this step - it needs 2.3s per slice (@130k triangles), about 99% of total CPU time
            results = []
            self.PlotListX = []
            self.PlotListY = []
            results.append([[0, 0, slicingLevel], [0, 0, slicingLevel]]) #basically the file output header.
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

                results.append([[x1, y1, 0],[x2, y2, 0]])

                x_dims = self.update_dims(x_dims, x1) #used to define bounding boxes in OpenGL
                x_dims = self.update_dims(x_dims, x2)

                y_dims = self.update_dims(y_dims, y1)
                y_dims = self.update_dims(y_dims, y2)


            results = np.array(results)

            #SORTING happens here (important for plt.fill() ):
            AlreadySeen = []
            shapes_counter = 0 #how many closed objects are in this slice
            SortedShapesList = []
            self.currentPlotListX = []
            self.currentPlotListY = []

            def PickNewStart():
                i = 1
                found_start = False
                while found_start == False:
                    if results[i].tolist() not in AlreadySeen:
                        AlreadySeen.append(results[i].tolist())
                        found_start = True
                    else:
                        i += 1
                return results[i].tolist()

            def FindNextPiece(ki):
                found_piece = False
                i = 1
                while not found_piece:
                    if results[i].tolist() not in AlreadySeen:
                        if np.allclose(ki[1], results[i, 0].tolist()):
                            currentShape.append(results[i].tolist())
                            AlreadySeen.append(results[i].tolist())
                            found_piece = True
                        elif np.allclose(ki[1], results[i, 1].tolist()):
                            currentShape.append([results[i, 1].tolist(), results[i, 0].tolist()]) #flip in case of endpoint=endpoint
                            AlreadySeen.append(results[i].tolist())
                            found_piece = True
                        else:
                            i += 1
                    else:
                        i += 1

            while len(AlreadySeen) < len(results)-1:
                currentShape = [PickNewStart()]
                while not np.allclose(currentShape[0][0], currentShape[-1][1]) or len(currentShape) == 1:
                    FindNextPiece(currentShape[-1])
                for i in range(len(currentShape)):
                    self.currentPlotListX.append(currentShape[i][0][0])
                    self.currentPlotListY.append(currentShape[i][0][1])
                self.currentPlotListX.append(None)
                self.currentPlotListY.append(None)
                currentShape.append(None)
                shapes_counter += 1
                SortedShapesList.append(currentShape)
            print("Objects in this slice: " + str(shapes_counter))
            self.PlotListX.append(self.currentPlotListX)
            self.PlotListY.append(self.currentPlotListY)
            self.allresults.append(Slice(results))

        # compute scale from extremal x and y values
        self._scale = self.compute_scale(x_dims, y_dims)
        self.x_dims = x_dims
        self.y_dims = y_dims

        return self.allresults

    def PlotSlice(self, slicenummer):
        plt.figure(1, facecolor='black')
        plt.subplot(1, 1, 1, axisbg='k')
        plt.fill(self.PlotListX[slicenummer], self.PlotListY[slicenummer], 'white')
        plt.xlim(self.x_dims)
        plt.ylim(self.y_dims)
        plt.show()


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

        s = max(sx, sy)

        return 1.0/s

if __name__ == "__main__":
    stl_model = StlModel('../Data/EiffelTowerTALL.stl')
    eiffel = EquiSlicer(stl_model)
    eiffel.slice(300)
    eiffel.PlotSlice(0)