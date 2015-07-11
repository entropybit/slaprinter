__author__ = 'mithrawnuruodo'

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array
from abc import ABCMeta,abstractmethod



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
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

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

        # object enables itself to receive events
        # like the ones triggered by mouse or keyboard input




    def initializeGL(self):
        # set background color
        self.qglClearColor(QtGui.QColor(60, 63, 65))
        self.initGeometry()

        glEnable(GL_DEPTH_TEST)

        # Set antialiasing
        glEnable( GL_LINE_SMOOTH )
        glEnable( GL_POLYGON_SMOOTH )
        glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )

        # Set alpha blending
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

    def resizeGL(self, width, height):
        if height == 0: height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
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

        # draw stuff for x in [0,1] and y in [0,1] so that this is centered
        #self.drawStuff()

        for d in self.drawables:
            d.draw()

        # redo tranlation
        glTranslate(0.5,0.5,0)


    def addDrawable(self,d):

        if isinstance(d, Drawable):
            self.drawables.add(d)


    def delDrawable(self,d):

        if isinstance(d,Drawable):
            self.drawables.remove(d)

    def drawStuff(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointerf(self.cubeVtxArray)
        glColorPointerf(self.cubeClrArray)
        glDrawElementsui(GL_QUADS, self.cubeIdxArray)

    def initGeometry(self):
        self.cubeVtxArray = array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 1.0]])
        self.cubeIdxArray = [
                0, 1, 2, 3,
                3, 2, 6, 7,
                1, 0, 4, 5,
                2, 1, 5, 6,
                0, 3, 7, 4,
                7, 6, 5, 4 ]
        self.cubeClrArray = [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0 ]]

    def spin(self):
        self.yRotDeg = (self.yRotDeg  + 1) % 360.0
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
                diffy = -1.0*diffy



                if self.trans:
                    w = 0.001
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
            self.update()

        print("mouse move (" + str(x) + ", " + str(y) + ")t")

    def wheelEvent(self, event):

        #print(event.delta()/120.0)

        diff = event.delta()/120.0

        w = 1.01

        if diff >= 0:
            self.scale = self.scale*w
        else:
            self.scale = self.scale/w


        self.update()









    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseMove:
    #         if event.buttons() == QtCore.Qt.NoButton:
    #             x0 = self.geometry().top
    #             y0 = self.pos().y()
    #
    #             pos = event.pos()
    #             print(" (x,y) = (" + str(pos.x()-x0) + "," + str(pos.y()-y0) + ")")
    #         else:
    #             pass # do other stuff
    #
    #     if event.type() == QtCore.QEvent.KeyPress:
    #
    #
    #
    #         if event.key() == QtCore.Qt.Key_Up:
    #             self.trans_y = self.trans_y + 0.01
    #             print("key up")
    #
    #         elif event.key() == QtCore.Qt.Key_Down:
    #             self.trans_y = self.trans_y - 0.01
    #             print("key dwn")
    #
    #
    #         if event.key() == QtCore.Qt.Key_Left:
    #             self.trans_x = self.trans_x - 0.01
    #             print("key left")
    #
    #         elif event.key() == QtCore.Qt.Key_Right:
    #             self.trans_x = self.trans_x + 0.01
    #             print("key right")
    #
    #
    #         if event.key() == QtCore.Qt.Key_Plus:
    #             self.scale = self.scale*1.05
    #
    #         elif event.key() == QtCore.Qt.Key_Minus:
    #             self.scale = self.scale/1.05
    #
    #
    #
    #         self.updateGL()
    #
    #     return QtGui.QMainWindow.eventFilter(self, source, event)
