__author__ = 'netanel'


GRINDING_TIME = 56.7/2  # [S]
WATER_POUR_TIME = (13.5/2)*1.265 # 17.7  # [S]
WATER_POUR_SEGMENTS = 3
WATER_DELAY_BETWEEN_SEGMENT = 10 
KNEADING_TIME = 60*4 + 15  # [S] 
BAKING_TIME = 10 #60*5  # [S]
EXTRUSION_TIME = 70   # how much time does an extrusion cycle take
EXTRUSION_NEMBER = 6  # how many times to run manual extrusion after kneading
TIME_TO_WAIT_BETWEEN_RUNS = 60*20  # waiting time after last extrusion untill next grinding

USE_INPUT_BUTTON = False  # if set to True, machine will start only on button touch
RUN_ONCE = False  # for debugging, run macine once and finish loop