__author__ = 'mithrawnuruodo'

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

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


        glRotate(self.rot_x, 1.0, 0, 0)
        glRotate(self.rot_y,0, 1.0, 0)
        glRotate(self.rot_z,0, 0, 1.0)

        glTranslate(self.trans_x, self.trans_y, self.trans_z)

        glScale(self.scale, self.scale, self.scale)



        # translate cosy
        glTranslate(-0.5,-0.5,0)

        # draw stuff for x in [0,1] and y in [0,1] so that this is centered
        self.drawStuff()

        # redo tranlation
        glTranslate(0.5,0.5,0)


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

        pos = event.pos()
        self.x0, self.y0 = pos.x(), pos.y()
        #print("mouse press event (" + str(x) + ", " + str(y) + ")" )


    def mouseReleaseEvent(self, event):
        pos = event.pos()
        x, y = pos.x(), pos.y()
        print("mouse release event (" + str(x) + ", " + str(y) + ")" )


    def mouseMoveEvent(self, event):
        pos = event.pos()
        x, y = pos.x(), pos.y()

        diffx = x - self.x0
        diffy = y - self.y0
        diffy = -1.0*diffy

        w = 0.001

        if self.trans:
            self.trans_x = self.trans_x + diffx*w
            self.trans_y = self.trans_y + diffy*w
        else:
            self.rot_y = self.rot_y + diffx*w
            self.rot_x = self.rot_x + diffy*w

        self.update()

        print("mouse move (" + str(x) + ", " + str(y) + ")t")





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
