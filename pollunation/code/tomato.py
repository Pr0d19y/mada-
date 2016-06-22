import sys
sys.path.append('/home/pi/mada-/classes')
from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Tomato (bi-sex) ##

debug = 0

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = '/home/pi/mada-/pollunation/videos/tomato_blink_1024X600.mp4'
dust_complete_video_file = '/home/pi/mada-/pollunation/videos/tomato_after_1024X600.mp4'
idle_video = OMXPlayer(idle_video_file, loop = True, debug=debug)
dust_complete_video = OMXPlayer(dust_complete_video_file, debug=debug)

# Set GPIO names
bee_on        = 38
bee_buzz      = 37

setup(bee_on      , IN, pull_up_down=PUD_DOWN)
setup(bee_buzz    , OUT)

output(bee_buzz, True)

def state_idle():
  idle_video.play()
  while True:
    if input(bee_on):
      return state_bee_on

def state_bee_on():
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>= CATCH_TIME_TH:
      idle_video.pause()
      return state_dust_complete

def state_dust_complete():
  dust_complete_video.play()
  while not dust_complete_video.paused:
    pass
  return state_idle
