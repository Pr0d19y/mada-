from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Female ##

# Const
CATCH_TIME_TH = 5 # seconds

# Set GPIO names
bee_lights  = 38
bee_catch   = 36
male_release = 

setup(bee_lights,  OUT)
setup(bee_catch,   IN, pull_up_down=PUD_DOWN)
setup(fem_release, IN, pull_up_down=PUD_DOWN)
setup(fem_catch,   OUT)

output(bee_vibrate, False)
output(bee_lights,  False)
output(fem_catch,   False)

# Set Videos
flags = '--loop'
male_pre  = OMXPlayer('/home/pi/Haavaka/avkanim_blink.mp4', '--loop')
male_post = OMXPlayer('/home/pi/Haavaka/<<<NAME>>>>.mp4', '--loop')

while True:
    male_pre.play()
    is_bee_catched = False
    catch_time = 0
    while catch_time < CATCH_TIME_TH:
        while not input(bee_catch):
            output(bee_vibrate, False)
            pass
        start_time = time.time()
        while input(bee_catch):
            output(bee_vibrate, True)
            pass
        end_time  = time.time()
        catch_time = end_time - start_time
    
    is_bee_catched = True
    
    output(fem_catch, True)
    male_pre.pause()
    male_post.play()

    while not fem_release:
        pass
    male_post.pause()
