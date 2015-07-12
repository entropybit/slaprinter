__author__ = 'mithrawnuruodo'

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *

#from ModelViews import StlModelView
from numpy import array
from abc import ABCMeta,abstractmethod
import time



class Drawable(object):

    __metaclass__ = ABCMeta

    udids = []

    def __init__(self):

        if len(self.udids) == 0:
            self.udid = 1
            self.udids.append(1)
        else:
            self.udid = self.udids[-1] +1


    def __hash__(self):
        return self.udid

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def mesh(self):
        pass

    @abstractmethod
    def boundingBox(self):
        pass



class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, fps=60, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        # rotation variables
        self._rot_x = 0.0
        self._rot_y = 0.0
        self._rot_z = 0.0

        # rotation flags
        self.xrotation = False
        self.yrotation = True
        self.zrotation = False

        self._trans_x = 0.0
        self._trans_y = 0.0
        self._trans_z = 0.0

        self._scale = 1.0

        self._x0 = 0
        self._y0 = 0

        self.allow_rot = True
        self.allow_trans = True
        self.allow_zoom = True


        self._rot = False
        self._trans = True
        self._moving_mode = False


        self._drawables = set()
        self.drawcosy = False


        #self._timer = QtCore.QTimer()
        #QtCore.QObject.connect(self._timer, QtCore.SIGNAL("timeout()"), self.updateGL)

        # object enables itself to receive events
        # like the ones triggered by mouse or keyboard input




    def initializeGL(self):
        # set background color
        self.qglClearColor(QtGui.QColor(60, 63, 65))

        glEnable(GL_DEPTH_TEST)

        # Set antialiasing
        glEnable( GL_LINE_SMOOTH )
        glEnable( GL_POLYGON_SMOOTH )
        glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )

        # Set alpha blending
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        glEnable(GL_VERTEX_ARRAY)


        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
        #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
        #glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
        #glEnable(GL_DEPTH_TEST);
        #glEnable(GL_LIGHTING);
        #glEnable(GL_TEXTURE_2D);
        #glEnable(GL_CULL_FACE);

        #glEnable(GL_LIGHTING)
        #glEnable(GL_LIGHT0)

        light0_pos = -12.0, 18.0, 30.0, 0.0
        diffuse0 = 0.5, 0.5, 0.5, 1.0
        specular0 = 0.5, 0.5, 0.5, 1.0
        ambient0 = 0.8, 0.8, 0.8, 1.0

        #glMatrixMode(GL_MODELVIEW)
        #glLightfv(GL_LIGHT0, GL_POSITION, light0_pos)
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse0)
        #glLightfv(GL_LIGHT0, GL_SPECULAR, specular0)
        #glLightfv(GL_LIGHT0, GL_AMBIENT, ambient0)

        # track material ambient and diffuse from surface color, call it before glEnable(GL_COLOR_MATERIAL)
        #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
        #glEnable(GL_COLOR_MATERIAL);
        #self._timer.start(1.0/self._fps)



    def resizeGL(self, width, height):
        if height == 0: height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):

        #print("[" + str(time.time()) + "] start of paint " )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslate(0.0, 0.0, -50.0)
        glScale(20.0, 20.0, 20.0)

        if self.allow_trans:
            glTranslate(self._trans_x, self._trans_y, self._trans_z)

        if self.allow_rot:
            glRotate(self._rot_x, 1.0, 0, 0)
            glRotate(self._rot_y,0, 1.0, 0)
            glRotate(self._rot_z,0, 0, 1.0)

        if self.allow_zoom:
            glScale(self._scale, self._scale, self._scale)

        if self.drawcosy:
            self.drawCosy()



        for d in self._drawables:
            d.draw()





        #print("[" + str(time.time()) + "] end of paint " )

    def addDrawable(self,d):

        if isinstance(d, Drawable):
            self._drawables.add(d)


    def delDrawable(self,d):

        if isinstance(d,Drawable):
            self._drawables.remove(d)


    def spin(self):

        if self.xrotation:
            self._rot_x = (self._rot_x + 1) % 360.0

        if self.yrotation:
            self._rot_y = (self._rot_y + 1) % 360.0

        if self.zrotation:
            self._rot_z = (self._rot_z + 1) % 360.0

        #self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()



    def mousePressEvent(self, event):

        self._moving_mode = True

        # on left button go to panning mode
        if event.button() == QtCore.Qt.LeftButton:
            self._trans = True
            self._rot = False
        # on right button go to rotation mode
        else:
            self._trans = False
            self._rot = True


        #pos = event.pos()
        #print("mouse press event (" + str(x) + ", " + str(y) + ")" )


    def mouseReleaseEvent(self, event):

        self._moving_mode = False
        self._x0 = 0
        self._y0 = 0

        #pos = event.pos()
        #x, y = pos.x(), pos.y()
        #print("mouse release event (" + str(x) + ", " + str(y) + ")" )


    def mouseMoveEvent(self, event):

        if self._moving_mode:
            pos = event.pos()

            x, y = pos.x(), pos.y()

            # apply difference beweteen last (x0,y0) and recent position
            # if there is a difference, if this is the first call of mouseMoveEvent after MousePressEvent
            # do not apply movement since ther is not yet enough data
            if self._x0 != 0 and self._y0 != 0:

                diffx = x - self._x0
                diffy = y - self._y0


                if self._trans:
                    w = 0.001
                    diffy = -1.0*diffy
                    self._trans_x = self._trans_x + diffx*w
                    self._trans_y = self._trans_y + diffy*w
                else:
                    w = 0.1
                    self._rot_y = self._rot_y + diffx*w
                    self._rot_x = self._rot_x + diffy*w

            # change x0 and y0 to received coordinates either way
            self._x0 = x
            self._y0 = y

            # after function refresh window
            self.updateGL()

            #print("mouse move (" + str(x) + ", " + str(y) + ")t")

    def wheelEvent(self, event):

        diff = event.delta()/120.0

        w = 1.1

        if diff >= 0:
            self._scale = self._scale*w
        else:
            self._scale = self._scale/w


        self.updateGL()


    def drawCosy(self):

        glBegin(GL_LINES)
        glColor3d(1.0,0,0)

        glVertex3d(0,0,0)
        glVertex3d(1.0,0,0)

        glVertex3d(0,0,0)
        glVertex3d(0,1.0,0)

        glVertex3d(0,0,0)
        glVertex3d(0,0,1.0)
        glEnd()


    def reset(self):

        self._scale = 1.0

        if len(self._drawables) > 0:
            for d in self._drawables:
                break
            self._scale = d.scale

        self._rot_x = 0
        self._rot_y = 0
        self._rot_z = 0

        self._trans_x = 0
        self._trans_y = 0
        self._trans_z = 0

        self.updateGL()


    def mesh(self):

        for d in self._drawables:
            d.mesh()

        self.updateGL()

    def bounding_box(self):

        for d in self._drawables:
            d.boundingBox()

        self.updateGL()



