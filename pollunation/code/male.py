from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Male ##

# Set Video Files
idle_video = '/home/pi/mada-/pollunation/videos/avkanim_blink_00.mp4'
wait_for_female_video = '/home/pi/mada-/pollunation/videos/avkanim_sequence_00.mp4'

# Const
CATCH_TIME_TH = 3 # seconds

# Set GPIO names
bee_on      = 38
flag_female = 37
flag_idle   = 31
bee_lights  = 36
bee2female  = 32

setup(bee_lights , OUT)
setup(bee_on     , IN, pull_up_down=PUD_DOWN)
setup(flag_idle  , IN, pull_up_down=PUD_DOWN)
setup(flag_female, OUT)

output(, False)
output(,  False)
output(,   False)

def state_idle():
  output(bee_lights,  False)
  output(flag_female, False)
  idle_video.play()
  while True:
    if input(bee_on):
      return state_bee_on
        
def state_bee_on():
  output(flag_female, False)
  # play_video(bee_on_video, loop=True)
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>= BEE_TIME_TH:
      idle_video.pause()
      idle_video.restart()
      return state_wait_for_female
  
def state_wait_for_female():
  output(flag_female, True)
  wait_for_female_video.play()
  while not input(flag_idle):
    output(bee2female, input(bee_on))
  return state_idle
