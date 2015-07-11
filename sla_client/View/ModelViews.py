__author__ = 'mithrawnuruodo'


from OpenGL.GL import *
from QlWidget import Drawable



class StlModelView(Drawable):

    def __init__(self, model):
        Drawable.__init__(self)
        self.model = model

        print(" x [max, min] = ")
        print(model.xlims)
        print("")

        print(" x [max, min] = ")
        print(model.ylims)
        print("")

        print(" x [max, min] = ")
        print(model.zlims)
        print("")

    def draw(self):
        '''
        draw a visualization of the provided stl file by iterating over the triangles and displaying them
        as a connected triangle list so as GL_TRIANGLES ...



        :return:
        '''

        '''
        ToDo: this is very inefficient we need to do this as vertex buffer or something like this because then the data
        would be written directly into the graphicard memory, therfore transformations like panning, zooming or rotation
        will be much faster
        '''


        scale = self.getScale()
        scale = scale[0]

        glScale(1.0/scale,1.0/scale,1.0/scale)

        glBegin(GL_TRIANGLES)

        n = len(self.model.mesh)

        v0 = self.model.mesh.v0
        v1 = self.model.mesh.v1
        v2 = self.model.mesh.v2


        for i in range(0,n):

            #v = self.model.mesh.points[i]
            n = self.model.mesh.normals[i]

            self.drawTriangle(v0[i],v1[i],v2[i],n)

        glEnd()

        glScale(scale,scale,scale)

    def drawTriangle(self,v0,v1,v2,n):
        '''
        draw a triangle given the edges and a normal vector

        :param v0:  triangle edge 0 in form [x0,y0,z0]
        :param v1:  triangle edge 1 in form [x1,y1,z1]
        :param v2:  triangle edge 2 in form [x2,y2,z2]
        :param n:   normal vector of the trianlge in form [nx,ny,nz]

        :return:    nothing
        '''

        glNormal3d(n[0],n[1],n[2])
        glVertex3d(v0[0],v0[1],v0[2])
        glVertex3d(v1[0],v1[1],v1[2])
        glVertex3d(v2[0],v2[1],v2[2])



    def getScale(self):
        '''
        This function is used to get the scalings based on the provided stl modells x,y and z dimensions
        These can than be used to update the zooming

        :return:    vector containing maximum of scales, xscale, yscale, zscale in this ordering

        '''

        xmin, xmax = self.model.xlims
        ymin, ymax = self.model.ylims
        zmin, zmax = self.model.zlims

        scalex = xmax - xmin
        scaley = ymax - ymin
        scalez = zmax - zmin

        return [max(scalex,scaley, scalez), scalex, scaley, scalez]

