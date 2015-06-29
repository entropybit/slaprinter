__author__ = 'mithrawnuruodo'

import sys
from Control import SlaController

controller = SlaController(sys.argv)
controller.start()
