
import subprocess
import re
import sys
sys.path.append("/home/pi/git/mada-")
import RPi.GPIO as GPIO
import time
from omxplayer import OMXPlayer

GPIO.setmode(GPIO.BOARD)

## Tomato (bi-sex) ##

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = '/home/pi/mada-/pollunation/videos/tomato_blink_1024X600.mp4'
dust_complete_video_file = '/home/pi/mada-/pollunation/videos/tomato_after_1024X600.mp4'


# Set GPIO names
bee_on        = 38
bee_buzz      = 37

GPIO.setup(bee_on      , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bee_buzz    , GPIO.OUT)

GPIO.output(bee_buzz, True)


idle_movie_controller = OMXPlayer(filename=idle_video_file, args=['--loop', '-b', '--no-osd'])
dust_complete_movie_controller = OMXPlayer(filename=dust_complete_video_file, args=['-b', '--no-osd'])

def findThisProcess( process_name ):
  ps     = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
  output = ps.stdout.read()
  ps.stdout.close()
  ps.wait()

  return output

# This is the function you can use  
def isThisRunning( process_name ):
  output = findThisProcess( process_name )

  if re.search('path/of/process'+process_name, output) is None:
    return False
  else:
    return True



def state_idle():
  print 'play movie a here'
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

def state_dust_complete():

  print 'before play b!!!!!!!!!!!!!!11'
  global dust_complete_movie_controller
  dust_complete_movie_controller.play_sync()
  dust_complete_movie_controller.quit()
  dust_complete_movie_controller = OMXPlayer(filename=dust_complete_video_file, args=['-b', '--no-osd'])
  idle_movie_controller.play()
  print 'after play b!!!!!!!!!!!!!!!!!'




