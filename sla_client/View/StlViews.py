__author__ = 'mithrawnuruodo'

from stl import mesh
from OpenGL.GL import *
from QlWidget import Drawable



class SltModellView(Drawable):

    def __init__(self, path):
        Drawable.__init__()
        self.mesh = mesh.Mesh.from_file(path)

    def draw(self):
        glBegin(GL_TRIANGLES)

        for tri in self.mesh.points:
            glVertex3d(tri[0],tri[1],tri[2])

        glEnd()
