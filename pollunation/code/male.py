from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Male ##

# Set Video Files
male_pre  = '/home/pi/Haavaka/avkanim_blink.mp4'

# Const
CATCH_TIME_TH = 5 # seconds

# Set GPIO names
bee_buzz    = 35
bee_lights  = 36
flag_female = 37
bee_on      = 38
flag_idle   = 31
bee2female  = 32

setup(bee_vibrate, OUT)
setup(bee_lights,  OUT)
setup(bee_catch,   IN, pull_up_down=PUD_DOWN)
setup(fem_release, IN, pull_up_down=PUD_DOWN)
setup(fem_catch,   OUT)

output(, False)
output(,  False)
output(,   False)

def state_idle():
  output(bee_buzz,    False)
  output(bee_lights,  False)
  output(flag_female, False)
  play_video(idle_video, loop=True)
  while True:
    if input(bee_on):
      return state_bee_on
        
def state_bee_on():
  output(bee_buzz, True)
  output(flag_female, False)
  # play_video(bee_on_video, loop=True)
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>= BEE_TIME_TH:
      return state_wait_for_female
  
def state_wait_for_female():
  output(bee_buzz, False)
  output(flag_female, True)
  play_video(wait_for_female_video, loop=True)
  while not input(flag_idle):
    output(bee2female, input(bee_on))
  return state_idle


# This is the old code
while False:
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
