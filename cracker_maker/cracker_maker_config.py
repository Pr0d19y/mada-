__author__ = 'netanel'

# grinder configurations
GRINDING_TIME = 28  # [S]
PULSE_GRINDER_FOR_STARTUP = True  # do we want to start/ stop the grinder 3 times before actually starting (help with startup of grinder)

# water configurations
WATER_POUR_TIME = 7.5  # [S] Total time for watering
WATER_POUR_SEGMENTS = 3
WATER_DELAY_BETWEEN_SEGMENT = 10 

# kneading + extruding configurations
FULL_EXTRUSIONS_NUMBER = 10 #6 at 3.7.16  # how many times to run manual extrusion after kneading

USE_PULSED_EXTRUSTION = True  # extrude in small pulses (instead of FULL_EXTRUSIONS_NUMBER)
PULSED_EXTRUSION_TIME = 8 # if we are using small pulses of extrusion, this is the extrusion amount [S]
WAIT_TIME_AFTER_PULSED_EXTRUSION = 120  # [S]
AMOUNT_OF_PULSED_EXTRUSIONS = 20

BAKING_TIME = 10 #60*5  # [S]
TIME_TO_WAIT_BETWEEN_RUNS = 60*20  # waiting time after last extrusion untill next grinding

# constants
KNEADING_TIME = 60*4 + 15  # [S] time to wait for aouto kneading proccess to finish
EXTRUSION_TIME = 70   # how much time does an extrusion cycle take

# debug options
USE_INPUT_BUTTON = False  # if set to True, machine will start only on button touch
RUN_ONCE = False  # for debugging, run macine once and finish loop