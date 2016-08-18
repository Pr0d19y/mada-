import threading
import logging
import datetime
import os
import subprocess
import re
import sys
sys.path.append("/home/pi/git/mada-")
from classes import omxplayer
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BOARD)

## Tomato (bi-sex) ##

#debug_jmp = 29
#setup(debug_jmp, IN, pull_up_down=PUD_UP)
#debug = not input(debug_jmp)

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = '/home/pi/git/mada-/pollunation/videos/avkanim_blink_00.mp4'
dust_complete_video_file = '/home/pi/git/mada-/pollunation/videos/avkanim_sequence_00.mp4'
#idle_video = OMXPlayer(idle_video_file, loop = True, debug=debug)
#dust_complete_video = OMXPlayer(dust_complete_video_file, debug=debug)
#idle_video = omxplayer.OMXPlayer(mediafile=idle_video_file, args='--loop --no-osd -b', start_playback=False)
#dust_complete_video = omxplayer.OMXPlayer(mediafile=dust_complete_video_file, args='--no-osd -b', start_playback=False)


# Set GPIO names
bee_on        = 38
bee_buzz      = 37

GPIO.setup(bee_on      , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bee_buzz    , GPIO.OUT)

GPIO.output(bee_buzz, True)

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
  
  global idle_video_file
  print 'play movie a here'
  subprocess.Popen(['feh --hide-pointer -x -q -B black -F /home/pi/git/mada-/Pollunation_OKap/idle.png'],shell=True)
  while True:
	#print (["omxplayer"," --loop --no-osd -b ",dust_complete_video_file ])
	print 'before play a!!!!!!!!!!!!'
	subprocess.Popen(['exec omxplayer' + ' --loop --no-osd -b ' + idle_video_file] ,shell=True )
	#idle_video = omxplayer.OMXPlayer(mediafile=idle_video_file, args='--loop --no-osd -b', start_playback=True)
	state_bee_on()

def state_bee_on():
  global idle_video
  global idle_video_file
  start_time = time.time()
  while  True:
    if not GPIO.input(bee_on):
      start_time = time.time()


    if (time.time() - start_time)>= CATCH_TIME_TH:
      #idle_video.stop()
      #subprocess.call(['scrot'],shell=True)
      subprocess.call(['pkill omxplayer'] ,shell=True )
      print 'after play a!!!!!!!!!!!'
      return state_dust_complete()

def state_dust_complete():

  #sleep(1)
  #proc.kill
  print 'before play b!!!!!!!!!!!!!!11'
  global dust_complete_video_file
  subprocess.call(['omxplayer'+' --no-osd -b '+dust_complete_video_file ],shell=True)
  #proc.kill
  #sleep(5)
  print 'after play b!!!!!!!!!!!!!!!!!'




