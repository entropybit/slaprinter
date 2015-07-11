__author__ = 'mithrawnuruodo'

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
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



class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, fps=60, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        # rotation variables
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

        # rotation flags
        self.xrotation = True
        self.yrotation = True
        self.zrotation = True

        self.trans_x = 0.0
        self.trans_y = 0.0
        self.trans_z = 0.0

        self.scale = 1.0

        self.x0 = 0
        self.y0 = 0

        self.rot = False
        self.trans = True

        self.moving_mode = False
        self.drawables = set()




        #self._timer = QtCore.QTimer()

        self._fps = fps
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


        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
        #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
        #glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
        glEnable(GL_DEPTH_TEST);
        glEnable(GL_LIGHTING);
        glEnable(GL_TEXTURE_2D);
        glEnable(GL_CULL_FACE);

        # track material ambient and diffuse from surface color, call it before glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
        glEnable(GL_COLOR_MATERIAL);
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


        glTranslate(self.trans_x, self.trans_y, self.trans_z)

        glRotate(self.rot_x, 1.0, 0, 0)
        glRotate(self.rot_y,0, 1.0, 0)
        glRotate(self.rot_z,0, 0, 1.0)

        glScale(self.scale, self.scale, self.scale)

        # translate cosy
        glTranslate(-0.5,-0.5,0)

        for d in self.drawables:
            d.draw()

        # redo tranlation
        glTranslate(0.5,0.5,0)

        #print("[" + str(time.time()) + "] end of paint " )

    def addDrawable(self,d):

        if isinstance(d, Drawable):
            self.drawables.add(d)


    def delDrawable(self,d):

        if isinstance(d,Drawable):
            self.drawables.remove(d)


    def spin(self):

        if self.xrotation:
            self.rot_x = (self.rot_x + 1) % 360.0

        if self.yrotation:
            self.rot_y = (self.rot_y + 1) % 360.0

        if self.zrotation:
            self.rot_z = (self.rot_z + 1) % 360.0

        #self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()



    def mousePressEvent(self, event):

        self.moving_mode = True

        # on left button go to panning mode
        if event.button() == QtCore.Qt.LeftButton:
            self.trans = True
            self.rot = False
        # on right button go to rotation mode
        else:
            self.trans = False
            self.rot = True


        #pos = event.pos()
        #self.x0, self.y0 = pos.x(), pos.y()
        #print("mouse press event (" + str(x) + ", " + str(y) + ")" )


    def mouseReleaseEvent(self, event):

        self.moving_mode = False
        self.x0 = 0
        self.y0 = 0

        #pos = event.pos()
        #x, y = pos.x(), pos.y()
        #print("mouse release event (" + str(x) + ", " + str(y) + ")" )


    def mouseMoveEvent(self, event):

        if self.moving_mode:
            pos = event.pos()

            x, y = pos.x(), pos.y()

            # apply difference beweteen last (x0,y0) and recent position
            # if there is a difference, if this is the first call of mouseMoveEvent after MousePressEvent
            # do not apply movement since ther is not yet enough data
            if self.x0 != 0 and self.y0 != 0:

                diffx = x - self.x0
                diffy = y - self.y0


                if self.trans:
                    w = 0.001
                    diffy = -1.0*diffy
                    self.trans_x = self.trans_x + diffx*w
                    self.trans_y = self.trans_y + diffy*w
                else:
                    w = 0.1
                    self.rot_y = self.rot_y + diffx*w
                    self.rot_x = self.rot_x + diffy*w

            # change x0 and y0 to received coordinates either way
            self.x0 = x
            self.y0 = y

            # after function refresh window
            #self.update()
            self.updateGL()

        #print("mouse move (" + str(x) + ", " + str(y) + ")t")

    def wheelEvent(self, event):

        #print(event.delta()/120.0)

        diff = event.delta()/120.0

        w = 1.1

        if diff >= 0:
            self.scale = self.scale*w
        else:
            self.scale = self.scale/w


        self.updateGL()
        #self.update()