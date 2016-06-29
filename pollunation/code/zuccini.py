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
#idle_video          = OMXPlayer(idle_video_file, loop = True, debug=debug)
dust_complete_video = OMXPlayer(dust_complete_video_file, debug=debug, loop=True)
#idle_video = dust_complete_video

# Set GPIO names
complete = 38

setwarnings(False)
setup(complete, IN, pull_up_down=PUD_DOWN)

def state_idle():
    # Opening day workaround
    while True:
        time.sleep(5e-3)
        dust_complete_video.play()

    #idle_video.restart()
    time.sleep(0.4)
    
    #idle_video.play()
    time.sleep(0.7)
    dust_complete_video.pause()
    start_time = time.time()
    while time.time()-start_time < 1:
        time.sleep(5e-3)
        if not input(complete):
            start_time = time.time()
#        else:
#            import pdb
#            pdb.set_trace()
    return(state_dust_complete)

def state_dust_complete():
    dust_complete_video.play()
    while not dust_complete_video.paused:
        time.sleep(5e-3)
        pass
    #time.sleep(2) #remove
#    dust_complete_video.restart()
#    dust_complete_video.pause()
    return state_idle
  
