__author__ = 'mithrawnuruodo'


from OpenGL.GL import *
from QlWidget import Drawable
from enum import Enum

class DrawingModes(Enum):
    '''
    listing of possible drawing modes for model views
    '''
    triangles = 1
    indexed = 2



class StlModelView(Drawable):

    def __init__(self, model):
        Drawable.__init__(self)
        self._model = model

        self._drawing_mode = DrawingModes.triangles


    def draw(self):
        '''
            depending on the drawing mode draw the model as connected list of triangles
            so as GL_TRIANGLES
            or draw them as indexed list of triangles.
            This als uses GL_TRIANGLES but together with an indexed buffer.
        '''


        if self._drawing_mode == DrawingModes.triangles:
            self.simpleTrianglesDraw()
        else:
            if self._drawing_mode==DrawingModes.indexed:
                self.indexedTrianglesDraw()


    def simpleTrianglesDraw(self):
        '''
        draw a visualization of the provided stl file by iterating over the triangles and displaying them
        as a connected triangle list so as GL_TRIANGLES ...
        '''

        scale, sx, sy, sz = self.getScale()

        # do local scaling an translation for better
        # displaying
        glScale(1.0/scale,1.0/scale,1.0/scale)
        glTranslate(sx/2.0,sy/2.0,0)


        glBegin(GL_TRIANGLES)


        n = len(self._model.mesh)

        v0 = self._model.mesh.v0
        v1 = self._model.mesh.v1
        v2 = self._model.mesh.v2


        for i in range(0,n):

            #v = self.model.mesh.points[i]
            n = self._model.mesh.normals[i]

            self.drawTriangle(v0[i],v1[i],v2[i],n)

        glEnd()

        # since translation and scaling were local
        # reverse them otherwise this will effect all other drawings aftewards
        glTranslate(-sx/2.0,-sy/2.0,0)
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

        xmin, xmax = self._model.xlims
        ymin, ymax = self._model.ylims
        zmin, zmax = self._model.zlims

        scalex = xmax - xmin
        scaley = ymax - ymin
        scalez = zmax - zmin

        return [max(scalex,scaley, scalez), scalex, scaley, scalez]



    def setDrawingMode(self,mode):

        if isinstance(mode,DrawingModes):
            self._drawing_mode = mode
        else:
            raise Exception("invalid drawing mode supplied")