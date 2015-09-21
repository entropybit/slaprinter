__author__ = 'mithrawnuruodo'

import math

# period with which the parallel processes check for new incoming messages
checking_period = 0.0001

# period with which the stepper checks for new incoming commands
stepper_processing_period = 0.001

# period after which controller rechecks connected gamepad controller
# ToDo: currently not working correctly ..
refresh_cycle_time = 1
refresh_cycle = math.ceil(refresh_cycle_time/checking_period)

# Flag specifiying if an in memory DB is to be used or
# an actual one where the data will be stored in server.db in the apps main directory
in_memory_database=False

# option specfying how many steps at once are made
several_steps = 10

# for the nth input of b ToDo or a? : lookup
# do  several_steps*multiplier_base^n many steps
multiplier_base = 2
#mode = "stepper_calibration"
#mode = "run"


# flag for controlling if actual steps are executed or
# just debug outputs
# if script is executed in actual working mode and should set according
# voltages to pins set to true
stepper_mode = False

# logging flags

# produce log output for messages in main controller
log_controller_input = False

# produce log output for messages in stepper controller
log_steppercontroller = False

# produce log output for messages within the actual stepper class
log_stepper = True


