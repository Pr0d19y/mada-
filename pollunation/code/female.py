gimport sys
sys.path.append('/home/pi/mada-/classes')
from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Female ##

debug=0

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file          = '/home/pi/mada-/pollunation/videos/tzaleket_idle_1024X600.mp4'
bee_on_video_file        = '/home/pi/mada-/pollunation/videos/tzaleket_blink_1024X600.mp4'
dust_complete_video_file = '/home/pi/mada-/pollunation/videos/tzaleket_after_1024X600.mp4'
idle_video = OMXPlayer(idle_video_file, loop = True, debug=debug)
dust_complete_video = OMXPlayer(dust_complete_video_file, debug=debug)

# Set GPIO names
bee_on        = 38
wait_for_bee  = 31
flag_male     = 37

setup(bee_on      , IN, pull_up_down=PUD_DOWN)
setup(wait_for_bee, IN, pull_up_down=PUD_DOWN)
setup(flag_male   , OUT)

output(flag_male, False)

def state_idle():
  output(flag_male, False)
  idle_video.play()
  while True:
    if input(wait_for_bee):
      return(state_wait_for_bee)

def state_wait_for_bee():
  output(flag_male, False)
  while True:
    if input(bee_on):
      return state_bee_on

def state_bee_on():
  output(flag_male, False)
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_wait_for_bee
    if (time.time() - start_time)>= CATCH_TIME_TH:
      return state_dust_complete

def state_dust_complete():
  output(flag_male, True)
  idle_video.pause()
  dust_complete_video.play()
  while dust_complete_video.paused:
    pass
  #time.sleep(2)
  return state_idle
  
