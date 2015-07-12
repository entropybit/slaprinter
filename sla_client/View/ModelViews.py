__author__ = 'mithrawnuruodo'

import traceback
from OpenGL.GL import *
from QlWidget import Drawable
from enum import Enum

# # global displaylist index list
# display_lists = []
#
#
# def register_displaylist():
#     '''
#     A function used to register any View using a display in the global display_lists array.
#     This is done to atuomatically generate new indices for new display lists.
#     Normally this would be done by glGenists(1) or glGenLists(N) for N new display lists
#     but there seems to be a problem with this under PyQt4
#
#     :return: a new index
#
#     '''
#     n = 0
#
#     if len(display_lists)==0:
#         n = 1
#         display_lists.append(1)
#     else:
#         n = display_lists[-1] +1
#         display_lists.append(n)
#
#     print(" new index registered " + str(n))
#
#     return n
#
#
# def unregister_displaylist(index):
#     '''
#     unregister a disply list upon deletion
#
#     :param index: display list index to be deleted
#
#     :return: boolean corresponding to successful deletion
#     '''
#     if index in display_lists:
#         display_lists.remove(index)
#         return True
#
#     return False


class DrawingModes(Enum):
    '''
    listing of possible drawing modes for model views
    '''
    triangles = 1   # note: this is very slow don't use it
    displaylist = 2




class StlModelView(Drawable):

    def __init__(self, model, draw_mode = DrawingModes.displaylist):
        Drawable.__init__(self)
        self.__model = model

        self.__drawing_mode = draw_mode

        self__index = 0
        self.__initialized = False
        self.scale = 1.5/(self.getScale()[0])

        self.display_solid = True
        self.display_mesh = True
        self.bounding_box = False

    def __del__(self):
        #for indx in self.__indices:
        #    unregister_displaylist(indx)
        glDeleteLists(self.__index, 1);



    def draw(self):
        '''
            depending on the drawing mode draw the model as connected list of triangles
            so as GL_TRIANGLES
            or draw them as indexed list of triangles.
            This als uses GL_TRIANGLES but together with an indexed buffer.
        '''

        scale, sx, sy, sz = self.getScale()

        xmin, xmax = self.__model.xlims
        ymin, ymax = self.__model.ylims
        zmin, zmax = self.__model.zlims


        # do local scaling an translation
        # for better visualization
        glTranslate(-xmin , -ymin , -zmin)
        glTranslate(-sx/2.0, -sy/2.0, -sz/2.0)

        # depending on drawing mode draw call according draw method
        if self.__drawing_mode == DrawingModes.triangles:
            self.simpleTrianglesDraw()
        else:
            if self.__drawing_mode==DrawingModes.displaylist:
                self.displayListTrianglesDraw()

        # if specified draw bounding box
        if self.bounding_box:
            self.draw_bounding_box()


        # since translation and scaling were local
        # reverse them otherwise this will effect all other drawings aftewards
        glTranslate(sx/2.0, sy/2.0, sz/2.0)
        glTranslate(xmin , ymin , zmin)





    def simpleTrianglesDraw(self):
        '''
        draw a visualization of the provided stl file by iterating over the triangles and displaying them
        as a connected triangle list so as GL_TRIANGLES ...
        '''



        glBegin(GL_TRIANGLES)


        n = len(self.__model.mesh)

        v0 = self.__model.mesh.v0
        v1 = self.__model.mesh.v1
        v2 = self.__model.mesh.v2


        for i in range(0,n):

            #v = self.model.mesh.points[i]
            n = self.__model.mesh.normals[i]

            self.drawTriangle(v0[i],v1[i],v2[i],n)

        glEnd()



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

        xmin, xmax = self.__model.xlims
        ymin, ymax = self.__model.ylims
        zmin, zmax = self.__model.zlims

        scalex = xmax - xmin
        scaley = ymax - ymin
        scalez = zmax - zmin

        return [max(scalex,scaley, scalez), scalex, scaley, scalez]


    def displayListTrianglesDraw(self):

        if not self.__initialized:
            try:
                self.initGeometry()
            except Exception as e:
                print(traceback.format_exc())
                exit()


        scale, sx, sy, sz = self.getScale()

        #glEnableClientState(GL_VERTEX_ARRAY)
        #glVertexPointerf(self._vertices)

        # draw object
        if self.display_solid:
            glCallList(self.__index)

        # draw mesh
        if self.display_mesh:
            glCallList(self.__index+1)



    def setDrawingMode(self,mode):

        if isinstance(mode,DrawingModes):
            self.__drawing_mode = mode
        else:
            raise Exception("invalid drawing mode supplied")


    def initGeometry(self):


        print("entering init geometry")

        self.__index = glGenLists(2)




        v0_points = self.__model.mesh.v0
        v1_points = self.__model.mesh.v1
        v2_points = self.__model.mesh.v2
        n_points  = self.__model.mesh.normals



        glNewList(self.__index, GL_COMPILE)
        # add triangles
        glBegin(GL_TRIANGLES)

        N = len(self.__model.mesh)
        for i in range(0, N):
            v0 = v0_points[i]
            v1 = v1_points[i]
            v2 = v2_points[i]
            n = n_points[i]

            #glNormal3d(n[0],n[1],n[2])

            glColor3d(124.0/255.0, 126.0/255.0, 128.0/255.0)
            glVertex3d(v0[0],v0[1],v0[2])
            glVertex3d(v1[0],v1[1],v1[2])
            glVertex3d(v2[0],v2[1],v2[2])

        glEnd()
        glEndList()


        glNewList(self.__index+1, GL_COMPILE)

        # add mesh
        glBegin(GL_LINES)
        for i in range(0, N):
            v0 = v0_points[i]
            v1 = v1_points[i]
            v2 = v2_points[i]
            n = n_points[i]

            #glNormal3d(n[0],n[1],n[2])


            glColor3d(159.0/255.0,159.0/255.0,159.0/255.0)
            glVertex3d(v0[0], v0[1], v0[2])
            glVertex3d(v1[0], v1[1], v1[2])




            glVertex3d(v1[0], v1[1], v1[2])
            glVertex3d(v2[0], v2[1], v2[2])




            glVertex3d(v2[0], v2[1], v2[2])
            glVertex3d(v0[0], v0[1], v0[2])


        glEnd()

        glEndList()

        self.__initialized = True




        print("leaving init geometry")
        #print("result : |vertices| = " + str(len(self._vertices)))
        #print(self._vertices[1:10])
        #print(self._indexes[1:10])


    def mesh(self):
        self.display_mesh = not self.display_mesh


    def boundingBox(self):
        self.bounding_box = not self.bounding_box


    def draw_bounding_box(self):

        xmin, xmax = self.__model.xlims
        ymin, ymax = self.__model.ylims
        zmin, zmax = self.__model.zlims



        glBegin(GL_LINES)

        glColor3d(1.0,0,0)

        # front recangle
        glVertex3d(xmin,ymin,zmin)
        glVertex3d(xmax,ymin,zmin)

        glVertex3d(xmax,ymin,zmin)
        glVertex3d(xmax,ymax,zmin)

        glVertex3d(xmax,ymax,zmin)
        glVertex3d(xmin,ymax,zmin)

        glVertex3d(xmin,ymax,zmin)
        glVertex3d(xmin,ymin,zmin)


        # back rectangle
        glVertex3d(xmin,ymin,zmax)
        glVertex3d(xmax,ymin,zmax)

        glVertex3d(xmax,ymin,zmax)
        glVertex3d(xmax,ymax,zmax)

        glVertex3d(xmax,ymax,zmax)
        glVertex3d(xmin,ymax,zmax)

        glVertex3d(xmin,ymax,zmax)
        glVertex3d(xmin,ymin,zmax)


        # connecting lines
        glVertex3d(xmin,ymin,zmin)
        glVertex3d(xmin,ymin,zmax)

        glVertex3d(xmax,ymin,zmin)
        glVertex3d(xmax,ymin,zmax)

        glVertex3d(xmax,ymax,zmin)
        glVertex3d(xmax,ymax,zmax)

        glVertex3d(xmin,ymax,zmin)
        glVertex3d(xmin,ymax,zmax)

        glEnd()


