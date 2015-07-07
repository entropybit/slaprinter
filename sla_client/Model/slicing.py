__author__ = 'aslan'

import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_triangles(pfile):
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
    print len(tri),len(normalen)
    for i in range(len(normalen)):
        print i
        norm = normalen[i]
        cur_tri = (tri[i*3],tri[i*3+1],tri[i*3+2])
        #full_tri.append([norm,cur_tri])
        full_tri.append(cur_tri)
    return np.array(full_tri)


def fillz(tris,z):

    save_t=[]

    for t in tris:
        zs = t[:,2]

        if ((zs[0] >= z and (zs[1] < z or zs[2] <z)) or
            (zs[0] < z and (zs[1] >= z or zs[2] >=z))):
                save_t.append(t)
    save_t = np.array(save_t)

    save_xs = save_t[:,:,0]
    min_x,max_x = np.min(save_xs),np.max(save_xs)

    xrange = np.arange(min_x,max_x,0.1)

    for x in xrange:
        # getroffene triangles..
        cur_tris = []

        xs = t[:,2]

        if ((zs[0] >= z and (zs[1] < z or zs[2] <z)) or
            (zs[0] < z and (zs[1] >= z or zs[2] >=z))):
                save_t.append(t)


if __name__ == "__main__":
    tris = create_triangles("pimpstick v2.stl")
    #for t in tris:
    #    print t[0,0]

    print "---"
    tri_x = tris[:,:,0]
    tri_y = tris[:,:,1]
    tri_z = tris[:,:,2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(tri_x, tri_y, tri_z, ".")

plt.show()