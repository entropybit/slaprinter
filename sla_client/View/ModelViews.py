__author__ = 'mithrawnuruodo'

import traceback
from OpenGL.GL import *
from GlWidget import Drawable
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


        if self.__drawing_mode==DrawingModes.displaylist:
            self.displayListTrianglesDraw()

        # if specified draw bounding box
        if self.bounding_box:
            self.draw_bounding_box()


        # since translation and scaling were local
        # reverse them otherwise this will effect all other drawings aftewards
        glTranslate(sx/2.0, sy/2.0, sz/2.0)
        glTranslate(xmin , ymin , zmin)



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


        #print("entering init geometry")

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



            #glColor3d(124.0/255.0, 126.0/255.0, 128.0/255.0)
            glColor3d(212.0/255.0, 214.0/255.0, 217.0/255.0)
            glNormal3d(n[0],n[1],n[2])
            glVertex3d(v0[0],v0[1],v0[2])

            glNormal3d(n[0],n[1],n[2])
            glVertex3d(v1[0],v1[1],v1[2])

            glNormal3d(n[0],n[1],n[2])
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


            #glColor3d(159.0/255.0,159.0/255.0,159.0/255.0)
            glColor3d(0,0,0)
            glVertex3d(v0[0], v0[1], v0[2])
            glVertex3d(v1[0], v1[1], v1[2])




            glVertex3d(v1[0], v1[1], v1[2])
            glVertex3d(v2[0], v2[1], v2[2])




            glVertex3d(v2[0], v2[1], v2[2])
            glVertex3d(v0[0], v0[1], v0[2])


        glEnd()

        glEndList()

        self.__initialized = True




        #print("leaving init geometry")
        #print("result : |vertices| = " + str(len(self._vertices)))
        #print(self._vertices[1:10])
        #print(self._indexes[1:10])


    def mesh(self):
        self.display_mesh = not self.display_mesh

    def solid(self):
        self.display_solid = not self.display_solid

    def boundingBox(self):
        self.bounding_box = not self.bounding_box


    def draw_bounding_box(self):

        xmin, xmax = self.__model.xlims
        ymin, ymax = self.__model.ylims
        zmin, zmax = self.__model.zlims


        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)

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

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)


class SliceModelView(Drawable):

    def __init__(self, model):
        Drawable.__init__(self)
        self.__model = model

        self.__initialized = False
        self.display_points = True
        self.display_mesh = True

    def __del__(self):
        glDeleteLists(self.__index, 1);

    def draw(self):
        self.displayListTrianglesDraw()

    def displayListTrianglesDraw(self):

        if not self.__initialized:
            try:
                self.initGeometry()
            except Exception as e:
                print(traceback.format_exc())
                exit()

        #glEnableClientState(GL_VERTEX_ARRAY)
        #glVertexPointerf(self._vertices)

        # draw object
        if self.display_points:
            glCallList(self.__index)

        # draw mesh
        if self.display_mesh:
            glCallList(self.__index+1)


    def initGeometry(self):


        #print("entering init geometry")

        self.__index = glGenLists(2)

        points = self.__model.points

        glNewList(self.__index, GL_COMPILE)
        # add triangles
        glBegin(GL_POINTS)

        for p in points:
            #glNormal3d(n[0],n[1],n[2])
            glColor3d(1.0,0,0)
            glVertex3d(p[0],p[1],p[2])
        glEnd()
        glEndList()


        glNewList(self.__index+1, GL_COMPILE)

        # add mesh

        glBegin(GL_LINES)
        for p in points:
            #glNormal3d(n[0],n[1],n[2])
            glColor3d(159.0/255.0,159.0/255.0,159.0/255.0)
            glVertex3d(p[0],p[1],p[2])
        glEnd()
        glEndList()

        self.__initialized = True

        #print("leaving init geometry")
        #print("result : |vertices| = " + str(len(self._vertices)))
        #print(self._vertices[1:10])
        #print(self._indexes[1:10])


    def mesh(self):
        self.display_mesh = not self.display_mesh

    def solid(self):
        self.display_points = not self.display_points