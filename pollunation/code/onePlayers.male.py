
import sys
sys.path.append('/home/pi/mada-/classes')
from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Male ##

debug=1

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = '/home/pi/mada-/pollunation/videos/avkanim_blink_00.mp4'
wait_for_female_video_file = '/home/pi/mada-/pollunation/videos/avkanim_sequence_00.mp4'

idle_video            = 'OMXPlayer(idle_video_file, loop=True, start_playback=True, debug=debug)'
wait_for_female_video = 'OMXPlayer(wait_for_female_video_file, loop=True, start_playback=True, debug=debug)'
omx = None

# Set GPIO names
bee_on      = 38 ## input
flag_idle   = 31 ## input
bee_lights  = 36 ## output # Also flags female
bee2female  = 32 ## output

setwarnings(False)
setup(bee_on     , IN, pull_up_down=PUD_DOWN)
setup(flag_idle  , IN, pull_up_down=PUD_DOWN)
setup(bee_lights , OUT)
setup(bee2female , OUT)

output(bee_lights, False)
output(bee2female, False)

def state_idle():
  output(bee_lights, False)
  output(bee2female, False)
  
  play(idle_video)
  while True:
    if input(bee_on):
      return state_bee_on
        
def state_bee_on():
  output(bee_lights, False)
  output(bee2female, False)
  #bee_on_video.play()
  start_time = time.time()
  while  True:
    if not input(bee_on):
      return state_idle
    if (time.time() - start_time)>=CATCH_TIME_TH:
      #idle_video.pause()
      #idle_video.restart()
      return state_wait_for_female
  
def state_wait_for_female():
  output(bee_lights, True)
  output(bee2female, False)
  play(wait_for_female_video)
  while not input(flag_idle):
    output(bee2female, input(bee_on))
  #wait_for_female_video.pause()
  #wait_for_female_video.restart()
  return state_idle

def play(video_cmd):
  global omx
  print 'omx is {0}'.format(omx)
  if omx is not None:
    print 'Stopping'
    omx.stop()
    time.sleep(0.5)
    print 'Stopped'
  exec 'omx = {0}'.format(video_cmd)
