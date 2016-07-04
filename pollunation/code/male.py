import sys
sys.path.append('/home/pi/mada-/classes')
from omxplayer_pollunation import OMXPlayer
from RPi.GPIO import *
import time

## Male ##

debug_jmp = 29
setup(debug_jmp, IN, pull_up_down=PUD_UP)
debug = 1 if not input(debug_jmp) else 0

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file            = '/home/pi/mada-/pollunation/videos/avkanim_blink_1024x600.mp4'
wait_for_female_video_file = '/home/pi/mada-/pollunation/videos/avkanim_after_1024x600.mp4'

idle_video            = OMXPlayer(idle_video_file, loop=True, debug=debug)
wait_for_female_video = OMXPlayer(wait_for_female_video_file, loop=False, debug=debug)
#omx = None

# Set GPIO names
bee_on      = 38 ## input
flag_idle   = 31 ## input
bee_lights  = 36 ## output # Also flags female
light2fem   = 37 ## output
bee2female  = 32 ## output

setwarnings(False)
setup(bee_on     , IN, pull_up_down=PUD_DOWN)
setup(flag_idle  , IN, pull_up_down=PUD_DOWN)
setup(bee_lights , OUT)
setup(light2fem  , OUT)
setup(bee2female , OUT)

output(bee_lights, False)
output(bee2female, False)
output(light2fem,  False)

def state_begin():
  return state_idle

def state_idle():
  output(bee_lights, False)
  output(light2fem,  False)
  output(bee2female, False)
  
  idle_video.play()
  time.sleep(1)
  while True:
    time.sleep(5e-3)
    if input(bee_on):
      return state_bee_on
        
def state_bee_on():
  output(bee_lights, False)
  output(light2fem,  False)
  output(bee2female, False)
  #bee_on_video.play()
  start_time = time.time()
  while  True:
    time.sleep(5e-3)
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>=CATCH_TIME_TH:
      idle_video.pause()
      #idle_video.restart()
      return state_wait_for_female
  
def state_wait_for_female():
  output(bee_lights, True)
  output(light2fem,  True)
  output(bee2female, False)
  wait_for_female_video.play()
  time.sleep(2)
  start_time = time.time()
  while time.time()-start_time < CATCH_TIME_TH:
    time.sleep(5e-3)
    if not input(bee_on):
      start_time = time.time()
  output(bee2female, True)
  time.sleep(2)
  #if not input(flag_idle):
  #    start_time = time.time()
  #wait_for_female_video.pause()
  wait_for_female_video.restart()
  return state_idle
