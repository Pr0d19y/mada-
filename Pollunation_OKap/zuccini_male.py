import subprocess
import re
import sys
sys.path.append("/home/pi/git/mada-")
import RPi.GPIO as GPIO
import time
from omxplayer import OMXPlayer

GPIO.setmode(GPIO.BOARD)

## Zuccini male !! ##

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = 'videos/zuccini/zuccini_male_1024x600/zuccini_male_blink_1024x600.mp4'
wait_video_file = 'videos/zuccini/zuccini_male_1024x600/zuccini_male_wait_1024x600.mp4'
after_video_file = 'videos/zuccini/zuccini_male_1024x600/zuccini_male_after_1024x600.mp4'



# Set GPIO names
bee_lights    = 36
from_female   = 31
to_female     = 32
bee_sensor    = 38


GPIO.setup(from_female  , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bee_sensor  , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(to_female    , GPIO.OUT)
GPIO.setup(bee_lights , GPIO.OUT)

GPIO.output(bee_lights, False)
GPIO.output(to_female, False)


idle_movie_controller = OMXPlayer(filename=idle_video_file, args=['--loop', '-b', '--no-osd'])
after_movie_controller = OMXPlayer(filename=after_video_file, args=['-b', '--no-osd'])
wait_movie_controller = OMXPlayer(filename=wait_video_file, args=['--loop', '-b', '--no-osd'])


def state_idle():
  #print 'play movie a here'
  idle_movie_controller.play()
  while True:
	print 'before play a!!!!!!!!!!!!'
	state_bee_on()

def state_bee_on():
  start_time = time.time()
  while  True:
    if not GPIO.input(bee_on):
      start_time = time.time()


    if (time.time() - start_time)>= CATCH_TIME_TH:
      idle_movie_controller.pause()
      time.sleep(0.05)
      idle_movie_controller.set_position(0)
      print 'after play a!!!!!!!!!!!'
      return state_dust_complete()

def wait_for_female():

  print 'before play b!!!!!!!!!!!!!!11'
  global dust_complete_movie_controller
  dust_complete_movie_controller.play_sync()
  dust_complete_movie_controller.quit()
  dust_complete_movie_controller = OMXPlayer(filename=dust_complete_video_file, args=['-b', '--no-osd'])
  idle_movie_controller.play()
  print 'after play b!!!!!!!!!!!!!!!!!'




