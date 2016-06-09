from RPi.GPIO import *
import time

## Zuccini ##

# Set Video Files
idle_video_file = '/home/pi/mada-/pollunation/videos/zucchini_00.mp4'
dust_complete_video_file = '/home/pi/mada-/pollunation/videos/zucchini_idle.mp4'
#idle_video = OMXPlayer(idle_video_file, loop = True)
#dust_complete_video = OMXPlayer(dust_complete_video_file)

# Set GPIO names
complete = 38

setup(complete, IN, pull_up_down=PUD_DOWN)
def state_idle():
    #idle_video.play()
    while True:
        if input(complete):
            idle_video.pause()
            idle_video.restart()
            return(state_dust_complete)

def state_dust_complete():
    #dust_complete_video.play()
    #while not dust_complete_video.paused:
    #    pass
    time.sleep(2) #remove
    return state_idle
  
