import time
import sys
sys.path.append('/home/pi/mada-')
from classes import omxplayer

print 'Debug 1'
movie_1 = '/home/pi/mada-/pollunation/videos/avkanim_blink_00.mp4'
movie_2 = '/home/pi/mada-/pollunation/videos/tzaleket_blink_00.mp4'

print 'Debug 2'
o1 = omxplayer.OMXPlayer(mediafile=movie_1, loop = False)
o2 = omxplayer.OMXPlayer(mediafile=movie_2, loop = False)

print 'Debug 3'
o1.play()
time.sleep(2)
    
print 'Debug 4'
o1.pause()
o2.play()

time.sleep(2)

print 'Debug 5'
o2.pause()
o1.play()

time.sleep(2)

print 'Debug 6'
o1.stop()
o2.stop()

