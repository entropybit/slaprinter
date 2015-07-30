__author__ = 'aslan'

import numpy as np
import matplotlib.pyplot as plt

class Slicer(object):

    def __init__(self, filename):
        from stl import mesh
        self.filename = filename
        self.your_mesh = mesh.Mesh.from_file(self.filename)

    def slice(self):

        def decide_relevant_triangles_z(triangle):
            if ((triangle[2] >= self.slicingLevel and (triangle[5] < self.slicingLevel or triangle[8] < self.slicingLevel)) or (triangle[2] < self.slicingLevel and (triangle[5] >= self.slicingLevel or triangle[8] >= self.slicingLevel))):
                return True

        self.slicingLevel = 10.0 # fixed for now. needs to be turned into an iteration in the very end
        self.save_z = np.array(filter(decide_relevant_triangles_z, self.your_mesh.points))
        self.results = []

        for triangle in self.save_z:
            #decide which corner point is a (=the single point on the other side of the slicing level). b&c are on the same side of the slicing level
            if (triangle[2] <= self.slicingLevel and triangle[5] <= self.slicingLevel) or (triangle[2] >= self.slicingLevel and triangle[5] >= self.slicingLevel):
                self.a = triangle[6:9]
                self.b = triangle[0:3]
                self.c = triangle[3:6]
            elif (triangle[8] <= self.slicingLevel and triangle[5] <= self.slicingLevel) or (triangle[8] >= self.slicingLevel and triangle[5] >= self.slicingLevel):
                self.a = triangle[0:3]
                self.b = triangle[6:9]
                self.c = triangle[3:6]
            elif (triangle[8] <= self.slicingLevel and triangle[2] <= self.slicingLevel) or (triangle[8] >= self.slicingLevel and triangle[2] >= self.slicingLevel):
                self.a = triangle[3:6]
                self.b = triangle[6:9]
                self.c = triangle[0:3]
            else:
                print "Error! Aslan dun fuckd up!"
                quit()

            #calculating the cutpoints via intersecting the two c-a and b-a lines with the slicinglevel
            #c-a
            self.t1 = (self.slicingLevel-self.a[2])/(self.c[2]-self.a[2]) #2 means: the first calculation of this Linear Equation System is in the z-plane
            self.x1 = self.a[0]+self.t1*(self.c[0]-self.a[0]) #0 means: in the x-plane
            self.y1 = self.a[1]+self.t1*(self.c[1]-self.a[1]) #1 means: in the y-plane
            #b-a
            self.t2 = (self.slicingLevel-self.a[2])/(self.b[2]-self.a[2]) #2 means: the first calculation of this Linear Equation System is in the z-plane
            self.x2 = self.a[0]+self.t2*(self.b[0]-self.a[0]) #0 means: in the x-plane
            self.y2 = self.a[1]+self.t2*(self.b[1]-self.a[1]) #1 means: in the y-plane

            self.results.append([[self.x1, self.y1, self.slicingLevel], [self.x2, self.y2, self.slicingLevel]])

        self.result = np.array(self.results)

        return self.result

    def plot2DSlice(self):
        fig1 = plt.figure(1, facecolor='black')
        ax1 = plt.axes(frameon=False)
        plt.plot([self.result[:, 0, 0],self.result[:, 1, 0]],[self.result[:, 0, 1], self.result[:, 1, 1]],'white') #[[xstart],[xend]],[[ystart],[yend]]
        plt.show()

        #phillippes x-beam method for slicing (unclean)
        """
        #now we filter for x
        vertical_slicing_thickness = 1
        xrange = np.arange(np.min(self.save_z[:, 0:9:3]), np.max(self.save_z[:, 0:9:3]), vertical_slicing_thickness) #the object is in this x range.

        self.plotListX1 = [0]
        self.plotListX2 = [0]
        self.plotListY1 = [0]
        self.plotListY2 = [0]

        def decide_relevant_triangles_x(triangle):
            #if ((triangle[0] >= xSlicingLevel and (triangle[3] < xSlicingLevel or triangle[6] < xSlicingLevel)) or (triangle[0] < xSlicingLevel and (triangle[3] >= xSlicingLevel or triangle[6] >= xSlicingLevel))):
            if ((triangle[0] >= self.xSlicingLevel and (triangle[3] < self.xSlicingLevel or triangle[6] < self.xSlicingLevel)) or (triangle[0] < self.xSlicingLevel and (triangle[3] >= self.xSlicingLevel or triangle[6] >= self.xSlicingLevel))):
                return True

        self.save_x_all=[]
        for self.xSlicingLevel in xrange:
            self.save_x = np.array(filter(decide_relevant_triangles_x, self.save_z))
            self.save_x_all.append(self.save_x)
            y = []
            for i in range(len(self.save_x)): y.append((self.save_x[i, 1] + self.save_x[i, 4] + self.save_x[i, 7])/3) #todo: make this precise

            #y_chk = remove_duplicates(y)
            #print y
            #print y_chk
            if len(y) > 0:
                first_hit = y[0]
                second_hit = y[-1] #todo: how do i group my results nicely into n*2 pairs?

                self.plotListX1.append(self.xSlicingLevel)
                self.plotListX2.append(self.xSlicingLevel)
                self.plotListY1.append(first_hit)
                self.plotListY2.append(second_hit)

        def remove_duplicates(values):
            output = []
            seen = set()
            for value in values:
                # If value has not been encountered yet,
                # ... add it to both list and set.
                v = round(value*5, 0)/5
                if v not in seen:
                    output.append(v)
                    seen.add(v)
            return output


    def plot_xbeams(self):
        fig1 = plt.figure(1, facecolor='black')
        ax1 = plt.axes(frameon=False)
        plt.plot([self.plotListX1, self.plotListX2], [self.plotListY1, self.plotListY2], 'white')
        #plt.xlim([-xSlicingLevel*1.1,xSlicingLevel*1.1])
        plt.ylim([np.min(self.your_mesh.y), np.max(self.your_mesh.y)])
        ax1.set_frame_on(False)
        ax1.axes.get_yaxis().set_visible(False)

        from mpl_toolkits import mplot3d

        def plotReformat(save_something):
            fisch = np.zeros([len(save_something), 3, 3])
            for i in range(len(save_something)):
                fisch[i, 0, :] = save_something[i, 0:3]
                fisch[i, 1, :] = save_something[i, 3:6]
                fisch[i, 2, :] = save_something[i, 6:9]
            return fisch

        layernumber=4
        fig2 = plt.figure(2)
        axes = mplot3d.Axes3D(fig2)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(plotReformat(self.save_x_all[layernumber])))
        scale = self.your_mesh.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        plt.show()
        """

if __name__ == "__main__":
    eiffel = Slicer('EiffelTowerTALL.stl')
    eiffel.slice()
    eiffel.plot2DSlice()


    #eiffel.plot_xbeams()


#plots a given set of points
"""
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def plotReformat(save_something):
    fisch = np.zeros([len(save_something), 3, 3])
    for i in range(len(save_something)):
        fisch[i, 0, :] = save_something[i, 0:3]
        fisch[i, 1, :] = save_something[i, 3:6]
        fisch[i, 2, :] = save_something[i, 6:9]
    return fisch

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(plotReformat(save_x)))
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)
pyplot.show()
"""

#---------------------3D Plot with numpy-stl--------------------------------
"""
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

your_mesh = mesh.Mesh.from_file('EiffelTowerTALL.stl')

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)
pyplot.show()

"""

#---------------------test examples with numpy-stl for future reference---------------------------
"""
from stl import mesh
your_mesh = mesh.Mesh.from_file('EiffelTowerTALL.stl')
print your_mesh.vectors[0] # gibt alle punkte in vektorform aus
print your_mesh.points # gibt alle punkte aus.
print your_mesh.v0 #gibt das array der koordinaten der 0ten vektoren jedes einzelnen dreiecks aus
print your_mesh.x[0] #gibt die x-koordinaten des 0ten punktes aus.
print len(your_mesh) # gibt die anzahl der dreieckspunkte aus
print your_mesh.units #einheitsvektoren
print your_mesh.areas #flaechen
print your_mesh.normals #normalenvektoren
#data = numpy.zeros(VERTICE_COUNT, dtype=mesh.Mesh.dtype)
#your_mesh = mesh.Mesh(data, remove_empty_areas=False)
your_mesh.save('new_stl_file.stl')

"""

#---------------------phils binary fileload algorithm--LEGACY-----------------
"""
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_triangles(pfile): #reads binary .stl files
    data = open(pfile, "rb")
    data.read(data.tell()+80)
    dl = struct.unpack("@i", data.read(4))

    normalen = []
    tri = []

    for i in range(dl[0]):
        s = data.read(12)
        x = struct.unpack("<3f",s)
        normalen.append(x)
        for j in range(3):
            s = data.read(12)
            x = struct.unpack("<3f",s)
            tri.append(x)
        data.read(2)

    full_tri = []
    for i in range(len(normalen)):
        norm = normalen[i]
        cur_tri = (tri[i*3],tri[i*3+1],tri[i*3+2])
        #full_tri.append([norm,cur_tri])
        full_tri.append(cur_tri)
    return np.array(full_tri)
"""