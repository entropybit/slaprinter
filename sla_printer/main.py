#__author__ = 'mithrawnuruodo'

import Model.Stepper as Stepper
#import Control.GamePadController as snes
#import View.Beamer
from Control import SlaPrinterController
import sys
import signal
import datetime

def get_now():
    "get the current date and time as a string"
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def sigterm_handler(_signo, _stack_frame):
    "When sysvinit sends the TERM signal, cleanup before exiting."
    print("[" + get_now() + "] received signal {}, exiting...".format(_signo))
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


controller = SlaPrinterController()
controller.start()

