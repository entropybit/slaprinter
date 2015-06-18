__author__ = 'mithrawnuruodo'

import Model.Stepper as Stepper
import RPi.GPIO as GPIO
#import Control.snes as snes
import View.Beamer as Beamer


#display = View.Beamer()
#display2 = Beamer("pimpstick.svg")

#controller = snes.InputManager()


fisch = Stepper.SoncebosStepper()
fisch.down()
#fisch.up_wtf()
#fisch.disable()
