import sys
sys.path.append('/home/pi/mada-/classes')
from omxplayer import OMXPlayer
from RPi.GPIO import *
import time

## Zuccini ##
debug_jmp = 29
setup(debug_jmp, IN, pull_up_down=PUD_UP)
debug = not input(debug_jmp)

# Set Video Files
idle_video_file          = '/home/pi/mada-/pollunation/videos/zucchini_idle.mp4'
dust_complete_video_file = '--orientation 180 /home/pi/mada-/pollunation/videos/zucchini_00.mp4'
idle_video          = OMXPlayer(idle_video_file, loop = True, debug=debug)
dust_complete_video = OMXPlayer(dust_complete_video_file, debug=debug)
#idle_video = dust_complete_video

# Set GPIO names
complete = 38

setwarnings(False)
setup(complete, IN, pull_up_down=PUD_DOWN)

def state_idle():
    #idle_video.restart()
    #time.sleep(0.4)
    idle_video.play()
    #time.sleep(0.7)
    #idle_video.pause()
    while True:
        if input(complete):
            return(state_dust_complete)

def state_dust_complete():
    dust_complete_video.play()
    while not dust_complete_video.paused:
        pass
    #time.sleep(2) #remove
    return state_idle
  
