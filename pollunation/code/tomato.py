from RPi.GPIO import *
import time

## Tomato (bi-sex) ##

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = ''
dust_complete_video_file = ''
#idle_video = OMXPlayer(idle_video_file, loop = True)
#dust_complete_video = OMXPlayer(dust_complete_video_file)

# Set GPIO names
bee_on        = 38
bee_buzz      = 37

setup(bee_on      , IN, pull_up_down=PUD_DOWN)
setup(bee_buzz    , OUT)

output(bee_buzz, True)

def state_idle():
  while True:
    if input(bee_on):
      return state_bee_on

def state_bee_on():
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>= CATCH_TIME_TH:
      return state_dust_complete

def state_dust_complete():
  #play_video(dust_complete_video, wait=True)
  time.sleep(2)
  return state_idle
