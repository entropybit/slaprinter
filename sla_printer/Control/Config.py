__author__ = 'mithrawnuruodo'

import math

checking_interval = 0.000001

refresh_cycle_time = 1
refresh_cycle = math.ceil(refresh_cycle_time/checking_interval)


in_memory_database=False
on_raspberry_pi = False
mode = "stepper_calibration"

multiple_steps = 100