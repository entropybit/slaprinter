__author__ = 'aslan'


import array
import cairo
import pygame
import rsvg

class Beamer(object):

    def __init__(self, *svgfile):
        #initialising the display
        self.WIDTH = int(round(1920*0.9)) # should be fullHD, the pi throws an error though. 90% of the resolution work
        self.HEIGHT = int(round(1080*0.9))
        self.svgfile = svgfile
        self.data = array.array('c', chr(0) * self.WIDTH * self.HEIGHT * 4)
        self.surface = cairo.ImageSurface.create_for_data(self.data, cairo.FORMAT_ARGB32, self.WIDTH, self.HEIGHT, self.WIDTH * 4)
        pygame.init()

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        if svgfile.__len__() == 0:
            self.svg = rsvg.Handle(file="black.svg") #instancing a Beamer() without loading a picture makes the screen go black - this way the resin doesnt get unnecessarily radiated
        else:
            self.svg = rsvg.Handle(file=self.svgfile[0])
        """
        #neuer code experimentell
        print self.svg.__sizeof__()
        self.pixbuf = self.svg.get_pixbuf(id='#layer30')
        print self.pixbuf
        #self.pixbuf.render_cairo(self.ctx)
        """
        self.ctx = cairo.Context(self.surface)
        self.svg.render_cairo(self.ctx)

        self.screen = pygame.display.get_surface()
        self.image = pygame.image.frombuffer(self.data.tostring(), (self.WIDTH, self.HEIGHT), "ARGB")

        self.screen.blit(self.image, (self.WIDTH/2, self.HEIGHT/2))
        pygame.display.flip()

        clock = pygame.time.Clock()
        while True:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit



#display = Beamer("pimpstick.svg")
if __name__ == "__main__":
    display = Beamer("pimpstick.svg")

#todo: anderes svg-layer anzeigen